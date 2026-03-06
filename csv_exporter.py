"""
csv_exporter.py
---------------
Modul untuk export data ke format CSV menggunakan modul csv bawaan Python.
Tidak memerlukan dependensi eksternal.
"""

import csv
from pathlib import Path


def export(data: list[dict], filepath: str) -> None:
    """
    Export list of dict ke file CSV.

    Args:
        data     : List of dict hasil scraping.
                   Contoh: [{"no": 1, "judul": "...", "link": "..."}]
        filepath : Path lengkap file tujuan, termasuk nama file (.csv).

    Raises:
        ValueError : Jika data kosong atau filepath kosong.
        IOError    : Jika file tidak dapat ditulis.
    """
    _validate(data, filepath)

    fieldnames = list(data[0].keys())

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def _validate(data: list[dict], filepath: str) -> None:
    if not data:
        raise ValueError("Data kosong — tidak ada yang diekspor.")
    if not filepath or not filepath.strip():
        raise ValueError("Filepath tidak boleh kosong.")
    if not filepath.endswith(".csv"):
        raise ValueError(f"Ekstensi file harus .csv, bukan: {Path(filepath).suffix!r}")
