import requests
from bs4 import BeautifulSoup

def scrape_headlines(url):
    """
    Fungsi untuk mengambil judul berita dari URL yang diberikan.
    Mengembalikan list of dictionary: [{"no": 1, "judul": "...", "link": "..."}]
    """
    # [cite: 11, 14]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Melakukan request ke website 
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Akan error jika request gagal 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # Contoh parsing sederhana (disesuaikan dengan target situs umum) [cite: 13]
        # Kita mencari tag <h3> atau <h2> yang biasanya berisi judul berita
        articles = soup.find_all(['h2', 'h3'], limit=10) 
        
        for index, article in enumerate(articles, start=1):
            judul = article.get_text(strip=True)
            # Mencari link di dalam atau di sekitar tag judul
            link_tag = article.find('a') or article.parent.find('a')
            link = link_tag['href'] if link_tag and link_tag.has_attr('href') else url
            
            # Memastikan link adalah URL lengkap
            if link.startswith('/'):
                from urllib.parse import urljoin
                link = urljoin(url, link)
                
            results.append({
                "no": index,
                "judul": judul,
                "link": link
            })
            
        return results # [cite: 11, 14]

    except Exception as e:
        # Melemparkan error agar bisa ditangkap oleh Controller (Anggota 3) 
        raise Exception(f"Gagal melakukan scraping: {str(e)}")