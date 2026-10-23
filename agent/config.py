"""Configuración de Work Items. El PAT no se imprime ni se copia a otro nombre."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def load_dotenv(path: Path) -> None:
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def _flag(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    return raw.strip().lower() in {"1", "true", "yes", "si", "sí"}


def _int(name: str, default: int) -> int:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    return int(raw)


@dataclass(frozen=True)
class Settings:
    org: str
    project: str
    pat_var: str
    token: str
    enabled: bool
    include_attachments: bool
    max_attachment_bytes: int
    max_total_attachment_bytes: int
    max_related_depth: int
    max_comments: int
    max_extract_chars: int
    llm_enabled: bool
    keep_raw: bool

    @property
    def allowed_hosts(self) -> frozenset[str]:
        return frozenset(
            {
                "dev.azure.com",
                f"{self.org}.visualstudio.com",
                "vsrm.dev.azure.com",
            }
        )


def load_settings(root: Path | None = None) -> Settings:
    root = root or Path(__file__).resolve().parents[1]
    load_dotenv(root / ".env")
    pat_var = os.environ.get("AZDO_WI_PAT_VAR", "TOKEN-AZURE").strip() or "TOKEN-AZURE"
    if pat_var != "TOKEN-AZURE" and "PAT" in pat_var.upper() and os.environ.get(pat_var) and os.environ.get("TOKEN-AZURE"):
        # Dos secretos distintos solo se usan si la variable apunta explícitamente a uno.
        pass
    return Settings(
        org=os.environ.get("AZDO_WI_ORG", "aviancavsts").strip() or "aviancavsts",
        project=os.environ.get("AZDO_WI_PROJECT", "Integration").strip() or "Integration",
        pat_var=pat_var,
        token=os.environ.get(pat_var, ""),
        enabled=_flag("AZDO_WI_ENABLED", True),
        include_attachments=_flag("AZDO_WI_INCLUDE_ATTACHMENTS", True),
        max_attachment_bytes=_int("AZDO_WI_MAX_ATTACHMENT_MB", 25) * 1024 * 1024,
        max_total_attachment_bytes=_int("AZDO_WI_MAX_TOTAL_ATTACHMENTS_MB", 100) * 1024 * 1024,
        max_related_depth=_int("AZDO_WI_MAX_RELATED_DEPTH", 1),
        max_comments=_int("AZDO_WI_MAX_COMMENTS", 200),
        max_extract_chars=_int("AZDO_WI_MAX_EXTRACT_CHARS", 20000),
        llm_enabled=_flag("AZDO_WI_LLM_ENABLED", False),
        keep_raw=_flag("AZDO_WI_KEEP_RAW", False),
    )
