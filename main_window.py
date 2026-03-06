
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Berita")
        self.resize(600, 400)
#Bagian memuat aplikasi dipindahkan ke controller.py (Anggota 3)
app = QApplication(sys.argv)
# membuat central widget
self.central_widget = QWidget()
self.setCentralWidget(self.central_widget)

# membuat layout
self.layout = QVBoxLayout()
self.central_widget.setLayout(self.layout)

#membuat judul aplikasi
self.title_label = QLabel("Web Scraping Judul Berita")
self.title_label.setStyleSheet("font-size:18px; font-weight:bold;")
self.layout.addWidget(self.title_label)

# membuat input URL
self.url_input = QLineEdit()
self.url_input.setPlaceholderText("Masukkan URL berita...")
self.layout.addWidget(self.url_input)


#membuat tombol scrape dan export
button_layout = QHBoxLayout()
scrape_button = QPushButton("Scrape")
export_button = QPushButton("Export")
button_layout.addWidget(scrape_button)
button_layout.addWidget(export_button)
self.layout.addLayout(button_layout)
self.scrape_button = scrape_button
self.export_button = export_button
self.scrape_button.setStyleSheet("background-color: #4CAF50; color: white;")
self.export_button.setStyleSheet("background-color: #2196F3; color: white;")

#membuat tabel
self.table = QTableWidget()
self.table.setColumnCount(4)
self.table.setHorizontalHeaderLabels(["No", "Judul", "Tanggal", "Link"])
self.table.horizontalHeader().setStretchLastSection(True)
self.layout.addWidget(self.table)

#membuat status label
self.status_label = QLabel("Status: Siap")
self.layout.addWidget(self.status_label)

# menampilkan window
window.show()

# menjalankan aplikasi
sys.exit(app.exec_())
