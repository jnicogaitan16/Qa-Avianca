"""Instala dependencias del lector de Work Items si QA_INSTALL_DEPS=true.

No lee ni imprime el PAT. No instala openpyxl: el Excel de casos no lo usa.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent.config import load_dotenv  # noqa: E402


def _venv_python() -> Path:
    candidate = ROOT / ".venv" / "Scripts" / "python.exe"
    if candidate.is_file():
        return candidate
    created = subprocess.run([sys.executable, "-m", "venv", str(ROOT / ".venv")], check=False)
    if created.returncode != 0 or not candidate.is_file():
        raise SystemExit("No se pudo crear .venv")
    return candidate


def main() -> int:
    load_dotenv(ROOT / ".env")
    import os

    if os.environ.get("QA_INSTALL_DEPS", "").strip().lower() not in {"1", "true", "yes", "si", "sí"}:
        print("QA_INSTALL_DEPS no está activo. No se instala nada.")
        return 0
    python = _venv_python()
    destino = python.parent
    for nombre in ("corre.cmd", "genera.cmd"):
        origen = ROOT / "scripts" / nombre
        if origen.is_file():
            (destino / nombre).write_bytes(origen.read_bytes())
    req = ROOT / "requirements-workitems.txt"
    print("Instalando requirements-workitems.txt en .venv")
    completed = subprocess.run(
        [str(python), "-m", "pip", "install", "-r", str(req)],
        check=False,
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
