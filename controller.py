from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from scraper import scrape_headlines # Sesuaikan nama file dengan scraper.py 

class Controller:
    def __init__(self):
        from main_window import MainWindow
        self.view = MainWindow()
        
        # Koneksi tombol ke fungsi (Tugas Anggota 3) 
        self.view.scrape_button.clicked.connect(self.handle_scrape)
        
        self.view.show()

    def handle_scrape(self):
        url = self.view.url_input.text().strip()
        
        # Handle error: URL kosong 
        if not url:
            QMessageBox.warning(self.view, "Peringatan", "URL tidak boleh kosong!")
            return

        try:
            self.view.status_label.setText("Status: Sedang memproses...") 
            
            # Panggil mesin scraper [cite: 11, 17]
            data = scrape_headlines(url)
            
            # Tampilkan hasil ke tabel 
            self.view.table.setRowCount(0)
            for row, item in enumerate(data):
                self.view.table.insertRow(row)
                self.view.table.setItem(row, 0, QTableWidgetItem(str(item.get("no", row+1))))
                self.view.table.setItem(row, 1, QTableWidgetItem(item.get("judul", "")))
                
                # --- TAMBAHKAN BARIS INI UNTUK MENGISI KOLOM TANGGAL ---
                self.view.table.setItem(row, 2, QTableWidgetItem(item.get("tanggal", "-")))
                
                self.view.table.setItem(row, 3, QTableWidgetItem(item.get("link", "")))
            
            self.view.status_label.setText(f"Status: Berhasil (Total: {len(data)})") 
            
        except Exception as e:
            # Handle error request atau timeout 
            QMessageBox.critical(self.view, "Error", f"Gagal: {str(e)}")
            self.view.status_label.setText("Status: Error")