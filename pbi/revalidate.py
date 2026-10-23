"""Revalidación escéptica. No reescribe casos ni el Excel."""

from __future__ import annotations

import re
from pathlib import Path

from agent.layout import reading_dir
from agent.work_items import WorkItemContext


def write_revalidation(context: WorkItemContext, root: Path) -> Path:
    work_id = context.source["work_item_id"]
    folder = reading_dir(root, int(work_id))
    folder.mkdir(parents=True, exist_ok=True)
    cases_path = root / "test-cases" / f"PBI-{work_id}" / "casos-de-prueba.md"
    lines = [
        f"# Revalidación WI {work_id}",
        "",
        "Los comentarios no son criterios de aceptación. Los manuales se releyeron antes de esta nota.",
        "Si no había markdown de casos, el comando lo escribe desde los comportamientos del requisito. No reescribe un archivo ya existente. No lee logs. Un comentario no entra.",
        "",
        "## Manuales",
        "",
    ]
    for manual in context.manuals:
        lines.append(f"- {manual.get('path')} ({manual.get('status')})")
    lines.extend(["", "## Work Item", ""])
    lines.append(f"- Proyecto: {context.source.get('project')}")
    lines.append(f"- Revisión: {context.source.get('revision')}")
    lines.append(f"- Tipo: {context.metadata.get('type')}")
    lines.append(f"- Estado: {context.metadata.get('status')}")
    acceptance = (context.requirements.get("acceptance_criteria") or "").strip()
    if acceptance:
        lines.append("- Criterios de aceptación: presentes en el Work Item.")
    else:
        lines.append("- Criterios de aceptación: no están en el Work Item. No se inventan.")
    lines.append(f"- Comentarios leídos: {len(context.discussions)}. No pasan a criterio.")
    lines.extend(["", "## Casos locales", ""])
    if not cases_path.is_file():
        lines.append("No hay `casos-de-prueba.md` local. No hay nada que actualizar.")
    else:
        text = cases_path.read_text(encoding="utf-8")
        names = re.findall(r"\|\s*\d+\s*\|\s*(PBI-\d+\s+#TC[^|]+)\|", text)
        lines.append(f"Archivo presente: `{cases_path.relative_to(root).as_posix()}`")
        lines.append(f"Casos encontrados: {len(names)}")
        for name in names:
            lines.append(f"- {name.strip()}")
        if not acceptance:
            lines.append("")
            lines.append("Hueco: el Work Item no trae criterios. Los esperados de los casos tienen que citar el relato, el PBI relacionado o el manual, no un comentario.")
        lines.append("")
        lines.append("Actualización aplicada: Context Pack. Los casos quedan como están hasta una revisión humana.")
    target = folder / "QA_Revalidacion.md"
    target.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    return target
