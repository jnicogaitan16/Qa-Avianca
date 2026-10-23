"""Escribe el markdown de casos cuando la carpeta no existe. No genera el Excel."""

from __future__ import annotations

import re
from pathlib import Path

from agent.layout import reading_dir
from agent.work_items import WorkItemContext


_LOG = re.compile(r"filas_datos|Camel \(|lineas_error|ERROR wk-refund|ExceptionMessage", re.IGNORECASE)
_SKIP = re.compile(r"^(hola\b|buen[oa]s\b|se adjunta\b|caso a revisar\b|@)", re.IGNORECASE)
_BEHAVIOR = re.compile(
    r"\b(debe|deben|no debe|no deben|continúa|continua|continuar|no se|se incluye|incluyen|inserta|insertar|failed|inprogress)\b",
    re.IGNORECASE,
)
_TICKET = re.compile(r"\b\d{13}\b")
_EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
_ARROW_PNR = re.compile(r"(>>\s*)([A-Z0-9]{6})(\s*>>)")
_LABELED_PNR = re.compile(r"\b(PNR|pnr)\s+[A-Z0-9]{6}\b")


def case_paths(root: Path, work_id: int) -> tuple[Path, Path]:
    folder = root / "test-cases" / f"PBI-{work_id}"
    return folder / "casos-de-prueba.md", folder / f"PBI-{work_id}-casos-de-prueba.xlsx"


def analyze(context: WorkItemContext) -> tuple[list[str], str]:
    description = str((context.requirements or {}).get("description") or "")
    acceptance = str((context.requirements or {}).get("acceptance_criteria") or "")
    if not description.strip() and not acceptance.strip():
        return [], "no hay texto que analizar"
    cases = _cases(f"{description}\n{acceptance}", context)
    if len(cases) == 1 and str(cases[0]["expected"]).startswith("El Work Item no trae"):
        return [], "el PBI no nombra un comportamiento verificable"
    return [str(case["title"]) for case in cases], ""


def write_cases(context: WorkItemContext, root: Path) -> Path:
    work_id = int(context.source["work_item_id"])
    markdown, _workbook = case_paths(root, work_id)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    if not markdown.is_file():
        markdown.write_text(_document(context, root), encoding="utf-8")
    return markdown


def _document(context: WorkItemContext, root: Path) -> str:
    work_id = context.source["work_item_id"]
    title = _public(str(context.metadata.get("title") or "Sin título"))
    description = context.requirements.get("description") or ""
    acceptance = (context.requirements.get("acceptance_criteria") or "").strip()
    source = f"{description}\n{acceptance}"
    cases = _cases(source, context)
    commit_case = _commit_case(context)
    if commit_case and len(cases) < 10:
        cases.append(commit_case)
    rows = []
    for index, case in enumerate(cases, start=1):
        steps = "<br>".join(case["steps"])
        rows.append(
            f"| {index} | PBI-{work_id} #TC {_public(case['title'])} | {steps} | {_public(case['expected'])} | Sin ejecutar. |"
        )
    notes = _notes(root, source)
    gap = ""
    if not acceptance:
        gap = "\n\nNo hay criterios de aceptación en el Work Item. Un comentario no entra.\n"
    extra = "\n".join(f"- {note}" for note in notes)
    extra_block = f"\n{extra}\n" if extra else ""
    return f"""# PBI-{work_id} — Casos de prueba: {title}

- **Carpeta:** PBI-{work_id}
- **State:** Design
- **Related work:** {work_id}
- **Evidencias:** Con fecha y hora en cada ejecución. Ese resultado se escribe en este markdown.
- **Excel:** no se actualiza con este archivo. Sale solo cuando se pide la presentación.
- **Lectura de logs:** el comando no coteja el log. El caso de traza, si existe, queda para el pegado en el chat.

Los casos salen de los comportamientos nombrados en la descripción y en los criterios, cruzados con la base de conocimiento. Skills: qa-funcional, postman y validador-logs-capa-media. No se copia el saludo ni un comentario. No se llama a un modelo externo.{gap}{extra_block}
{_comparison_block(root, work_id)}
{_commit_block(context)}
## Casos

| # | Nombre del caso de prueba | Pasos | Resultado esperado | Resultado ejecución |
|---|---|---|---|---|
{chr(10).join(rows)}

## Matriz de riesgos

No se califica probabilidad ni impacto. `lineamientos-qa.md` y el manual general no traen esa fórmula. F-S-V mide un defecto ya observado, no este diseño.

{_risk_table(context, root, source, cases)}
"""


def _commit_case(context: WorkItemContext) -> dict[str, str | list[str]] | None:
    last = ((getattr(context, "code_changes", None) or {}).get("last")) or None
    if not last:
        return None
    paths = [str(path) for path in (last.get("paths") or [])[:8]]
    comment = str(last.get("comment") or "").strip()
    expected = comment or "El cambio queda en los archivos del último commit."
    if paths:
        expected = f"{expected} Archivos: {', '.join(paths)}."
    return {
        "title": "el último commit respalda el cambio",
        "steps": [
            "1. Tomar el último commit enlazado al PBI. Los commits anteriores pesan menos.",
            "2. Revisar el mensaje y los archivos de ese commit.",
            "3. Ejecutar el comportamiento que ese cambio toca. No reejecutar producción.",
            "4. Guardar la evidencia con fecha y hora.",
        ],
        "expected": expected,
        "risk": "El comportamiento probado no corresponde a los archivos del último commit.",
        "fuente": "Último commit enlazado al Work Item",
    }


def _commit_block(context: WorkItemContext) -> str:
    changes = getattr(context, "code_changes", None) or {}
    last = changes.get("last") or None
    if not last:
        return ""
    lines = [
        "## Último commit",
        "",
        "Este commit pesa más que los anteriores.",
        f"Fecha: {last.get('date') or 'sin fecha'}",
        "",
    ]
    if last.get("comment"):
        lines.extend([_public(str(last.get("comment"))), ""])
    for path in last.get("paths") or []:
        lines.append(f"- {_public(str(path))}")
    return "\n".join(lines) + "\n"


def _comparison_block(root: Path, work_id: int) -> str:
    path = reading_dir(root, int(work_id)) / "comparacion-base.md"
    if not path.is_file():
        return ""
    return "\n## Comparación con la base de conocimiento\n\n" + path.read_text(encoding="utf-8") + "\n"


def _cases(source: str, context: WorkItemContext) -> list[dict[str, str | list[str]]]:
    faltantes = _valores_faltantes(source)
    if faltantes:
        return faltantes
    found: list[dict[str, str | list[str]]] = []
    failed = re.search(r"failed|inprogress", source, re.IGNORECASE)
    if re.search(r"validate", source, re.IGNORECASE) or failed:
        found.append(
            {
                "title": "solo sigue el tiquete que el paso de validación deja continuar",
                "steps": [
                    "1. En QA, preparar una carga con los tiquetes del mismo caso. No reejecutar la solicitud de producción.",
                    "2. Llegar al paso de validación que la descripción nombra.",
                    "3. Guardar el resultado, con fecha y hora, identificando qué tiquete sigue y cuáles quedan en failed.",
                ],
                "expected": "Solo continúa el tiquete que la validación deja seguir. Los que están inprogress quedan en failed y no siguen en el proceso.",
                "risk": "Un tiquete en failed por inprogress sigue en el proceso.",
                "fuente": "Descripción del Work Item",
            }
        )
    if re.search(r"getcandidate|updatemozart", source, re.IGNORECASE):
        found.append(
            {
                "title": "getcandidate y updatemozart excluyen los failed",
                "steps": [
                    "1. Usar la misma carga del caso anterior.",
                    "2. Revisar getcandidate y anotar qué tiquetes incluye.",
                    "3. Revisar updatemozart y anotar qué tiquetes incluye.",
                    "4. Guardar ambos extractos con fecha y hora.",
                ],
                "expected": "getcandidate y updatemozart no incluyen los tiquetes que quedaron en failed.",
                "risk": "getcandidate o updatemozart incluyen tiquetes que ya estaban en failed.",
                "fuente": "Descripción del Work Item",
            }
        )
    if re.search(r"paso\s*17|AVRefund|AVrefund", source, re.IGNORECASE):
        found.append(
            {
                "title": "el error de actualización sigue a la inserción en AVRefund",
                "steps": [
                    "1. Provocar el error de actualización que la descripción relata.",
                    "2. Seguir la misma ejecución después de ese error.",
                    "3. Comprobar si el flujo llega a la inserción en AVRefund.",
                    "4. Guardar la evidencia con fecha y hora.",
                ],
                "expected": "Aunque la actualización falle, el flujo continúa a la inserción en AVRefund del tiquete que sí podía continuar. No se inventa el nombre de la tabla.",
                "risk": "El error de actualización no continúa a la inserción en AVRefund.",
                "fuente": "Descripción del Work Item",
            }
        )
    if re.search(r"no deben ser considerados", source, re.IGNORECASE) and re.search(r"AVRefund|AVrefund|insert", source, re.IGNORECASE):
        found.append(
            {
                "title": "los tiquetes en failed no se insertan",
                "steps": [
                    "1. En la misma ejecución de la inserción, revisar AVRefund.",
                    "2. Buscar los tiquetes que quedaron en failed.",
                    "3. Guardar la evidencia con fecha y hora.",
                ],
                "expected": "Los tiquetes en failed no se insertan. La descripción dice que no deben ser considerados en el proceso.",
                "risk": "Los tiquetes en failed se insertan en AVRefund.",
                "fuente": "Descripción del Work Item",
            }
        )
    if _log_names(context):
        found.append(
            {
                "title": "una traza de la ejecución muestra el error y lo que sigue",
                "steps": [
                    "1. Abrir el log del pod de la ejecución de QA, no la muestra suelta del adjunto.",
                    "2. Reunir una sola traza por su correlation id.",
                    "3. Ubicar el error que la descripción relata y lo que ocurre después.",
                    "4. Adjuntar la traza con fecha y hora. No completar un JSON cortado.",
                ],
                "expected": "La misma traza muestra el error y la continuación que el caso exige. Si el fragmento no cierra, el caso queda en revisión y no se declara Fail.",
                "risk": "Se use la muestra del adjunto como si fuera la traza de la ejecución.",
                "fuente": "Descripción del Work Item",
            }
        )
    if found:
        return found[:10]
    return _fallback(context)


def _fallback(context: WorkItemContext) -> list[dict[str, str | list[str]]]:
    acceptance = (context.requirements.get("acceptance_criteria") or "").strip()
    description = context.requirements.get("description") or ""
    source_name = "Criterios de aceptación del Work Item" if acceptance else "Descripción del Work Item"
    text = acceptance or description
    pieces = _keep(_sentences(text))
    if not pieces:
        pieces = [
            part
            for part in _sentences(text)
            if 25 <= len(part) <= 500 and not _SKIP.search(part) and not _LOG.search(part)
        ]
    if not pieces:
        pieces = ["El Work Item no trae un comportamiento verificable. No se inventa el resultado."]
    cases = []
    for piece in pieces[:10]:
        cases.append(
            {
                "title": _title(piece),
                "steps": [
                    "1. Preparar en QA el escenario del resultado esperado. No reejecutar una solicitud de producción.",
                    "2. Ejecutar ese comportamiento.",
                    "3. Guardar la evidencia con fecha y hora.",
                ],
                "expected": piece,
                "risk": piece,
                "fuente": source_name,
            }
        )
    return cases


def _risk_table(context: WorkItemContext, root: Path, source: str, cases: list[dict[str, str | list[str]]]) -> str:
    rows = [
        "| # | Riesgo citado | Fuente | Caso | Medición |",
        "|---|---|---|---|---|",
    ]
    for index, case in enumerate(cases, start=1):
        rows.append(
            f"| {index} | {_public(str(case['risk']))} | {case['fuente']} | {index} | Cubierto por el caso {index}. |"
        )
    next_id = len(cases) + 1
    if re.search(r"notificacion", source, re.IGNORECASE):
        insert_at = next((i for i, case in enumerate(cases, start=1) if "AVRefund" in str(case["expected"])), None)
        target = str(insert_at) if insert_at else "—"
        rows.append(
            f"| {next_id} | La descripción nombra las notificaciones como efecto de que no hubo inserción. | Descripción del Work Item | {target} | Síntoma. No se abre un caso aparte de notificación. |"
        )
        next_id += 1
    if not (context.requirements.get("acceptance_criteria") or "").strip():
        rows.append(
            f"| {next_id} | No hay criterios de aceptación en el Work Item. | Campo de criterios del Work Item | — | Hueco: el esperado sale del relato. |"
        )
        next_id += 1
    for name in _log_names(context):
        rows.append(
            f"| {next_id} | El adjunto {name} tiene forma de log. | Adjunto del Work Item | — | Fuera del cotejo de este comando. |"
        )
        next_id += 1
    for note in _notes(root, source):
        rows.append(f"| {next_id} | {_public(note)} | Manual o catálogo del proyecto | — | Hueco o contradicción. No se inventa el dato. |")
        next_id += 1
    return "\n".join(rows)


def _notes(root: Path, source: str) -> list[str]:
    notes = []
    if re.search(r"PIC_PAYMENT_REQUEST_VF", source):
        manual = root / "base_conocimiento" / "manual-aplicacion-pi.md"
        if manual.is_file():
            body = manual.read_text(encoding="utf-8")
            if "Se cancelan las acciones" in body:
                notes.append("El manual PI, sección 11.1.10, dice que Finalizar cancela las acciones. Para Valores Faltantes el oráculo es el estado F del PBI.")
            if "MST_IATA_ACM" in body and "MST_IATA_ACM" not in source:
                notes.append("El manual exige IATA activo en MST_IATA_ACM para Guardar. El PBI no lo repite en el flujo VF.")
    if re.search(r"load\s*massive|loadmassive", source, re.IGNORECASE):
        catalog = root / "docs" / "proyectos" / "apis-por-modulo.md"
        if catalog.is_file():
            line = next((item for item in catalog.read_text(encoding="utf-8").splitlines() if "Load Massive Refund Request" in item), "")
            if line and "http" not in line.lower():
                notes.append("La fila Load Massive Refund Request del catálogo no trae URL. No se arma request.")
            if "wk-refund-orchloadmassiverefund" in line:
                notes.append("El pod de esa fila es wk-refund-orchloadmassiverefund, proyecto ssf-npci-refund.")
    if re.search(r"avrefund", source, re.IGNORECASE):
        manual = root / "base_conocimiento" / "manual-aplicacion-avr.md"
        if manual.is_file() and not re.search(r"avrefund", manual.read_text(encoding="utf-8"), re.IGNORECASE):
            notes.append("El manual AVR no contiene el nombre AVRefund. No se inventa la tabla.")
    if re.search(r"load\s*massive|loadmassive", source, re.IGNORECASE):
        sr = root / "base_conocimiento" / "manual-aplicacion-sr.md"
        if sr.is_file():
            body = sr.read_text(encoding="utf-8")
            if "E = Reintento" in body and "cambia su estado a E" in body:
                notes.append("El manual SR trata el estado E como fallo en el relato del cargue y como Reintento en la sección 7.2.3.1. No se usa como el failed de la descripción.")
    return notes


def _log_names(context: WorkItemContext) -> list[str]:
    names = []
    for item in context.attachments.get("extracted_documents") or []:
        text = str(item.get("text") or "")
        if _LOG.search(text[:2000]):
            names.append(_public(str(item.get("filename") or "adjunto")))
    return names


def _valores_faltantes(source: str) -> list[dict[str, str | list[str]]]:
    if not re.search(r"PIC_PAYMENT_REQUEST_VF", source) or not re.search(r"PIC_PAYMENT_DETAIL_VF", source):
        return []
    if not re.search(r"guardar", source, re.IGNORECASE) or not re.search(r"finalizar", source, re.IGNORECASE):
        return []
    cases: list[dict[str, str | list[str]]] = [
        {
            "title": "el check de Valores Faltantes elige las tablas VF",
            "steps": [
                "1. En QA, abrir Procesos >> Gestión de pago ACM.",
                "2. Elegir un registro que la pantalla marque con el check de Valores Faltantes. No reejecutar una solicitud de producción.",
                "3. Confirmar que ese registro está en [rfd].[PIC_PAYMENT_REQUEST_VF] o [rfd].[PIC_PAYMENT_DETAIL_VF].",
                "4. Guardar la evidencia con fecha y hora, antes de pulsar Guardar o Finalizar.",
            ],
            "expected": "El registro con el check se trata como Valores Faltantes y el origen de la gestión son PIC_PAYMENT_REQUEST_VF y PIC_PAYMENT_DETAIL_VF. La regla interna del check está citada en el PBI 1299106 y no se inventa aquí.",
            "risk": "Un registro con check de Valores Faltantes se actualiza en PIC_PAYMENT_REQUEST o PIC_PAYMENT_DETAIL.",
            "fuente": "Descripción del Work Item",
        },
        {
            "title": "Guardar actualiza el IATA y deja estado V en las tablas VF",
            "steps": [
                "1. Partir del registro del caso 1.",
                "2. Informar el IATA y pulsar Guardar.",
                "3. Consultar [rfd].[PIC_PAYMENT_REQUEST_VF] y [rfd].[PIC_PAYMENT_DETAIL_VF] de ese mismo registro.",
                "4. Guardar la evidencia con fecha y hora. No consultar solo PIC_PAYMENT_REQUEST ni PIC_PAYMENT_DETAIL.",
            ],
            "expected": "En PIC_PAYMENT_REQUEST_VF quedan actualizados el IATA y el estado V. En PIC_PAYMENT_DETAIL_VF se inserta el registro en estado V. El PBI no nombra la razón de ese insert ni el mensaje de confirmación en pantalla.",
            "risk": "Guardar no deja el IATA y el estado V en PIC_PAYMENT_REQUEST_VF, o no inserta el estado V en PIC_PAYMENT_DETAIL_VF.",
            "fuente": "Descripción del Work Item",
        },
        {
            "title": "Finalizar deja estado F y la razón Finalizado en las tablas VF",
            "steps": [
                "1. Partir de otro registro con el check de Valores Faltantes.",
                "2. Pulsar Finalizar.",
                "3. Consultar [rfd].[PIC_PAYMENT_REQUEST_VF] y [rfd].[PIC_PAYMENT_DETAIL_VF] de ese mismo registro.",
                "4. Guardar la evidencia con fecha y hora.",
            ],
            "expected": "PIC_PAYMENT_REQUEST_VF queda en estado F. PIC_PAYMENT_DETAIL_VF recibe el insert en estado F con razón Finalizado. No se espera que Finalizar cancele la edición: eso lo dice el manual para la pantalla que no es Valores Faltantes.",
            "risk": "Finalizar no deja el estado F ni la razón Finalizado en las tablas VF.",
            "fuente": "Descripción del Work Item",
        },
        {
            "title": "un registro sin el check no escribe las tablas VF",
            "steps": [
                "1. En la misma pantalla, elegir un registro que no tenga el check de Valores Faltantes.",
                "2. Pulsar Guardar o Finalizar, según lo que la pantalla permita en ese registro.",
                "3. Consultar [rfd].[PIC_PAYMENT_REQUEST_VF] y [rfd].[PIC_PAYMENT_DETAIL_VF].",
                "4. Guardar la evidencia con fecha y hora.",
            ],
            "expected": "Esas dos tablas VF no cambian por ese registro. El PBI exige identificar el origen y operar la tabla que corresponda.",
            "risk": "Un registro sin el check escribe las tablas VF.",
            "fuente": "Descripción del Work Item",
        },
    ]
    return cases


def _sentences(text: str) -> list[str]:
    joined: list[str] = []
    buffer = ""
    for part in _pieces(text):
        if not part:
            continue
        buffer = f"{buffer} {part}".strip() if buffer else part
        if buffer[-1:] in ".!?":
            joined.append(buffer)
            buffer = ""
    return joined


def _pieces(text: str) -> list[str]:
    text = text.replace("\r", "\n")
    parts = re.split(r"\n+|(?<=[.!?])\s+|(?=\b\d+\.\s)", text)
    cleaned = [re.sub(r"\s+", " ", part).strip(" -*") for part in parts]
    sized: list[str] = []
    for part in cleaned:
        if len(part) <= 500:
            sized.append(part)
            continue
        words = part.split()
        chunk: list[str] = []
        length = 0
        for word in words:
            if chunk and length + len(word) > 400:
                sized.append(" ".join(chunk))
                chunk = [word]
                length = len(word)
            else:
                chunk.append(word)
                length += len(word) + 1
        if chunk:
            sized.append(" ".join(chunk))
    return sized


def _readable(parts: list[str]) -> list[str]:
    return [
        part
        for part in parts
        if 25 <= len(part) <= 500 and not _SKIP.search(part) and not _LOG.search(part)
    ]


def _keep(parts: list[str]) -> list[str]:
    kept = []
    for part in parts:
        if len(part) < 25 or len(part) > 500 or _SKIP.search(part) or _LOG.search(part):
            continue
        if not _BEHAVIOR.search(part):
            continue
        kept.append(part)
    return kept


def _title(text: str) -> str:
    words = re.sub(r"[^\wÁÉÍÓÚÜÑáéíóúüñ]+", " ", _public(text)).split()
    return " ".join(words[:12]).strip()[:80] or "escenario"


def _public(text: str) -> str:
    text = _EMAIL.sub("el correo", text)
    text = _TICKET.sub("el tiquete", text)
    text = _ARROW_PNR.sub(lambda match: f"{match.group(1)}el PNR{match.group(3)}", text)
    text = _LABELED_PNR.sub("el PNR", text)
    return text.replace("|", "/").replace("\n", " ").strip()
