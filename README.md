# PROYEK_KELOMPOK 5_W3

| No | Nama                         | NIM       | GitHub           |
|----|------------------------------|-----------|------------------|
| 1  | Bimo Surya Anggara           | 251524040 | Bisura16         |
| 2  | Ghaisan Khoirul Badruzaman   | 251524048 | Ghaisank         |
| 3  | Abhidal Muhammad Gazza       | 251524032 | AbhidalMG        |
| 4  | Muhammad Iqbal               | 251524057 | Ballvoldigoad    |
| 5  | Alia Ardani                  | 251524035 | vssixla          |


## APLIKASI SCRAPING BERITA DENGAN GUI (SELENIUM)
Aplikasi ini merupakan program web scraping berita berbasis desktop yang dibuat menggunakan bahasa pemrograman Python dengan memanfaatkan beberapa library, yaitu PyQt5 sebagai antarmuka grafis (GUI), requests untuk melakukan HTTP request ke website, BeautifulSoup4 untuk melakukan parsing HTML, serta pandas atau csv untuk mengekspor data ke dalam format CSV.

Aplikasi ini memungkinkan pengguna untuk memasukkan URL halaman berita, kemudian sistem akan mengambil artikel dari halaman tersebut dan mengekstrak informasi penting seperti judul berita, tanggal publikasi, serta tautan artikel. Hasil proses scraping tersebut kemudian ditampilkan dalam bentuk tabel pada aplikasi, sehingga pengguna dapat melihat data yang diperoleh secara terstruktur. Selain itu, data yang telah diperoleh juga dapat diekspor ke dalam file CSV untuk keperluan penyimpanan atau pengolahan data lebih lanjut.

## SISTEM UNTUK MENJALANKAN PROGRAM 
Berikut ini library yang dapat digunakan untuk menjalankan aplikasi ini: 
- Python, digunakan sebagai bahasa pemrograman utama untuk membangun dan menjalankan seluruh fungsi aplikasi
- PyQt5, digunakan untuk membuat antarmuka grafis (GUI) sehingga pengguna dapat berinteraksi dengan aplikasi.
- Requests, digunakan untuk mengambil data halaman web melalui HTTP request.
- BeautifulSoup4, digunakan untuk memproses dan mengekstrak informasi dari struktur HTML halaman web.
- CSV Module, digunakan untuk menyimpan hasil scraping ke dalam file berformat CSV. Modul ini merupakan modul bawaan Python sehingga tidak memerlukan instalasi tambahan

## CARA UNTUK MENJALANKAN APLIKASI
Untuk menjalankan aplikasi ini, pastikan perangkat yang akan digunakan mempunyai bahasa pemrograman python
1. Clone repository ini ke komputer lokal (Command Prompt, Git Bash, dll)
   ```
   git clone https://github.com/Bisura16/Proyek_Kelompok5_W3.git
   ```
2. Masuk ke root repositori ini
   ```
   cd Proyek_Kelompok5_W3
   ```
4. Install library yang diperlukan menggunakan file requirements.txt
   ```
   pip install -r requirements.txt
   ```
5. Setelah semua terinstall, jalankan aplikasi ini
   ```
   python main_window.py
   ```
   
## TAMPILAN APLIKASI 
1. Halaman utama Aplikasi
   <img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/40ffac89-fe6c-4d38-9654-03009a87d844" />

2. Melampirkan tautan berita yang akan discraping
   <img width="1915" height="334" alt="image" src="https://github.com/user-attachments/assets/73ca1742-05d9-450c-b33e-e6b779261cc5" />

3. Tampilan hasil scraping berita
   <img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/716439fa-2547-4e44-a1a1-33b6904faa8c" />

4. Hasil scraping yang diekspor menjadi file.csv
   <img width="1920" height="1200" alt="Cuplikan layar 2026-03-07 204648" src="https://github.com/user-attachments/assets/6e653b34-15e5-4112-a0cc-167da3b31050" />




