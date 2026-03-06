#Program ini dibuat untuk menguji fungsi controller dan scraper secara terpisah sebelum diintegrasikan ke dalam MainWindow.
#Tujuannya untuk memastikan bahwa fungsi scraping berjalan dengan baik dan dapat menangani berbagai jenis URL berita tanpa error, serta untuk memverifikasi bahwa data yang diambil sesuai dengan format yang diharapkan.
#Catatan: Silahkan ganti nama file nya dengan scraper dan ubah juga nama fungsi nya dengan scrape_headlines jika ingin menguji fungsi tersebut secara langsung tanpa menggunakan GUI.

import requests
from bs4 import BeautifulSoup

def scrape_headlines(url):
    """
    Fungsi untuk mengambil judul berita dari URL yang diberikan.
    Target: detik.com, kompas.com, atau portal berita lainnya.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Melakukan request ke website [cite: 12]
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Akan memicu error jika request gagal [cite: 19]
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # Mencari elemen judul (biasanya h2 atau h3 di portal berita) 
        articles = soup.find_all(['h2', 'h3'], limit=15) 
        
        for index, article in enumerate(articles, start=1):
            judul = article.get_text(strip=True)
            
            # Mencari link berita
            link_tag = article.find('a') or article.parent.find('a')
            link = link_tag['href'] if link_tag and link_tag.has_attr('href') else url
            
            # Memastikan link adalah URL lengkap
            if link.startswith('/'):
                from urllib.parse import urljoin
                link = urljoin(url, link)
            
            # Memasukkan ke format list of dict sesuai instruksi 
            results.append({
                "no": index,
                "judul": judul,
                "link": link
            })
            
        return results

    except Exception as e:
        # Melemparkan error agar bisa ditangani oleh Controller (Anggota 3) [cite: 19]
        raise Exception(f"Gagal melakukan scraping: {str(e)}")