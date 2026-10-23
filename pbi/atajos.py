"""Atajos de la terminal. No cambian la lectura ni el Excel: solo arman la llamada."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def work_item_id(args: list[str]) -> str:
    tokens = [arg for arg in args if arg.lower() not in {"pbi", "doc"}]
    if len(tokens) != 1 or not tokens[0].isdigit():
        raise SystemExit("Uso: Corre PBI 1330194    o    Genera doc PBI 1330194")
    return tokens[0]


def markdown_de(work_id: str) -> Path:
    return ROOT / "test-cases" / f"PBI-{work_id}" / "casos-de-prueba.md"


def main(argv: list[str] | None = None) -> int:
    argumentos = list(sys.argv[1:] if argv is None else argv)
    if not argumentos or argumentos[0].lower() not in {"corre", "genera"}:
        raise SystemExit("Uso: Corre PBI 1330194    o    Genera doc PBI 1330194")
    accion = argumentos[0].lower()
    work_id = work_item_id(argumentos[1:])
    if accion == "corre":
        sys.argv = ["pbi", work_id]
        from pbi.__main__ import main as leer

        return leer()
    markdown = markdown_de(work_id)
    if not markdown.is_file():
        print(f"No está el markdown {markdown.relative_to(ROOT)}")
        return 1
    spec = importlib.util.spec_from_file_location("exportar_casos", ROOT / "scripts" / "exportar_casos.py")
    module = importlib.util.module_from_spec(spec)
    from agent.layout import excel_drive

    try:
        salida = excel_drive(work_id)
    except FileNotFoundError:
        print("No está la carpeta de OneDrive QA nico/Test cases. No se escribió el Excel en el proyecto.")
        return 1
    spec.loader.exec_module(module)
    sys.argv = ["exportar_casos.py", str(markdown), "-o", str(salida)]
    module.main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
