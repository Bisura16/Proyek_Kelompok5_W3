import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QLabel

app = QApplication(sys.argv)  # membuat aplikasi

window = QMainWindow()  # membuat window
window.setWindowTitle("Berita")  # memberi judul web

# membuat central widget
central_widget = QWidget()
window.setCentralWidget(central_widget)

# membuat layout
layout = QVBoxLayout()
central_widget.setLayout(layout)

#membuat judul aplikasi
title_label = QLabel("Web Scraping Judul Berita")
title_label.setStyleSheet("font-size:18px; font-weight:bold;")
layout.addWidget(title_label)

# membuat input URL
url_input = QLineEdit()
url_input.setPlaceholderText("Masukkan URL berita...")
layout.addWidget(url_input)


#membuat tombol scrape dan export
button_layout = QHBoxLayout()
scrape_button = QPushButton("Scrape")
export_button = QPushButton("Export")
button_layout.addWidget(scrape_button)
button_layout.addWidget(export_button)
layout.addLayout(button_layout)
scrape_button.setStyleSheet("background-color: #4CAF50; color: white;")
export_button.setStyleSheet("background-color: #2196F3; color: white;")

#membuat tabel
table = QTableWidget()
table.setColumnCount(4)
table.setHorizontalHeaderLabels(["No", "Judul", "Tanggal", "Link"])
table.horizontalHeader().setStretchLastSection(True)
layout.addWidget(table)

#membuat status label
status_label = QLabel("Status: Siap")
layout.addWidget(status_label)

# menampilkan window
window.show()

# menjalankan aplikasi
sys.exit(app.exec_())