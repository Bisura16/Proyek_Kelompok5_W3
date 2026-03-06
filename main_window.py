import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QLabel, QHeaderView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Berita")
        self.resize(800, 500)

        # Membuat central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Membuat layout utama
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Membuat judul aplikasi
        self.title_label = QLabel("Web Scraping Judul Berita")
        self.title_label.setStyleSheet("font-size:18px; font-weight:bold;")
        self.layout.addWidget(self.title_label)

        # Membuat input URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Masukkan URL berita...")
        self.layout.addWidget(self.url_input)

        # Membuat tombol scrape dan export
        self.button_layout = QHBoxLayout()
        self.scrape_button = QPushButton("Scrape")
        self.export_button = QPushButton("Export")
        self.button_layout.addWidget(self.scrape_button)
        self.button_layout.addWidget(self.export_button)
        self.layout.addLayout(self.button_layout)
        
        self.scrape_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.export_button.setStyleSheet("background-color: #2196F3; color: white;")

        # Membuat tabel hasil
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["No", "Judul", "Tanggal", "Link"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        # Membuat status label
        self.status_label = QLabel("Status: Siap")
        self.layout.addWidget(self.status_label)

# Entry Point Program
if __name__ == "__main__":
    from controller import Controller 
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    # Controller akan menginisialisasi MainWindow dan menghubungkan tombol
    program = Controller() 
    sys.exit(app.exec_())
