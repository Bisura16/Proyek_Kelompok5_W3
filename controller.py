from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from contohscraper import scrape_headlines # Fungsi Anggota 2 [cite: 11]

class Controller:
    def __init__(self):
        from main_window import MainWindow
        self.view = MainWindow()
        
        # Koneksi tombol ke fungsi (Tugas Anggota 3) [cite: 17]
        self.view.scrape_button.clicked.connect(self.handle_scrape)
        
        self.view.show()

    def handle_scrape(self):
        url = self.view.url_input.text().strip()
        
        # Handle error: URL kosong [cite: 19]
        if not url:
            QMessageBox.warning(self.view, "Peringatan", "URL tidak boleh kosong!")
            return

        try:
            self.view.status_label.setText("Status: Sedang memproses...") 
            
            # Panggil mesin scraper [cite: 11, 17]
            data = scrape_headlines(url)
            
            # Tampilkan hasil ke tabel [cite: 18]
            self.view.table.setRowCount(0)
            for row, item in enumerate(data):
                self.view.table.insertRow(row)
                self.view.table.setItem(row, 0, QTableWidgetItem(str(item.get("no", row+1))))
                self.view.table.setItem(row, 1, QTableWidgetItem(item.get("judul", "")))
                self.view.table.setItem(row, 3, QTableWidgetItem(item.get("link", "")))
            
            self.view.status_label.setText(f"Status: Berhasil (Total: {len(data)})") 
            
        except Exception as e:
            # Handle error request atau timeout [cite: 19, 20]
            QMessageBox.critical(self.view, "Error", f"Gagal: {str(e)}")
            self.view.status_label.setText("Status: Error")