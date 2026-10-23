#!/usr/bin/env python3
"""
Exporta casos de prueba desde un archivo .md a Excel (.xlsx).

Estructura del Excel:
  Hoja del PBI, cuatro columnas:
    A: Nombre del caso de prueba (celdas combinadas por caso)
    B: Pasos (un paso por fila)
    C: Resultado esperado (celdas combinadas por caso)
    D: Resultado ejecución (celdas combinadas por caso)
  Hoja "matriz de riesgos": la tabla de la sección Matriz de riesgos del markdown.

Uso:
  python scripts/exportar_casos.py test-cases/PBI-XXXXXX/casos-de-prueba.md
  python scripts/exportar_casos.py test-cases/PBI-XXXXXX/casos-de-prueba.md -o salida.xlsx
"""

import re
import sys
import os
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZipFile, ZIP_DEFLATED


def clean_markdown(text: str) -> str:
    """Elimina sintaxis markdown del texto: negrillas, backticks, cursivas."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)  # **negrilla**
    text = re.sub(r"__(.+?)__", r"\1", text)       # __negrilla__
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", text)  # *cursiva*
    text = re.sub(r"(?<![\w])_(.+?)_(?![\w])", r"\1", text)  # _cursiva_, no REF_STA_DET
    text = re.sub(r"`(.+?)`", r"\1", text)         # `código`
    return text


def parse_md_test_cases(md_path: str) -> list[dict]:
    """Lee el .md y extrae los casos de prueba de la tabla markdown."""
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Buscar la tabla de casos de prueba
    table_match = re.search(
        r"\|\s*#\s*\|\s*Nombre del caso de prueba\s*\|.*?\n"
        r"\|[-\s|]+\n"
        r"((?:\|.*\n?)+)",
        content,
    )
    if not table_match:
        print("ERROR: No se encontró la tabla de casos de prueba en el .md")
        sys.exit(1)

    rows_raw = table_match.group(1).strip().split("\n")
    cases = []

    for row in rows_raw:
        # Limpiar la fila
        cols = [c.strip() for c in row.split("|")]
        # Quitar elementos vacíos al inicio/fin por los pipes exteriores
        cols = [c for c in cols if c != ""]
        if len(cols) < 4:
            continue

        num = cols[0].strip()
        nombre = cols[1].strip()
        pasos_raw = cols[2].strip()
        resultado = cols[3].strip()
        ejecucion = cols[4].strip() if len(cols) > 4 else ""

        # Separar pasos por <br> y limpiar
        pasos = re.split(r"<br\s*/?>", pasos_raw)
        pasos = [p.strip() for p in pasos if p.strip()]

        cases.append({
            "num": num,
            "nombre": clean_markdown(nombre),
            "pasos": [clean_markdown(p) for p in pasos],
            "resultado": clean_markdown(resultado),
            "ejecucion": clean_markdown(ejecucion),
        })

    return cases


def parse_risk_matrix(md_path: str) -> list[list[str]]:
    """Lee la tabla que sigue a '## Matriz de riesgos'. No usa la tabla de casos."""
    content = Path(md_path).read_text(encoding="utf-8")
    section = re.search(r"##\s+Matriz de riesgos\s*\n(.*)", content, re.IGNORECASE | re.DOTALL)
    if not section:
        return []
    body = re.split(r"\n##\s+", section.group(1), maxsplit=1)[0]
    table = re.search(r"(\|[^\n]+\|\n\|[-:\s|]+\n(?:\|[^\n]*\n?)*)", body)
    if not table:
        return []
    rows = []
    for line in table.group(1).strip().split("\n"):
        if re.match(r"^\|\s*[-: ]+(\|\s*[-: ]+)*\|?\s*$", line):
            continue
        rows.append(_split_row(line))
    return [row for row in rows if any(cell.strip() for cell in row)]


def _split_row(line: str) -> list[str]:
    parts = line.strip().split("|")
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return [clean_markdown(part.strip()) for part in parts]


def _col_letter(n: int) -> str:
    letters = ""
    while n:
        n, rem = divmod(n - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def _inline(ref: str, text: str, style: int) -> str:
    safe = escape(text or "")
    return f'<c r="{ref}" t="inlineStr" s="{style}"><is><t xml:space="preserve">{safe}</t></is></c>'


def _risk_sheet_xml(risks: list[list[str]]) -> str:
    rows = risks or [["El markdown no trae la matriz de riesgos."]]
    width = max(len(row) for row in rows)
    rows_xml = []
    for index, row in enumerate(rows, start=1):
        padded = row + [""] * (width - len(row))
        style = 1 if index == 1 and risks else 3
        cells = "".join(_inline(f"{_col_letter(col)}{index}", padded[col - 1], style) for col in range(1, width + 1))
        rows_xml.append(f'<row r="{index}" ht="32" customHeight="1">{cells}</row>')
    cols_xml = "".join(
        f'<col min="{col}" max="{col}" width="36" customWidth="1"/>' for col in range(1, width + 1)
    )
    last_ref = f"{_col_letter(width)}{len(rows)}"
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<dimension ref="A1:{last_ref}"/>
<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>
<cols>{cols_xml}</cols>
<sheetData>{"".join(rows_xml)}</sheetData>
</worksheet>'''


def create_excel_stdlib(cases: list[dict], output_path: str, pbi_id: str = "", risks: list[list[str]] | None = None):
    """Misma hoja que create_excel, sin openpyxl. xlsx es un zip OOXML."""
    headers = ["Nombre del caso de prueba", "Pasos", "Resultado esperado", "Resultado ejecución"]
    ultima_col = 4
    widths = [45, 65, 75, 80]

    rows_xml = []
    merges = []
    header_cells = "".join(
        _inline(f"{_col_letter(i)}1", headers[i - 1], 1) for i in range(1, ultima_col + 1)
    )
    rows_xml.append(f'<row r="1" ht="22" customHeight="1">{header_cells}</row>')

    current_row = 2
    for case in cases:
        num_pasos = max(len(case["pasos"]), 1)
        start_row = current_row
        end_row = current_row + num_pasos - 1
        for i in range(num_pasos):
            r = start_row + i
            cells = []
            if i == 0:
                cells.append(_inline(f"A{r}", case["nombre"], 2))
            cells.append(_inline(f"B{r}", case["pasos"][i] if i < len(case["pasos"]) else "", 3))
            if i == 0:
                cells.append(_inline(f"C{r}", case["resultado"], 3))
                cells.append(_inline(f"D{r}", case.get("ejecucion") or "", 3))
            rows_xml.append(
                f'<row r="{r}" ht="48" customHeight="1">{"".join(cells)}</row>'
            )
        if num_pasos > 1:
            merges.append(f"A{start_row}:A{end_row}")
            merges.append(f"C{start_row}:C{end_row}")
            merges.append(f"D{start_row}:D{end_row}")
        current_row = end_row + 2

    last_row = max(current_row - 2, 1)
    last_ref = f"{_col_letter(ultima_col)}{last_row}"
    cols_xml = "".join(
        f'<col min="{i}" max="{i}" width="{widths[i - 1]}" customWidth="1"/>'
        for i in range(1, ultima_col + 1)
    )
    merge_xml = ""
    if merges:
        merge_xml = f'<mergeCells count="{len(merges)}">' + "".join(
            f'<mergeCell ref="{ref}"/>' for ref in merges
        ) + "</mergeCells>"

    sheet = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<dimension ref="A1:{last_ref}"/>
<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>
<cols>{cols_xml}</cols>
<sheetData>{"".join(rows_xml)}</sheetData>
{merge_xml}
</worksheet>'''

    risk_sheet = _risk_sheet_xml(risks or [])
    sheet_name = (pbi_id or "Casos de prueba")[:31]
    styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<fonts count="2">
<font><sz val="10"/><name val="Calibri"/></font>
<font><b/><sz val="11"/><name val="Calibri"/></font>
</fonts>
<fills count="3">
<fill><patternFill patternType="none"/></fill>
<fill><patternFill patternType="gray125"/></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFD9E2F3"/></patternFill></fill>
</fills>
<borders count="2">
<border><left/><right/><top/><bottom/></border>
<border>
<left style="thin"/><right style="thin"/><top style="thin"/><bottom style="thin"/>
</border>
</borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="4">
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
<xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>
<xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>
<xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
</cellXfs>
</styleSheet>'''

    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>'''
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>'''
    workbook = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets>
<sheet name="{escape(sheet_name)}" sheetId="1" r:id="rId1"/>
<sheet name="matriz de riesgos" sheetId="2" r:id="rId3"/>
</sheets>
</workbook>'''
    wb_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
</Relationships>'''

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with ZipFile(output_path, "w", ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("xl/workbook.xml", workbook)
        zf.writestr("xl/_rels/workbook.xml.rels", wb_rels)
        zf.writestr("xl/styles.xml", styles)
        zf.writestr("xl/worksheets/sheet1.xml", sheet)
        zf.writestr("xl/worksheets/sheet2.xml", risk_sheet)
    print(f"Excel generado: {output_path}")
    print(f"  {len(cases)} casos de prueba exportados.")
    print(f"  hoja matriz de riesgos: {max(len(risks or []) - 1, 0)} filas.")


def create_excel(cases: list[dict], output_path: str, pbi_id: str = "", risks: list[list[str]] | None = None):
    """Genera el libro: cuatro columnas de casos y la hoja matriz de riesgos."""
    try:
        import openpyxl
        from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
    except ModuleNotFoundError:
        create_excel_stdlib(cases, output_path, pbi_id, risks)
        return

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = pbi_id or "Casos de prueba"

    # Estilos
    header_font = Font(name="Calibri", bold=True, size=11)
    header_fill = PatternFill(start_color="D9E2F3", end_color="D9E2F3", fill_type="solid")
    cell_font = Font(name="Calibri", size=10)
    thin_border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin"),
    )
    wrap_alignment = Alignment(wrap_text=True, vertical="top")
    center_alignment = Alignment(wrap_text=True, vertical="center")

    ultima_col = 4

    # Anchos de columna
    ws.column_dimensions["A"].width = 45
    ws.column_dimensions["B"].width = 65
    ws.column_dimensions["C"].width = 75
    ws.column_dimensions["D"].width = 80

    # Header
    headers = ["Nombre del caso de prueba", "Pasos", "Resultado esperado", "Resultado ejecución"]
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin_border
        cell.alignment = Alignment(vertical="center")

    current_row = 2

    for case in cases:
        num_pasos = len(case["pasos"])
        start_row = current_row
        end_row = current_row + num_pasos - 1

        # Columna A: Nombre (merged)
        ws.cell(row=start_row, column=1, value=case["nombre"])
        if num_pasos > 1:
            ws.merge_cells(
                start_row=start_row, start_column=1,
                end_row=end_row, end_column=1,
            )

        # Columna B: Pasos (un paso por fila)
        for i, paso in enumerate(case["pasos"]):
            ws.cell(row=start_row + i, column=2, value=paso)

        # Columna C: Resultado (merged)
        ws.cell(row=start_row, column=3, value=case["resultado"])
        if num_pasos > 1:
            ws.merge_cells(
                start_row=start_row, start_column=3,
                end_row=end_row, end_column=3,
            )

        ws.cell(row=start_row, column=4, value=case.get("ejecucion") or "")
        if num_pasos > 1:
            ws.merge_cells(
                start_row=start_row, start_column=4,
                end_row=end_row, end_column=4,
            )

        # Aplicar estilos a todas las filas del caso
        for r in range(start_row, end_row + 1):
            for c in range(1, ultima_col + 1):
                cell = ws.cell(row=r, column=c)
                cell.font = cell_font
                cell.border = thin_border
                cell.alignment = wrap_alignment if c != 1 else center_alignment
            ws.row_dimensions[r].height = 48

        # Fila vacía de separación entre casos
        current_row = end_row + 2

    risk_rows = risks or [["El markdown no trae la matriz de riesgos."]]
    risk_sheet = wb.create_sheet("matriz de riesgos")
    for row_index, row in enumerate(risk_rows, start=1):
        for col_index, value in enumerate(row, start=1):
            cell = risk_sheet.cell(row=row_index, column=col_index, value=value)
            cell.font = header_font if row_index == 1 and risks else cell_font
            cell.fill = header_fill if row_index == 1 and risks else PatternFill()
            cell.border = thin_border
            cell.alignment = wrap_alignment
            risk_sheet.column_dimensions[_col_letter(col_index)].width = 36
        risk_sheet.row_dimensions[row_index].height = 32

    wb.save(output_path)
    print(f"Excel generado: {output_path}")
    print(f"  {len(cases)} casos de prueba exportados.")
    print(f"  hoja matriz de riesgos: {max(len(risks or []) - 1, 0)} filas.")


def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/exportar_casos.py <ruta-al-md> [-o salida.xlsx]")
        sys.exit(1)

    md_path = sys.argv[1]

    # Determinar output path
    if "-o" in sys.argv:
        output_path = sys.argv[sys.argv.index("-o") + 1]
    else:
        pbi_num = re.search(r"PBI-(\d+)", md_path)
        if not pbi_num:
            print("El markdown no trae el número del PBI. No se escribió el Excel.")
            sys.exit(1)
        root = Path(__file__).resolve().parents[1]
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))
        from agent.layout import excel_drive

        try:
            output_path = str(excel_drive(pbi_num.group(1)))
        except FileNotFoundError:
            print("No está la carpeta de OneDrive QA nico/Test cases. No se escribió el Excel en el proyecto.")
            sys.exit(1)

    pbi_match = re.search(r"(PBI-\d+)", md_path)
    pbi_id = pbi_match.group(1) if pbi_match else ""

    cases = parse_md_test_cases(md_path)
    risks = parse_risk_matrix(md_path)
    create_excel(cases, output_path, pbi_id, risks)


if __name__ == "__main__":
    main()
