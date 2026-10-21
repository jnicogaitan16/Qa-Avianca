#!/usr/bin/env python3
"""
Exporta casos de prueba desde un archivo .md a Excel (.xlsx).

Estructura del Excel (3 columnas):
  A: Nombre del caso de prueba (celdas combinadas por caso)
  B: Pasos (un paso por fila)
  C: Resultado esperado (celdas combinadas por caso)

Uso:
  python scripts/exportar_casos.py test-cases/PBI-XXXXXX/casos-de-prueba.md
  python scripts/exportar_casos.py test-cases/PBI-XXXXXX/casos-de-prueba.md -o salida.xlsx
"""

import re
import sys
import os
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter


def clean_markdown(text: str) -> str:
    """Elimina sintaxis markdown del texto: negrillas, backticks, cursivas."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)  # **negrilla**
    text = re.sub(r"__(.+?)__", r"\1", text)       # __negrilla__
    text = re.sub(r"\*(.+?)\*", r"\1", text)       # *cursiva*
    text = re.sub(r"_(.+?)_", r"\1", text)         # _cursiva_
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

        # Separar pasos por <br> y limpiar
        pasos = re.split(r"<br\s*/?>", pasos_raw)
        pasos = [p.strip() for p in pasos if p.strip()]

        cases.append({
            "num": num,
            "nombre": clean_markdown(nombre),
            "pasos": [clean_markdown(p) for p in pasos],
            "resultado": clean_markdown(resultado),
        })

    return cases


def create_excel(cases: list[dict], output_path: str, pbi_id: str = ""):
    """Genera el archivo Excel con la estructura de 3 columnas."""
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

    # Anchos de columna
    ws.column_dimensions["A"].width = 45
    ws.column_dimensions["B"].width = 65
    ws.column_dimensions["C"].width = 75

    # Header
    headers = ["Nombre del caso de prueba", "Pasos", "Resultado"]
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

        # Aplicar estilos a todas las filas del caso
        for r in range(start_row, end_row + 1):
            for c in range(1, 4):
                cell = ws.cell(row=r, column=c)
                cell.font = cell_font
                cell.border = thin_border
                cell.alignment = center_alignment if c != 2 else wrap_alignment

        # Fila vacía de separación entre casos
        current_row = end_row + 2

    wb.save(output_path)
    print(f"Excel generado: {output_path}")
    print(f"  {len(cases)} casos de prueba exportados.")


def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/exportar_casos.py <ruta-al-md> [-o salida.xlsx]")
        sys.exit(1)

    md_path = sys.argv[1]

    # Determinar output path
    if "-o" in sys.argv:
        output_path = sys.argv[sys.argv.index("-o") + 1]
    else:
        # Por defecto: mismo directorio que el .md
        md_dir = os.path.dirname(md_path)
        # Extraer PBI ID del path
        pbi_match = re.search(r"(PBI-\d+)", md_path)
        pbi_id = pbi_match.group(1) if pbi_match else "casos"
        output_path = os.path.join(md_dir, f"{pbi_id}-casos-de-prueba.xlsx")

    pbi_match = re.search(r"(PBI-\d+)", md_path)
    pbi_id = pbi_match.group(1) if pbi_match else ""

    cases = parse_md_test_cases(md_path)
    create_excel(cases, output_path, pbi_id)


if __name__ == "__main__":
    main()
