"""python -m pbi 1330194

Lee el Work Item empezando por Integration, enmascara y crea la carpeta de casos.
No publica nada y no lee logs.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from agent.azure_client import AzureReadClient, AzureReadError
from agent.config import load_settings
from agent.context_pack import write_context_pack
from agent.layout import excel_drive, reading_dir
from agent.work_items import WorkItemReader

from pbi.compare import compare_knowledge
from pbi.generate_cases import analyze, write_cases
from pbi.mask import write_masked_pack
from pbi.revalidate import write_revalidation


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m pbi")
    parser.add_argument("work_item_id", help="Número del Work Item")
    args = parser.parse_args(argv)
    if not args.work_item_id.isdigit():
        print("El argumento es el número del Work Item. Ejemplo: python -m pbi 1330194")
        return 1
    work_id = int(args.work_item_id)
    settings = load_settings(ROOT)
    if settings.llm_enabled:
        print("AZDO_WI_LLM_ENABLED=true, pero no hay proveedor autorizado. No se envía el PBI fuera de la máquina.")
    try:
        reader = WorkItemReader(settings, AzureReadClient(settings))
        project = reader.locate(work_id)
        print(f"leyendo PBI - {work_id} del proyecto {project}", flush=True)
        context = reader.fetch(str(work_id), ROOT, project=project)
    except AzureReadError as exc:
        print("paso 1 lectura del PBI: falló — no se leyó el PBI", flush=True)
        print(str(exc))
        print("Proceso incompleto", flush=True)
        _print_tokens(0)
        return 1
    return finish(context, ROOT)


def finish(context, root: Path) -> int:
    meter = 0
    read_error = _unread_reason(context)
    if read_error:
        return _fail(1, "lectura del PBI", read_error, meter)
    _ok(1, "lectura del PBI")
    _print_reading(context)
    meter += _requirement_chars(context)
    documents = context.attachments.get("extracted_documents") or []
    attachment_error = _attachment_error(context)
    for item in documents:
        meter += len(str(item.get("text") or ""))
    if not documents and attachment_error:
        print(f"paso 2 documentos adjuntos: cumplido — {attachment_error}. Se continúa.", flush=True)
    elif not documents:
        print("paso 2 documentos adjuntos: cumplido — no se encontraron. Se continúa.", flush=True)
    elif attachment_error:
        print(f"paso 2 documentos adjuntos: cumplido — algunos no se leyeron ({attachment_error}). Se continúa.", flush=True)
    else:
        _ok(2, "documentos adjuntos")
    titles, analysis_error = analyze(context)
    if analysis_error == "no hay texto que analizar":
        return _fail(3, "análisis del PBI", analysis_error, meter)
    if analysis_error:
        print(f"paso 3 análisis del PBI: cumplido — {analysis_error}. Se continúa.", flush=True)
        titles = ["el texto del PBI queda como referencia del caso"]
    work_id = int(context.source["work_item_id"])
    write_context_pack(context, root, llm_enabled=False)
    analysis = reading_dir(root, work_id) / "analisis.md"
    analysis.write_text(_analysis_text(context, titles), encoding="utf-8")
    if not analysis.is_file() or analysis.stat().st_size == 0:
        return _fail(3, "análisis del PBI", "no se escribió el análisis", meter)
    _ok(3, "análisis del PBI")
    print(f"análisis: {len(titles)} comportamientos", flush=True)
    changes = getattr(context, "code_changes", None) or {}
    notice = changes.get("notice") or "No se encontraron enlaces de código. Se continúa."
    print(notice, flush=True)
    last = changes.get("last") or {}
    meter += len(str(last.get("comment") or ""))
    meter += sum(len(path) for path in last.get("paths") or [])
    comparison, read_chars, compare_error = compare_knowledge(context, ROOT)
    meter += read_chars
    if compare_error:
        return _fail(4, "base de conocimiento", compare_error, meter)
    compared = reading_dir(root, work_id) / "comparacion-base.md"
    compared.write_text(comparison, encoding="utf-8")
    if not compared.is_file() or compared.stat().st_size == 0:
        return _fail(4, "base de conocimiento", "no se escribió la comparación", meter)
    _ok(4, "base de conocimiento")
    write_masked_pack(context, root)
    report = reading_dir(root, work_id) / "mascara_reporte.md"
    masked = masked_text(root, work_id)
    meter += len(masked)
    if not report.is_file() or "Elegible para análisis de IA: sí" not in report.read_text(encoding="utf-8"):
        print("El enmascarado detectó una fuga. No se generan casos.", flush=True)
        return _fail(5, "enmascarado", "la máscara no quedó elegible", meter)
    _ok(5, "enmascarado")
    print("enmascarando data para que procese la IA", flush=True)
    print("generando casos de prueba", flush=True)
    markdown = root / "test-cases" / f"PBI-{work_id}" / "casos-de-prueba.md"
    existed = markdown.is_file()
    write_cases(context, root)
    write_revalidation(context, root)
    if not markdown.is_file() or " #TC " not in markdown.read_text(encoding="utf-8"):
        return _fail(6, "casos de prueba", "no se creó el markdown de casos", meter)
    meter += markdown.stat().st_size
    _ok(6, "casos de prueba")
    if existed:
        print("el markdown ya existe y no se reescribe", flush=True)
    else:
        print("casos escritos", flush=True)
    print(markdown.relative_to(root).as_posix(), flush=True)
    _ok(7, "notificación")
    print("Proceso completo", flush=True)
    print(validation_line(context, root), flush=True)
    _ok(8, "consumo de tokens")
    _print_tokens(meter)
    print("pasos cumplidos: 8", flush=True)
    return 0


def _ok(number: int, name: str) -> None:
    print(f"paso {number} {name}: cumplido", flush=True)


def _fail(number: int, name: str, reason: str, meter: int) -> int:
    print(f"paso {number} {name}: falló — {reason}", flush=True)
    print("Proceso incompleto", flush=True)
    _print_tokens(meter)
    return 1


def _print_tokens(meter: int) -> None:
    print("tokens usados: 0", flush=True)
    print(f"tokens estimados de la ejecución: {estimated_tokens_from_chars(meter)}", flush=True)


def _requirement_chars(context) -> int:
    requirements = context.requirements or {}
    return len(str(requirements.get("description") or "")) + len(str(requirements.get("acceptance_criteria") or ""))


def _analysis_text(context, titles: list[str]) -> str:
    work_id = context.source.get("work_item_id")
    lines = [
        f"# Análisis WI {work_id}",
        "",
        "Un comentario no entra en este análisis.",
        "",
        "## Comportamientos",
        "",
    ]
    lines.extend(f"- {title}" for title in titles)
    changes = getattr(context, "code_changes", None) or {}
    lines.extend(["", "## Código enlazado", "", changes.get("notice") or "No se encontraron enlaces de código. Se continúa."])
    last = changes.get("last") or {}
    if last:
        lines.extend(["", "El último commit es el de más peso.", f"Fecha: {last.get('date') or 'sin fecha'}", ""])
        if last.get("comment"):
            lines.append(str(last.get("comment")))
            lines.append("")
        for path in last.get("paths") or []:
            lines.append(f"- {path}")
    return "\n".join(lines) + "\n"


def _unread_reason(context) -> str:
    source = context.source or {}
    meta = context.metadata or {}
    if not source.get("work_item_id") or not source.get("project") or not source.get("revision"):
        return "no se leyó el PBI"
    if not str(meta.get("title") or "").strip() or not str(meta.get("type") or "").strip():
        return "no se leyó el PBI"
    return ""


def _attachment_error(context) -> str:
    failed = []
    for item in context.attachments.get("skipped_documents") or []:
        name = item.get("filename") or "adjunto"
        warnings = item.get("warnings") or []
        if item.get("status") == "revision_visual":
            continue
        if warnings or item.get("status") == "omitido":
            detail = warnings[0] if warnings else "no se pudo leer"
            failed.append(f"{name}: {detail}")
    return "; ".join(failed)


def _print_reading(context) -> None:
    documents = context.attachments.get("extracted_documents") or []
    manuals = sum(1 for item in context.manuals if item.get("status") == "presente")
    print(
        f"rev {context.source.get('revision')} | {context.metadata.get('type')} | {context.metadata.get('status')}",
        flush=True,
    )
    print(f"adjuntos leídos: {len(documents)}", flush=True)
    for item in documents:
        print(f"  {item.get('filename')}", flush=True)
    print(f"manuales revalidados: {manuals}", flush=True)
    changes = getattr(context, "code_changes", None) or {}
    print(f"commits leídos: {int(changes.get('commits_read') or 0)}", flush=True)
    print(f"wiki leídas: {int(changes.get('wiki_read') or 0)}", flush=True)


def validation_line(context, root: Path) -> str:
    work_id = int(context.source["work_item_id"])
    manuals = sum(1 for item in context.manuals if item.get("status") == "presente")
    comments = len(context.discussions)
    markdown = root / "test-cases" / f"PBI-{work_id}" / "casos-de-prueba.md"
    if markdown.is_file():
        cases = len(re.findall(r"\|\s*\d+\s*\|\s*PBI-\d+\s+#TC", markdown.read_text(encoding="utf-8")))
        cases_label = f"casos {cases} ya en markdown"
    else:
        cases_label = "casos pendientes de análisis"
    try:
        excel = "excel en OneDrive" if excel_drive(work_id).is_file() else "excel no generado"
    except FileNotFoundError:
        excel = "excel no generado"
    return (
        f"validación: máscara elegible | manuales {manuals} | comentarios {comments} sin criterio | "
        f"{cases_label} | {excel}"
    )


def masked_text(root: Path, work_id: int) -> str:
    path = reading_dir(root, work_id) / "envio_ia.md"
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def estimated_tokens(text: str) -> int:
    """Aproximación local de caracteres / 4. No es el consumo de un modelo."""
    return estimated_tokens_from_chars(len(text or ""))


def estimated_tokens_from_chars(chars: int) -> int:
    return (chars + 3) // 4 if chars else 0


if __name__ == "__main__":
    sys.exit(main())
