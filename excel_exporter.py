"""
excel_exporter.py
-----------------
Modul untuk export data ke format Excel (.xlsx) menggunakan pandas + openpyxl.

Dependensi:
    pip install pandas openpyxl
"""

from pathlib import Path

try:
    import pandas as pd
    _PANDAS_OK = True
except ImportError:
    _PANDAS_OK = False


def export(data: list[dict], filepath: str) -> None:
    """
    Export list of dict ke file Excel (.xlsx).

    Args:
        data     : List of dict hasil scraping.
        filepath : Path lengkap file tujuan (.xlsx).

    Raises:
        ImportError : Jika pandas / openpyxl belum terinstall.
        ValueError  : Jika data kosong atau filepath tidak valid.
        IOError     : Jika file tidak dapat ditulis.
    """
    _check_dependency()
    _validate(data, filepath)

    df = pd.DataFrame(data)
    df.to_excel(filepath, index=False, engine="openpyxl")


def is_available() -> bool:
    """Return True jika pandas tersedia dan fitur Excel bisa digunakan."""
    return _PANDAS_OK


# ── Private ────────────────────────────────────────────────────────────────────

def _check_dependency() -> None:
    if not _PANDAS_OK:
        raise ImportError(
            "pandas dan openpyxl diperlukan untuk export Excel.\n"
            "Install dengan: pip install pandas openpyxl"
        )


def _validate(data: list[dict], filepath: str) -> None:
    if not data:
        raise ValueError("Data kosong — tidak ada yang diekspor.")
    if not filepath or not filepath.strip():
        raise ValueError("Filepath tidak boleh kosong.")
    if not filepath.endswith(".xlsx"):
        raise ValueError(f"Ekstensi file harus .xlsx, bukan: {Path(filepath).suffix!r}")
