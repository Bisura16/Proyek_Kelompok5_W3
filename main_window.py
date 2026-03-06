import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton

app = QApplication(sys.argv)  # membuat aplikasi

window = QMainWindow()  # membuat window
window.setWindowTitle("Berita")  # memberi judul

# membuat central widget
central_widget = QWidget()
window.setCentralWidget(central_widget)

# membuat layout
layout = QVBoxLayout()
central_widget.setLayout(layout)

# membuat input URL
url_input = QLineEdit()
url_input.setPlaceholderText("Masukkan URL berita...")

#membuat tombol scrape
scrape_button = QPushButton("Scrape")
layout.addWidget(scrape_button)

#membuat tombol export
export_button = QPushButton("Export")
layout.addWidget(export_button)

# memasukkan input ke layout
layout.addWidget(url_input)

# menampilkan window
window.show()

# menjalankan aplikasi
sys.exit(app.exec_())