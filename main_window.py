import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

app = QApplication(sys.argv) #Membuat aplikasi

window = QMainWindow() #Membuat window
window.setWindowTitle("Berita") #Memberi judul
window.show() #Menampilkan window

sys.exit(app.exec_()) #Menjalankan aplikasi