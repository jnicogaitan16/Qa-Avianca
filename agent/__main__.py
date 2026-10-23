"""Cliente interno de lectura. El comando de uso es python -m pbi <id>."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from agent.azure_client import AzureReadClient, AzureReadError
from agent.config import load_settings
from agent.context_pack import write_context_pack
from agent.work_items import WorkItemReader


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m agent")
    sub = parser.add_subparsers(dest="command", required=True)
    work = sub.add_parser("work-item")
    work_sub = work.add_subparsers(dest="action", required=True)
    for name in ("fetch", "analyze"):
        cmd = work_sub.add_parser(name)
        cmd.add_argument("ref")
        if name == "analyze":
            cmd.add_argument("--no-llm", action="store_true")
    args = parser.parse_args(argv)
    settings = load_settings(ROOT)
    use_llm = settings.llm_enabled and not getattr(args, "no_llm", False)
    if use_llm:
        print("AZDO_WI_LLM_ENABLED=true, pero no hay proveedor autorizado. Se genera el Context Pack sin llamada externa.")
        use_llm = False
    try:
        reader = WorkItemReader(settings, AzureReadClient(settings))
        context = reader.fetch(args.ref, ROOT)
        folder = write_context_pack(context, ROOT, llm_enabled=use_llm)
    except AzureReadError as exc:
        print(str(exc))
        return 1
    print(f"Work Item {context.source['work_item_id']} rev {context.source['revision']}")
    print(f"Proyecto {context.source['project']} | {context.metadata.get('type')} | {context.metadata.get('status')}")
    print(f"Manuales {len(context.manuals)} | comentarios {len(context.discussions)} | adjuntos extraídos {len(context.attachments['extracted_documents'])}")
    print(f"Salida {folder.relative_to(ROOT).as_posix()}")
    if args.action == "fetch":
        print("fetch: lectura y Context Pack. No se redactan casos ni se genera el Excel.")
    else:
        print("analyze: Context Pack y prompt_ready.md. Los casos siguen en casos-de-prueba.md y exportar_casos.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
