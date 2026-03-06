"""
export_handler.py
-----------------
Orkestrator / façade yang menggabungkan semua modul exporter.

Alur kerja:
  1. Tampilkan dialog pilih lokasi file  (file_dialog)
  2. Jalankan fungsi export sesuai format (csv_exporter / excel_exporter)
  3. Tampilkan notifikasi hasil           (notifier)

Hanya modul INI yang perlu diimpor oleh controller / main_window.
"""

from PyQt5.QtWidgets import QWidget

from exporter import csv_exporter, excel_exporter, file_dialog, notifier

# Mapping format → fungsi export
_EXPORTERS = {
    "csv":   csv_exporter.export,
    "excel": excel_exporter.export,
}


def run(
    data: list[dict],
    parent: QWidget = None,
    fmt: str = "csv",
) -> bool:
    """
    Jalankan seluruh alur export secara berurutan.

    Args:
        data   : Data hasil scraping dari QTableWidget.
        parent : Widget parent (untuk dialog & notifikasi).
        fmt    : Format tujuan — "csv" atau "excel".

    Returns:
        True  → export berhasil.
        False → dibatalkan atau gagal.
    """
    # 1. Pilih lokasi simpan
    filepath = file_dialog.ask_save_path(parent=parent, fmt=fmt)
    if not filepath:
        return False  # user klik Cancel — tidak perlu notifikasi

    # 2. Ekspor data
    export_fn = _get_exporter(fmt)
    if export_fn is None:
        notifier.failed(parent, reason=f"Format {fmt!r} tidak didukung.")
        return False

    try:
        export_fn(data, filepath)
    except (ValueError, ImportError, OSError) as exc:
        notifier.failed(parent, reason=str(exc))
        return False

    # 3. Notifikasi sukses
    notifier.success(parent, filepath)
    return True


# ── Private ────────────────────────────────────────────────────────────────────

def _get_exporter(fmt: str):
    """Return fungsi export yang sesuai, atau None jika tidak dikenal."""
    return _EXPORTERS.get(fmt)
