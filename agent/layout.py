"""Una carpeta por PBI. La lectura local no se mezcla con el caso que se presenta."""

from pathlib import Path


def case_dir(root: Path, work_id: int) -> Path:
    return Path(root) / "test-cases" / f"PBI-{int(work_id)}"


def reading_dir(root: Path, work_id: int) -> Path:
    return case_dir(root, work_id) / "lectura"


def carpeta_drive() -> Path:
    """OneDrive sincronizado: Documentos/QA nico/Test cases."""
    folder = Path.home() / "OneDrive - SQA" / "QA nico" / "Test cases"
    if not folder.is_dir():
        raise FileNotFoundError(folder)
    return folder


def excel_drive(work_id: int | str, carpeta: Path | None = None) -> Path:
    base = carpeta if carpeta is not None else carpeta_drive()
    return base / f"PBI-{work_id}.xlsx"
