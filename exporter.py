"""
exporter.py
-----------
Modul Anggota 4 — Export Data.

Tanggung jawab:
  - Ambil data dari QTableWidget (kolom: No, Judul, Tanggal, Link)
  - Munculkan QFileDialog untuk pilih lokasi simpan
  - Panggil csv_exporter untuk menulis file CSV
  - Tampilkan notifikasi sukses/gagal via QMessageBox

Cara pakai di controller.py:
    from exporter import handle_export
    self.view.export_button.clicked.connect(
        lambda: handle_export(self.view.table, parent=self.view)
    )
"""

from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidget, QWidget

from csv_exporter import export as write_csv

# Kolom tabel sesuai main.py: ["No", "Judul", "Tanggal", "Link"]
_TABLE_HEADERS = ["No", "Judul", "Tanggal", "Link"]


def handle_export(table: QTableWidget, parent: QWidget = None) -> None:
    """
    Jalankan seluruh alur export dari QTableWidget ke file CSV.

    Args:
        table  : QTableWidget berisi data hasil scraping.
        parent : Widget parent untuk dialog & notifikasi.
    """
    # 1. Ambil data dari tabel
    data = _get_table_data(table)
    if not data:
        _show_error(parent, "Tabel kosong — lakukan scraping terlebih dahulu.")
        return

    # 2. Pilih lokasi simpan
    filepath, _ = QFileDialog.getSaveFileName(
        parent,
        "Simpan File CSV",
        "hasil_scraping.csv",
        "CSV Files (*.csv)",
    )
    if not filepath:
        return  # user klik Cancel, tidak perlu notifikasi

    # 3. Tulis file CSV
    try:
        write_csv(data, filepath)
    except (ValueError, IOError) as e:
        _show_error(parent, str(e))
        return

    # 4. Notifikasi sukses
    QMessageBox.information(
        parent,
        "Export Berhasil",
        f"Data berhasil disimpan ke:\n{filepath}",
    )


# ── Private ────────────────────────────────────────────────────────────────────

def _get_table_data(table: QTableWidget) -> list[dict]:
    """
    Konversi isi QTableWidget ke list of dict.

    Menghasilkan:
        [{"No": "1", "Judul": "...", "Tanggal": "...", "Link": "..."}, ...]
    """
    result = []
    for row in range(table.rowCount()):
        item = {
            _TABLE_HEADERS[col]: table.item(row, col).text() if table.item(row, col) else ""
            for col in range(table.columnCount())
        }
        result.append(item)
    return result


def _show_error(parent: QWidget, message: str) -> None:
    """Tampilkan QMessageBox error."""
    QMessageBox.critical(parent, "Export Gagal", message)
