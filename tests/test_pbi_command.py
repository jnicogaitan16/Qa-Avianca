import tempfile
import unittest
from pathlib import Path

from agent.azure_client import AzureReadError
from agent.work_items import WorkItemContext, WorkItemReader
from pbi.__main__ import estimated_tokens, finish, main
from pbi.generate_cases import analyze, write_cases
from pbi.mask import leaks, mask_text, write_masked_pack
from pbi.revalidate import write_revalidation
from tests.test_work_items import FakeClient, settings


SANDBOX = Path(tempfile.mkdtemp(prefix="qa-avianca-"))


class LocateTests(unittest.TestCase):
    def test_empieza_por_integration(self):
        item = {
            "id": 94,
            "rev": 2,
            "fields": {
                "System.TeamProject": "Integration",
                "System.Title": "Ejemplo",
                "System.WorkItemType": "Product Backlog Item",
                "System.State": "QA",
            },
            "relations": [],
        }
        client = FakeClient({"$expand=relations": item})
        found = WorkItemReader(settings(), client).locate(94)
        self.assertEqual(found, "Integration")
        self.assertTrue(any("Integration" in call for call in client.calls))
        self.assertFalse(any("/_apis/projects?" in call for call in client.calls))

    def test_si_no_esta_en_integration_recorre_el_resto(self):
        class Catalogo(FakeClient):
            def get_json(self, url: str) -> dict:
                self.calls.append(url)
                if "/_apis/projects?" in url:
                    return {"value": [{"name": "Integration"}, {"name": "DigitalChannels"}]}
                if "/Integration/" in url:
                    raise AzureReadError(404, "http_404", "No se encontró el Work Item en el proyecto configurado.")
                if "/DigitalChannels/" in url:
                    return {
                        "id": 94,
                        "fields": {"System.TeamProject": "DigitalChannels", "System.Title": "Otro"},
                        "relations": [],
                    }
                raise AzureReadError(404, "http_404", "No se encontró el Work Item en el proyecto configurado.")

        client = Catalogo({})
        found = WorkItemReader(settings(), client).locate(94)
        self.assertEqual(found, "DigitalChannels")

    def test_revalidacion_no_toca_los_casos(self):
        root = SANDBOX
        cases = root / "test-cases" / "PBI-94" / "casos-de-prueba.md"
        cases.parent.mkdir(parents=True, exist_ok=True)
        original = "| 1 | PBI-94 #TC ejemplo | paso | esperado | Aún no está ejecutado. |\n"
        cases.write_text(original, encoding="utf-8")
        context = WorkItemContext(
            source={"organization": "aviancavsts", "project": "Integration", "work_item_id": 94, "url": "", "revision": 1},
            metadata={"title": "t", "type": "Incident", "status": "QA", "area": "", "iteration": "", "tags": ""},
            requirements={"description": "dato", "acceptance_criteria": "", "acceptance_field": None, "custom_fields": {}, "evidence_ids": {"description": "AZDO-WI-94:DESC", "acceptance_criteria": "AZDO-WI-94:AC"}},
            discussions=[{"id": 1, "text": "comentario", "note": "Un comentario no es un criterio de aceptación."}],
            manuals=[{"path": "base_conocimiento/manual-aplicacion-sr.md", "status": "presente"}],
            warnings={"missing_requirements": [], "inaccessible_resources": []},
        )
        report = write_revalidation(context, root)
        self.assertEqual(cases.read_text(encoding="utf-8"), original)
        text = report.read_text(encoding="utf-8")
        self.assertIn("PBI-94 #TC ejemplo", text)
        self.assertIn("No se inventan", text)
        self.assertFalse((root / "test-cases" / "PBI-94" / "PBI-94-casos-de-prueba.xlsx").exists())

    def test_el_envio_no_conserva_datos_originales(self):
        raw = (
            'Tiquete 1342159456425 PNR C8OSGA correo qa.prueba@ejemplo.com '
            'cuenta 4162034938 37182088 >> C8OSGA >>1342159456425 {"firstName": "Oracio"}'
        )
        masked, mapping = mask_text(raw)
        self.assertEqual(leaks(masked, mapping), [])
        self.assertNotIn("1342159456425", masked)
        self.assertNotIn("C8OSGA", masked)
        self.assertNotIn("qa.prueba@ejemplo.com", masked)
        self.assertNotIn("4162034938", masked)
        self.assertNotIn("Oracio", masked)
        self.assertIn("TKT-", masked)
        self.assertIn("PNR-", masked)
        root = SANDBOX
        context = WorkItemContext(
            source={"organization": "aviancavsts", "project": "Integration", "work_item_id": 502, "url": "", "revision": 1},
            metadata={"title": "Ejemplo", "type": "Incident", "status": "QA", "area": "", "iteration": "", "tags": ""},
            requirements={
                "description": raw,
                "acceptance_criteria": "",
                "acceptance_field": None,
                "custom_fields": {},
                "evidence_ids": {"description": "AZDO-WI-502:DESC", "acceptance_criteria": "AZDO-WI-502:AC"},
            },
            manuals=[{"path": "base_conocimiento/lineamientos-qa.md", "status": "presente"}],
            warnings={"missing_requirements": [], "inaccessible_resources": []},
        )
        path = write_masked_pack(context, root)
        sent = path.read_text(encoding="utf-8")
        self.assertNotIn("1342159456425", sent)
        self.assertNotIn("Oracio", sent)
        report = (path.parent / "mascara_reporte.md").read_text(encoding="utf-8")
        self.assertNotIn("1342159456425", report)
        self.assertIn("Elegible para análisis de IA: sí", report)

    def test_rechaza_texto_en_lugar_de_numero(self):
        self.assertEqual(main(["abc"]), 1)

    def test_la_estimacion_de_tokens_no_inventa_un_consumo(self):
        self.assertEqual(estimated_tokens(""), 0)
        self.assertEqual(estimated_tokens("abcd"), 1)
        self.assertEqual(estimated_tokens("abcde"), 2)


def _context(work_id: int, description: str, comment: str = "", attachment: str = "") -> WorkItemContext:
    attachments = []
    if attachment:
        attachments.append({"filename": "log.csv", "extension": ".csv", "status": "extraido", "text": attachment})
    return WorkItemContext(
        source={"organization": "aviancavsts", "project": "Integration", "work_item_id": work_id, "url": "", "revision": 1},
        metadata={"title": "Load Massive", "type": "Incident", "status": "QA", "area": "", "iteration": "", "tags": ""},
        requirements={
            "description": description,
            "acceptance_criteria": "",
            "acceptance_field": None,
            "custom_fields": {},
            "evidence_ids": {"description": f"AZDO-WI-{work_id}:DESC", "acceptance_criteria": f"AZDO-WI-{work_id}:AC"},
        },
        discussions=[{"id": 1, "text": comment, "note": "Un comentario no es un criterio de aceptación."}] if comment else [],
        attachments={"extracted_documents": attachments},
        manuals=[
            {"path": "base_conocimiento/lineamientos-qa.md", "status": "presente"},
            {"path": "base_conocimiento/manual-aplicacion-avr.md", "status": "presente"},
            {"path": "base_conocimiento/manual-aplicacion-pi.md", "status": "presente"},
            {"path": "base_conocimiento/manual-aplicacion-ror.md", "status": "presente"},
            {"path": "base_conocimiento/manual-aplicacion-sr.md", "status": "presente"},
        ],
        warnings={"missing_requirements": [], "inaccessible_resources": []},
    )


class CaseFolderTests(unittest.TestCase):
    def test_el_comando_deja_la_carpeta_y_no_usa_el_comentario_ni_el_log(self):
        root = SANDBOX
        context = _context(
            503,
            "De los tres tiquetes solo debe continuar uno. Los otros dos quedan en failed porque estan inprogress.",
            comment="COMENTARIO-UNICO-NO-CASO",
            attachment="filas_datos: 10 Camel (camel-1) ERROR wk-refund no debe insertar este log",
        )
        from io import StringIO
        from contextlib import redirect_stdout

        folder = root / "test-cases" / "PBI-503"
        markdown = folder / "casos-de-prueba.md"
        workbook = folder / "PBI-503-casos-de-prueba.xlsx"
        if markdown.exists():
            markdown.unlink()
        if workbook.exists():
            workbook.unlink()
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = finish(context, root)
        output = buffer.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("paso 1 lectura del PBI: cumplido", output)
        self.assertIn("paso 2 documentos adjuntos: cumplido", output)
        self.assertIn("paso 4 base de conocimiento: cumplido", output)
        self.assertIn("paso 6 casos de prueba: cumplido", output)
        self.assertIn("paso 8 consumo de tokens: cumplido", output)
        self.assertIn("Proceso completo", output)
        self.assertIn("pasos cumplidos: 8", output)
        self.assertNotIn("Proceso incompleto", output)
        self.assertIn("validación: máscara elegible", output)
        self.assertIn("comentarios 1 sin criterio", output)
        self.assertIn("excel no generado", output)
        self.assertIn("tokens usados: 0", output)
        self.assertIn("tokens estimados de la ejecución:", output)
        text = markdown.read_text(encoding="utf-8")
        self.assertIn("PBI-503 #TC", text)
        self.assertNotIn("COMENTARIO-UNICO-NO-CASO", text)
        self.assertNotIn("filas_datos", text)
        self.assertFalse(workbook.is_file())

    def test_un_relato_sin_la_palabra_debe_no_bloquea(self):
        from io import StringIO
        from contextlib import redirect_stdout

        root = SANDBOX
        description = (
            "Se ajusta la pantalla de soporte para mostrar el estado de la solicitud "
            "cuando el analista consulta el caso en QA y guarda la evidencia."
        )
        context = _context(509, description)
        markdown = root / "test-cases" / "PBI-509" / "casos-de-prueba.md"
        if markdown.exists():
            markdown.unlink()
        titles, error = analyze(context)
        self.assertEqual(error, "")
        self.assertTrue(titles)
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = finish(context, root)
        self.assertEqual(code, 0)
        self.assertIn("Proceso completo", buffer.getvalue())
        self.assertNotIn("falló — el PBI no nombra un comportamiento verificable", buffer.getvalue())

    def test_los_atajos_leen_el_numero(self):
        from pbi.atajos import markdown_de, work_item_id

        self.assertEqual(work_item_id(["PBI", "1330194"]), "1330194")
        self.assertEqual(work_item_id(["doc", "PBI", "1365790"]), "1365790")
        self.assertEqual(work_item_id(["1330194"]), "1330194")
        from agent.layout import excel_drive

        self.assertEqual(excel_drive("1330194", Path("C:/casos")).name, "PBI-1330194.xlsx")
        self.assertTrue(str(markdown_de("1365790")).endswith("test-cases\\PBI-1365790\\casos-de-prueba.md") or str(markdown_de("1365790")).endswith("test-cases/PBI-1365790/casos-de-prueba.md"))

    def test_valores_faltantes_no_corta_la_frase(self):
        description = (
            "Cuando desde la pantalla ACM se tengan registros con el check de Valores Faltantes, "
            "el sistema deberá identificar su origen. "
            "Finalizar: Actualizar el estado a F en la PIC_PAYMENT_REQUEST_VF y se inserta el registro "
            "en PIC_PAYMENT_DETAIL_VF. Razon: Finalizado. "
            "Guardar: Se actualiza el IATA y el estado a V en la PIC_PAYMENT_REQUEST_VF y se inserta "
            "el registro en V en PIC_PAYMENT_DETAIL_VF."
        )
        acceptance = (
            "que se selecciona un registro desde la pantalla ACM y este corresponde al\n"
            "módulo de Valores Faltantes, identificado de acuerdo con la lógica."
        )
        context = _context(510, description)
        context.requirements["acceptance_criteria"] = acceptance
        root = SANDBOX
        markdown = root / "test-cases" / "PBI-510" / "casos-de-prueba.md"
        if markdown.exists():
            markdown.unlink()
        write_cases(context, root)
        text = markdown.read_text(encoding="utf-8")
        self.assertNotIn("corresponde al", text)
        self.assertIn("estado V", text)
        self.assertIn("razón Finalizado", text)
        self.assertIn("PIC_PAYMENT_REQUEST_VF", text)
        self.assertIn("## Matriz de riesgos", text)

    def test_sin_adjunto_avanza(self):
        from io import StringIO
        from contextlib import redirect_stdout

        root = SANDBOX
        context = _context(508, "El flujo debe continuar al paso 17 e insertar en AVRefund.")
        markdown = root / "test-cases" / "PBI-508" / "casos-de-prueba.md"
        if markdown.exists():
            markdown.unlink()
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = finish(context, root)
        output = buffer.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("adjuntos leídos: 0", output)
        self.assertIn("manuales revalidados: 5", output)
        self.assertIn("commits leídos: 0", output)
        self.assertIn("wiki leídas: 0", output)
        self.assertIn("paso 2 documentos adjuntos: cumplido — no se encontraron. Se continúa.", output)
        self.assertIn("No se encontraron enlaces de código. Se continúa.", output)
        self.assertIn("Proceso completo", output)

    def test_el_ultimo_commit_pesa_mas(self):
        from agent.code_changes import collect_code_changes, parse_git_link, parse_wiki_link

        parsed = parse_git_link("vstfs:///Git/PullRequestId/proj%2Frepo%2F15")
        self.assertEqual(parsed["kind"], "pr")
        self.assertEqual(parsed["pr"], "15")
        self.assertIsNone(parse_git_link(""))

        class Client:
            def get_json(self, url: str) -> dict:
                if "/pullRequests/" in url:
                    return {
                        "value": [
                            {"commitId": "aaa1111", "comment": "primero", "author": {"date": "2026-01-01T00:00:00Z"}},
                            {"commitId": "bbb2222", "comment": "ultimo cambio", "author": {"date": "2026-02-01T00:00:00Z"}},
                        ]
                    }
                if "/commits/bbb2222/changes" in url:
                    return {"changes": [{"item": {"path": "/src/Refund.cs"}}]}
                if "/commits/aaa1111/changes" in url:
                    return {"changes": [{"item": {"path": "/src/Viejo.cs"}}]}
                return {}

        result = collect_code_changes(Client(), "aviancavsts", [{"url": "vstfs:///Git/PullRequestId/proj%2Frepo%2F15"}])
        self.assertEqual(result["last"]["commit_id"], "bbb2222")
        self.assertEqual(result["last"]["peso"], "ultimo")
        self.assertEqual(result["last"]["paths"], ["/src/Refund.cs"])
        self.assertEqual(result["commits_read"], 2)
        self.assertEqual(result["wiki_read"], 0)
        self.assertEqual(result["previous"][0]["peso"], "anterior")
        hidden = collect_code_changes(Client(), "aviancavsts", [{"url": ""}])
        self.assertEqual(hidden["status"], "sin_enlaces")
        self.assertEqual(hidden["commits_read"], 0)
        self.assertEqual(hidden["wiki_read"], 0)
        wiki = parse_wiki_link("vstfs:///Wiki/WikiPage/proj%2Fwiki-soporte%2F12")
        self.assertEqual(wiki["page"], "12")

    def test_si_no_se_lee_el_pbi_el_paso_falla(self):
        from io import StringIO
        from contextlib import redirect_stdout

        context = _context(506, "El flujo debe continuar al paso 17.")
        context.source["revision"] = None
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = finish(context, SANDBOX)
        output = buffer.getvalue()
        self.assertEqual(code, 1)
        self.assertIn("paso 1 lectura del PBI: falló — no se leyó el PBI", output)
        self.assertIn("Proceso incompleto", output)
        self.assertIn("tokens usados: 0", output)
        self.assertNotIn("Proceso completo", output)

    def test_si_faltan_manuales_el_paso_falla(self):
        from io import StringIO
        from contextlib import redirect_stdout

        context = _context(507, "El flujo debe continuar al paso 17 e insertar en AVRefund.", attachment="WB campo debe continuar")
        context.manuals = []
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = finish(context, SANDBOX)
        output = buffer.getvalue()
        self.assertEqual(code, 1)
        self.assertIn("paso 4 base de conocimiento: falló", output)
        self.assertIn("manual-aplicacion-sr.md", output)
        self.assertIn("Proceso incompleto", output)
        self.assertNotIn("Proceso completo", output)

    def test_no_copia_el_saludo_ni_el_tiquete(self):
        root = SANDBOX
        context = _context(
            505,
            "Hola buenos dias se reporta un error. "
            "En Validate Mozart de los tiquetes 1342159456425 solo puede continuar uno y los otros quedan en failed porque estan inprogress. "
            "getcandidate y updatemozart incluyen esos failed. "
            "El error debio continuar al paso 17 que es insertar en AVRefund y esos tiquetes no deben ser considerados.",
        )
        markdown = root / "test-cases" / "PBI-505" / "casos-de-prueba.md"
        if markdown.exists():
            markdown.unlink()
        write_cases(context, root)
        text = markdown.read_text(encoding="utf-8")
        self.assertNotIn("Hola buenos", text)
        self.assertNotIn("1342159456425", text)
        self.assertIn("getcandidate y updatemozart excluyen los failed", text)
        self.assertIn("AVRefund", text)

    def test_no_reescribe_casos_existentes(self):
        root = SANDBOX
        context = _context(504, "El flujo debe continuar al paso 17 e insertar en AVRefund.")
        markdown, _workbook = (
            root / "test-cases" / "PBI-504" / "casos-de-prueba.md",
            root / "test-cases" / "PBI-504" / "PBI-504-casos-de-prueba.xlsx",
        )
        markdown.parent.mkdir(parents=True, exist_ok=True)
        original = (
            "| # | Nombre del caso de prueba | Pasos | Resultado esperado | Resultado ejecución |\n"
            "|---|---|---|---|---|\n"
            "| 1 | PBI-504 #TC conservar | 1. Paso.<br>2. Otro. | Esperado propio. | Sin ejecutar. |\n"
        )
        markdown.write_text(original, encoding="utf-8")
        workbook = markdown.parent / "PBI-504-casos-de-prueba.xlsx"
        if workbook.exists():
            workbook.unlink()
        write_cases(context, root)
        self.assertEqual(markdown.read_text(encoding="utf-8"), original)
        self.assertFalse(workbook.is_file())


if __name__ == "__main__":
    unittest.main()
