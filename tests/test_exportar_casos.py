import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("exportar_casos", ROOT / "scripts" / "exportar_casos.py")
exportar = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(exportar)


MARKDOWN = """# PBI-1

| Término | Resultado |
|---|---|
| esta fila no es un caso | comparación |

## Casos

| # | Nombre del caso de prueba | Pasos | Resultado esperado | Resultado ejecución |
|---|---|---|---|---|
| 1 | PBI-1 #TC guardar el estado | 1. Abrir la pantalla.<br>2. Pulsar Guardar. | El estado queda en V. | Sin ejecutar. |

## Matriz de riesgos

No se califica probabilidad ni impacto.

| # | Riesgo citado | Fuente | Caso | Medición |
|---|---|---|---|---|
| 1 | Guardar no deja el estado V. | Descripción del PBI | 1 | Cubierto por el caso 1. |
| 2 | El manual contradice el botón. | Manual PI | — | Hueco. No se inventa el dato. |
"""


class ExportarCasosTests(unittest.TestCase):
    def test_cuatro_columnas_y_hoja_de_riesgos(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            markdown = folder / "casos-de-prueba.md"
            workbook = folder / "PBI-1-casos-de-prueba.xlsx"
            markdown.write_text(MARKDOWN, encoding="utf-8")
            cases = exportar.parse_md_test_cases(str(markdown))
            risks = exportar.parse_risk_matrix(str(markdown))
            self.assertEqual(len(cases), 1)
            self.assertEqual(cases[0]["pasos"], ["1. Abrir la pantalla.", "2. Pulsar Guardar."])
            self.assertEqual(cases[0]["ejecucion"], "Sin ejecutar.")
            self.assertEqual(risks[0], ["#", "Riesgo citado", "Fuente", "Caso", "Medición"])
            self.assertEqual(risks[1][1], "Guardar no deja el estado V.")
            self.assertEqual(risks[2][3], "—")
            exportar.create_excel_stdlib(cases, str(workbook), "PBI-1", risks)
            with zipfile.ZipFile(workbook) as package:
                book = package.read("xl/workbook.xml").decode("utf-8")
                cases_sheet = package.read("xl/worksheets/sheet1.xml").decode("utf-8")
                risk_sheet = package.read("xl/worksheets/sheet2.xml").decode("utf-8")
            self.assertIn('name="PBI-1"', book)
            self.assertIn('name="matriz de riesgos"', book)
            for header in ("Nombre del caso de prueba", "Pasos", "Resultado esperado", "Resultado ejecución"):
                self.assertIn(header, cases_sheet)
            self.assertIn("2. Pulsar Guardar.", cases_sheet)
            self.assertNotIn("esta fila no es un caso", cases_sheet)
            self.assertIn("Guardar no deja el estado V.", risk_sheet)
            self.assertIn("Hueco. No se inventa el dato.", risk_sheet)
            self.assertNotIn("esta fila no es un caso", risk_sheet)

    def test_sin_matriz_la_hoja_avisa(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            markdown = folder / "casos-de-prueba.md"
            workbook = folder / "salida.xlsx"
            markdown.write_text(
                "| # | Nombre del caso de prueba | Pasos | Resultado esperado | Resultado ejecución |\n"
                "|---|---|---|---|---|\n"
                "| 1 | PBI-2 #TC uno | 1. Ejecutar. | Queda el resultado. | Sin ejecutar. |\n",
                encoding="utf-8",
            )
            self.assertEqual(exportar.parse_risk_matrix(str(markdown)), [])
            exportar.create_excel_stdlib(
                exportar.parse_md_test_cases(str(markdown)),
                str(workbook),
                "PBI-2",
                [],
            )
            with zipfile.ZipFile(workbook) as package:
                risk_sheet = package.read("xl/worksheets/sheet2.xml").decode("utf-8")
            self.assertIn("El markdown no trae la matriz de riesgos.", risk_sheet)

    def test_el_pbi_1365790_separa_casos_y_riesgos(self):
        markdown = ROOT / "test-cases" / "PBI-1365790" / "casos-de-prueba.md"
        if not markdown.is_file():
            self.skipTest("no está el markdown de 1365790")
        cases = exportar.parse_md_test_cases(str(markdown))
        risks = exportar.parse_risk_matrix(str(markdown))
        self.assertEqual(len(cases), 4)
        self.assertEqual(risks[0], ["#", "Riesgo citado", "Fuente", "Caso", "Medición"])
        self.assertGreaterEqual(len(risks), 5)
        self.assertIn("estado V", cases[1]["resultado"])
        self.assertNotIn("Riesgo citado", cases[0]["nombre"])
        with tempfile.TemporaryDirectory() as folder:
            workbook = Path(folder) / "PBI-1365790-casos-de-prueba.xlsx"
            exportar.create_excel_stdlib(cases, str(workbook), "PBI-1365790", risks)
            with zipfile.ZipFile(workbook) as package:
                book = package.read("xl/workbook.xml").decode("utf-8")
                cases_sheet = package.read("xl/worksheets/sheet1.xml").decode("utf-8")
                risk_sheet = package.read("xl/worksheets/sheet2.xml").decode("utf-8")
        self.assertIn('name="matriz de riesgos"', book)
        self.assertIn("Resultado ejecución", cases_sheet)
        self.assertNotIn("Riesgo citado", cases_sheet)
        self.assertIn("Cubierto por el caso 1.", risk_sheet)
        self.assertIn("estado V", cases_sheet)


if __name__ == "__main__":
    unittest.main()
