"""Pasa docs/informe-qa-avianca.md a un .docx. No usa librerías externas."""

from __future__ import annotations

import re
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
ORIGEN = ROOT / "docs" / "informe-qa-avianca.md"
DESTINO = ROOT / "docs" / "informe-qa-avianca.docx"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def _runs(text: str, *, code: bool = False) -> str:
    if code:
        return _run(text, code=True)
    parts = re.split(r"(`[^`]+`)", text)
    xml = []
    for part in parts:
        if part.startswith("`") and part.endswith("`") and len(part) >= 2:
            xml.append(_run(part[1:-1], code=True))
        else:
            xml.append(_run(part))
    return "".join(xml)


def _run(text: str, *, code: bool = False) -> str:
    if text == "":
        return ""
    fonts = "<w:rFonts w:ascii=\"Consolas\" w:hAnsi=\"Consolas\"/>" if code else ""
    size = "<w:sz w:val=\"20\"/><w:szCs w:val=\"20\"/>" if code else ""
    shade = "<w:shd w:val=\"clear\" w:color=\"auto\" w:fill=\"F2F2F2\"/>" if code else ""
    return (
        f"<w:r><w:rPr>{fonts}{size}{shade}</w:rPr>"
        f"<w:t xml:space=\"preserve\">{escape(text)}</w:t></w:r>"
    )


def _p(text: str, style: str = "Normal", *, code: bool = False) -> str:
    if code:
        pieces = []
        lines = text.split("\n")
        for index, line in enumerate(lines):
            pieces.append(_run(line, code=True))
            if index < len(lines) - 1:
                pieces.append("<w:r><w:br/></w:r>")
        body = "".join(pieces)
    else:
        body = _runs(text)
    shade = "<w:shd w:val=\"clear\" w:color=\"auto\" w:fill=\"F7F7F7\"/>" if code else ""
    return f"<w:p><w:pPr><w:pStyle w:val=\"{style}\"/>{shade}</w:pPr>{body}</w:p>"


def _bullet(text: str, number: str | None = None) -> str:
    prefix = f"{number}. " if number else "• "
    return _p(prefix + text.strip())


def _table(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    width = max(len(row) for row in rows)
    grid = "".join("<w:gridCol w:w=\"3120\"/>" for _ in range(width))
    trs = []
    for index, row in enumerate(rows):
        cells = []
        padded = row + [""] * (width - len(row))
        for cell in padded:
            fill = "<w:shd w:val=\"clear\" w:color=\"auto\" w:fill=\"1F4E79\"/>" if index == 0 else ""
            color = "<w:color w:val=\"FFFFFF\"/>" if index == 0 else ""
            bold = "<w:b/>" if index == 0 else ""
            cells.append(
                "<w:tc>"
                "<w:tcPr><w:tcW w:w=\"3120\" w:type=\"dxa\"/>"
                f"{fill}"
                "<w:tcMar><w:top w:w=\"60\" w:type=\"dxa\"/><w:left w:w=\"80\" w:type=\"dxa\"/>"
                "<w:bottom w:w=\"60\" w:type=\"dxa\"/><w:right w:w=\"80\" w:type=\"dxa\"/></w:tcMar>"
                "</w:tcPr>"
                "<w:p><w:r><w:rPr>"
                f"{bold}{color}<w:sz w:val=\"20\"/><w:szCs w:val=\"20\"/>"
                "</w:rPr>"
                f"<w:t xml:space=\"preserve\">{escape(cell)}</w:t></w:r></w:p>"
                "</w:tc>"
            )
        trs.append(f"<w:tr>{''.join(cells)}</w:tr>")
    borders = (
        "<w:tblBorders>"
        "<w:top w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"BDD3E6\"/>"
        "<w:left w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"BDD3E6\"/>"
        "<w:bottom w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"BDD3E6\"/>"
        "<w:right w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"BDD3E6\"/>"
        "<w:insideH w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"BDD3E6\"/>"
        "<w:insideV w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"BDD3E6\"/>"
        "</w:tblBorders>"
    )
    return (
        "<w:tbl><w:tblPr><w:tblW w:w=\"9360\" w:type=\"dxa\"/>"
        f"{borders}<w:tblLook w:val=\"04A0\"/></w:tblPr>"
        f"<w:tblGrid>{grid}</w:tblGrid>{''.join(trs)}</w:tbl>"
    )


def _split_row(line: str) -> list[str]:
    parts = line.strip().split("|")
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return [re.sub(r"`([^`]+)`", r"\1", part.strip()) for part in parts]


def _blocks(markdown: str) -> str:
    lines = markdown.replace("\r\n", "\n").split("\n")
    xml: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith("```"):
            chunk = []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                chunk.append(lines[index])
                index += 1
            xml.append(_p("\n".join(chunk), code=True))
            index += 1
            continue
        if line.startswith("|") and index + 1 < len(lines) and re.match(r"^\|[-:\s|]+\|?\s*$", lines[index + 1]):
            rows = [_split_row(line)]
            index += 2
            while index < len(lines) and lines[index].startswith("|"):
                rows.append(_split_row(lines[index]))
                index += 1
            xml.append(_table(rows))
            continue
        if line.startswith("### "):
            xml.append(_p(line[4:].strip(), "Heading2"))
        elif line.startswith("## "):
            xml.append(_p(line[3:].strip(), "Heading1"))
        elif line.startswith("# "):
            xml.append(_p(line[2:].strip(), "Title"))
        elif line.startswith("- "):
            xml.append(_bullet(line[2:]))
        elif re.match(r"^\d+\. ", line):
            number, text = line.split(". ", 1)
            xml.append(_bullet(text, number))
        elif line.strip() in {"", "---"}:
            pass
        else:
            xml.append(_p(line.rstrip()))
        index += 1
    return "".join(xml)


def _document(body: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{W}">
<w:body>
{body}
<w:sectPr>
<w:pgSz w:w="11906" w:h="16838"/>
<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="567" w:footer="567" w:gutter="0"/>
</w:sectPr>
</w:body>
</w:document>'''


STYLES = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="{W}">
<w:style w:type="paragraph" w:default="1" w:styleId="Normal">
<w:name w:val="Normal"/>
<w:qFormat/>
<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
<w:pPr><w:spacing w:after="160" w:line="276" w:lineRule="auto"/></w:pPr>
</w:style>
<w:style w:type="paragraph" w:styleId="Title">
<w:name w:val="Title"/>
<w:basedOn w:val="Normal"/>
<w:qFormat/>
<w:rPr><w:b/><w:color w:val="1F4E79"/><w:sz w:val="44"/><w:szCs w:val="44"/></w:rPr>
<w:pPr><w:spacing w:before="0" w:after="200"/></w:pPr>
</w:style>
<w:style w:type="paragraph" w:styleId="Heading1">
<w:name w:val="heading 1"/>
<w:basedOn w:val="Normal"/>
<w:uiPriority w:val="9"/>
<w:qFormat/>
<w:pPr><w:keepNext/><w:spacing w:before="360" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr>
<w:rPr><w:b/><w:color w:val="1F4E79"/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
</w:style>
<w:style w:type="paragraph" w:styleId="Heading2">
<w:name w:val="heading 2"/>
<w:basedOn w:val="Normal"/>
<w:uiPriority w:val="9"/>
<w:qFormat/>
<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="80"/><w:outlineLvl w:val="1"/></w:pPr>
<w:rPr><w:b/><w:color w:val="2E75B6"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
</w:style>
</w:styles>'''


def main() -> None:
    body = _blocks(ORIGEN.read_text(encoding="utf-8"))
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>'''
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>'''
    word_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''
    core = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:title>QA-Avianca. Informe de la iniciativa</dc:title>
<dc:subject>Asistencia a pruebas de reembolsos</dc:subject>
<cp:category>QA</cp:category>
</cp:coreProperties>'''
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(DESTINO, "w", ZIP_DEFLATED) as package:
        package.writestr("[Content_Types].xml", content_types)
        package.writestr("_rels/.rels", rels)
        package.writestr("word/document.xml", _document(body))
        package.writestr("word/styles.xml", STYLES)
        package.writestr("word/_rels/document.xml.rels", word_rels)
        package.writestr("docProps/core.xml", core)
    print(DESTINO)


if __name__ == "__main__":
    main()
