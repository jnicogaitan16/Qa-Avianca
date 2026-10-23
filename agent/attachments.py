"""Extracción pasiva de adjuntos. No ejecuta macros, fórmulas ni binarios."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree


ALLOWED = {
    ".txt": "text/plain",
    ".md": "text/markdown",
    ".csv": "text/csv",
    ".xml": "application/xml",
    ".json": "application/json",
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}
VISUAL = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".tif", ".tiff", ".bmp"}


@dataclass
class ExtractedDocument:
    filename: str
    extension: str
    status: str
    text: str = ""
    sheets_or_pages: list[str] = field(default_factory=list)
    sha256: str = ""
    source_url: str = ""
    warnings: list[str] = field(default_factory=list)


def safe_name(name: str) -> str:
    base = Path(name.replace("\\", "/")).name
    base = re.sub(r"[^A-Za-z0-9._ -]", "_", base).strip(" .")
    return base or "adjunto"


def extract_bytes(filename: str, payload: bytes, limit_chars: int, source_url: str = "") -> ExtractedDocument:
    name = safe_name(filename)
    ext = Path(name).suffix.lower()
    digest = hashlib.sha256(payload).hexdigest()
    doc = ExtractedDocument(filename=name, extension=ext, status="omitido", sha256=digest, source_url=source_url)
    if ext in VISUAL:
        doc.status = "revision_visual"
        doc.warnings.append("Imagen. Requiere revisión visual. No hay OCR en esta versión.")
        return doc
    if ext not in ALLOWED:
        doc.warnings.append("Extensión fuera de la lista permitida.")
        return doc
    try:
        if ext in {".txt", ".md"}:
            doc.text = _decode(payload)
            doc.status = "extraido"
        elif ext == ".csv":
            doc.text, note = _csv(payload)
            doc.sheets_or_pages = ["csv"]
            doc.status = "extraido"
            if note:
                doc.warnings.append(note)
        elif ext == ".xml":
            doc.text, note = _xml(payload)
            doc.sheets_or_pages = ["xml"]
            doc.status = "extraido"
            if note:
                doc.warnings.append(note)
        elif ext == ".json":
            doc.text = json.dumps(json.loads(_decode(payload)), ensure_ascii=False, indent=2)
            doc.status = "extraido"
        elif ext == ".docx":
            doc.text = _docx(payload)
            doc.sheets_or_pages = ["word/document.xml"]
            doc.status = "extraido"
        elif ext == ".xlsx":
            text, sheets = _xlsx(payload)
            doc.text = text
            doc.sheets_or_pages = sheets
            doc.status = "extraido"
        elif ext == ".pdf":
            doc.text, pages, note = _pdf(payload)
            doc.sheets_or_pages = pages
            if note:
                doc.status = "omitido"
                doc.warnings.append(note)
            elif doc.text.strip():
                doc.status = "extraido"
            else:
                doc.status = "revision_visual"
                doc.warnings.append("PDF sin texto extraíble. Puede ser un escaneo. No se inventa contenido.")
    except Exception as exc:  # noqa: BLE001
        doc.status = "omitido"
        doc.warnings.append(f"No se pudo extraer: {type(exc).__name__}.")
        doc.text = ""
    if len(doc.text) > limit_chars:
        doc.text = doc.text[:limit_chars]
        doc.warnings.append("Texto truncado por AZDO_WI_MAX_EXTRACT_CHARS.")
    return doc


def _decode(payload: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return payload.decode(encoding)
        except UnicodeDecodeError:
            continue
    return payload.decode("latin-1", errors="replace")


def _csv(payload: bytes) -> tuple[str, str]:
    rows = _csv_rows(_decode(payload))
    if not rows:
        return "", "CSV sin filas."
    header = [_clean_header(cell) for cell in rows[0]]
    data = rows[1:]
    lines = [
        f"filas_datos: {len(data)}",
        f"columnas: {len(header)}",
        "encabezado: " + " | ".join(header),
    ]
    full = len(data) <= 200 and len(payload) <= 100_000
    if full:
        lines.extend(_join_row(header, row) for row in data)
        return "\n".join(lines), ""
    lines.extend(_csv_profile(header, data))
    note = (
        f"CSV de {len(data)} filas. Se conservan columnas, conteos y una muestra corta. "
        "El archivo completo no se copia al contexto."
    )
    return "\n".join(lines), note


def _csv_rows(text: str) -> list[list[str]]:
    standard = list(csv.reader(io.StringIO(text), csv.excel))
    if not _collapsed(standard):
        return standard
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return standard
    header = [_clean_header(cell) for cell in next(csv.reader([lines[0]]))]
    rows = [header]
    for line in lines[1:]:
        parsed = _unwrap_wrapped_row(line, len(header))
        rows.append(parsed or [line])
    return rows


def _collapsed(rows: list[list[str]]) -> bool:
    if len(rows) < 2 or len(rows[0]) < 2:
        return False
    width = len(rows[0])
    sample = rows[1:6]
    return sum(1 for row in sample if len(row) < width) >= 1


def _unwrap_wrapped_row(line: str, width: int) -> list[str] | None:
    raw = line.strip()
    if len(raw) >= 2 and raw[0] == '"' and raw[-1] == '"':
        raw = raw[1:-1]
    parts = raw.split(',""', width - 1)
    if len(parts) < width:
        return None
    fields = [parts[0].strip().strip('"')]
    for part in parts[1:]:
        fields.append(part.strip().strip('"').replace('""', '"').rstrip(";"))
    return fields


def _csv_profile(header: list[str], data: list[list[str]]) -> list[str]:
    lines: list[str] = []
    names = [name.lower() for name in header]
    if "service" in names:
        index = names.index("service")
        counts: dict[str, int] = {}
        for row in data:
            if len(row) <= index:
                continue
            service = row[index].strip()
            if service:
                counts[service] = counts.get(service, 0) + 1
        clean = {name: count for name, count in counts.items() if '"' not in name and "{" not in name}
        dirty = sum(count for name, count in counts.items() if name not in clean)
        top = sorted(clean.items(), key=lambda item: item[1], reverse=True)[:5]
        lines.append("servicios: " + ", ".join(f"{name} ({count})" for name, count in top))
        if dirty:
            lines.append(f"filas_no_partidas: {dirty}")
    content_index = names.index("content") if "content" in names else -1
    if content_index >= 0:
        errors = 0
        warnings = 0
        samples: list[str] = []
        for row in data:
            if len(row) <= content_index:
                continue
            text = row[content_index]
            lowered = f" {text.lower()} "
            if " error " in lowered:
                errors += 1
                if len(samples) < 5:
                    samples.append(_cell(text, 220))
            elif " warn " in lowered:
                warnings += 1
        lines.append(f"lineas_error: {errors}")
        lines.append(f"lineas_warn: {warnings}")
        if samples:
            lines.append("muestra_error:")
            lines.extend(f"- {item}" for item in samples)
    else:
        lines.extend(_join_row(header, row) for row in data[:30])
    return lines


def _join_row(header: list[str], row: list[str]) -> str:
    return " | ".join(_cell(cell) for cell in row)


def _clean_header(value: str) -> str:
    return value.strip().strip(";").strip()


def _cell(value: str, limit: int = 180) -> str:
    text = " ".join(value.split())
    if len(text) <= limit:
        return text
    return text[:limit] + "..."


def _xml(payload: bytes) -> tuple[str, str]:
    root = ElementTree.fromstring(payload)
    lines: list[str] = [f"raiz: {_local(root.tag)}"]
    kept = 0
    for element in root.iter():
        if kept >= 400:
            break
        text = " ".join((element.text or "").split())
        if not text:
            continue
        lines.append(f"{_local(element.tag)}: {_cell(text)}")
        kept += 1
    note = ""
    if kept >= 400:
        note = "XML grande. El contexto conserva los primeros 400 textos; no se copia el documento completo."
    return "\n".join(lines), note


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _docx(payload: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(payload)) as package:
        xml = package.read("word/document.xml")
    root = ElementTree.fromstring(xml)
    texts = [node.text or "" for node in root.iter() if node.tag.endswith("}t")]
    return "\n".join(part.strip() for part in texts if part and part.strip())


def _xlsx(payload: bytes) -> tuple[str, list[str]]:
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(io.BytesIO(payload)) as package:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in package.namelist():
            root = ElementTree.fromstring(package.read("xl/sharedStrings.xml"))
            for item in root.findall("m:si", ns):
                shared.append("".join(node.text or "" for node in item.iter() if node.tag.endswith("}t")))
        labels = _xlsx_sheet_names(package, ns)
        sheets = [name for name in package.namelist() if name.startswith("xl/worksheets/sheet")]
        priority = {"request": 0, "response": 1, "definición técnica": 2, "definicion tecnica": 2}
        sheets.sort(key=lambda name: priority.get(labels.get(name, "").lower(), 9))
        blocks: list[str] = []
        used: list[str] = []
        for sheet_name in sheets:
            root = ElementTree.fromstring(package.read(sheet_name))
            lines: list[str] = []
            for row in root.findall(".//m:row", ns)[:80]:
                cells: list[str] = []
                for cell in row.findall("m:c", ns):
                    kind = cell.attrib.get("t")
                    value = cell.find("m:v", ns)
                    inline = cell.find("m:is", ns)
                    raw = ""
                    if kind == "s" and value is not None and value.text and value.text.isdigit():
                        raw = shared[int(value.text)]
                    elif kind == "inlineStr" and inline is not None:
                        raw = "".join(node.text or "" for node in inline.iter() if node.tag.endswith("}t"))
                    elif value is not None and value.text:
                        raw = value.text
                    cells.append(" ".join(raw.split()))
                if any(cells):
                    lines.append(" | ".join(cells))
            if not lines:
                continue
            label = labels.get(sheet_name, sheet_name)
            used.append(label)
            blocks.append(f"# {label}\n" + "\n".join(lines))
    return "\n\n".join(blocks), used


def _xlsx_sheet_names(package: zipfile.ZipFile, ns: dict[str, str]) -> dict[str, str]:
    if "xl/workbook.xml" not in package.namelist() or "xl/_rels/workbook.xml.rels" not in package.namelist():
        return {}
    workbook = ElementTree.fromstring(package.read("xl/workbook.xml"))
    rels = ElementTree.fromstring(package.read("xl/_rels/workbook.xml.rels"))
    targets = {rel.attrib.get("Id", ""): rel.attrib.get("Target", "") for rel in rels}
    names: dict[str, str] = {}
    for sheet in workbook.findall("m:sheets/m:sheet", ns):
        rid = sheet.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id", "")
        target = targets.get(rid, "").lstrip("/")
        if target and not target.startswith("xl/"):
            target = "xl/" + target
        if target:
            names[target] = sheet.attrib.get("name") or target
    return names


def _pdf(payload: bytes) -> tuple[str, list[str], str]:
    try:
        from pypdf import PdfReader
    except ImportError:
        return "", [], "pypdf no está instalado. El PDF queda sin interpretar."
    reader = PdfReader(io.BytesIO(payload))
    pages: list[str] = []
    chunks: list[str] = []
    for index, page in enumerate(reader.pages[:30], start=1):
        text = page.extract_text() or ""
        pages.append(f"pagina-{index}")
        if text.strip():
            chunks.append(f"# pagina {index}\n{text.strip()}")
    return "\n\n".join(chunks), pages, ""
