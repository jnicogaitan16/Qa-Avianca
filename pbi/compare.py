"""Lee la base de conocimiento y la compara con el texto del PBI."""

from __future__ import annotations

import re
from pathlib import Path

from agent.work_items import WorkItemContext


MANUALS = (
    "base_conocimiento/lineamientos-qa.md",
    "base_conocimiento/manual-aplicacion-avr.md",
    "base_conocimiento/manual-aplicacion-pi.md",
    "base_conocimiento/manual-aplicacion-ror.md",
    "base_conocimiento/manual-aplicacion-sr.md",
)

_TERMS = (
    ("Load Massive", r"load\s*massive|loadmassive"),
    ("AVRefund", r"avrefund"),
    ("Mozart", r"mozart"),
    ("getcandidate", r"getcandidate"),
    ("updatemozart", r"updatemozart"),
    ("inprogress", r"inprogress"),
    ("failed", r"\bfailed\b"),
    ("notificación", r"notificacion"),
)


def compare_knowledge(context: WorkItemContext, repo: Path) -> tuple[str, int, str]:
    present = {item.get("path") for item in context.manuals if item.get("status") == "presente"}
    missing = [path for path in MANUALS if path not in present]
    if missing:
        return "", 0, "no se revalidó " + ", ".join(missing)
    bodies: dict[str, str] = {}
    read_chars = 0
    unread = []
    for path in MANUALS:
        file = repo / path
        if not file.is_file():
            unread.append(path)
            continue
        text = file.read_text(encoding="utf-8")
        bodies[path] = text
        read_chars += len(text)
    if unread:
        return "", read_chars, "no se pudo leer " + ", ".join(unread)
    source = "\n".join(
        [
            str((context.requirements or {}).get("description") or ""),
            str((context.requirements or {}).get("acceptance_criteria") or ""),
        ]
    )
    read_chars += len(source)
    rows = [
        "| Término del PBI | Dónde se buscó | Resultado |",
        "|---|---|---|",
    ]
    for label, pattern in _TERMS:
        if not re.search(pattern, source, re.IGNORECASE):
            continue
        hits = [path for path, body in bodies.items() if re.search(pattern, body, re.IGNORECASE)]
        if hits:
            rows.append(f"| {label} | {hits[0]} | Encontrado |")
        else:
            rows.append(f"| {label} | base_conocimiento/ | No está en la base |")
    if len(rows) == 2:
        rows.append("| — | base_conocimiento/ | El PBI no usa términos de esa lista |")
    body = "\n".join(rows) + "\n"
    return body, read_chars, ""
