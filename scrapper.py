# scraper.py
# Modul untuk scraping judul berita dari situs berita Indonesia

import requests
from bs4 import BeautifulSoup


def scrape_headlines(url):
    """
    Fungsi utama untuk scraping headline berita.

    Parameter:
        url (str): URL situs berita yang akan di-scrape

    Return:
        list of dict: [{"no": 1, "judul": "...", "link": "..."}]

    Raises:
        ValueError: Jika URL kosong
        ConnectionError: Jika gagal terhubung ke situs
    """
    # Validasi URL
    if not url or not url.strip():
        raise ValueError("URL tidak boleh kosong!")

    if not url.startswith("http"):
        raise ValueError("URL harus diawali dengan http:// atau https://")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise ConnectionError("Request timeout! Coba lagi nanti.")
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Gagal terhubung ke situs. Cek koneksi internet.")
    except requests.exceptions.HTTPError as e:
        raise ConnectionError(f"HTTP Error: {e}")

    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # Parsing untuk detik.com
    articles = soup.find_all("article")
    headlines = []

    for article in articles:
        link_tag = article.find("a")
        if link_tag:
            judul = link_tag.get_text(strip=True)
            link = link_tag.get("href", "")
            if judul:
                headlines.append({"judul": judul, "link": link})

    # Tambahkan nomor urut
    result = []
    for i, item in enumerate(headlines, start=1):
        result.append({
            "no": i,
            "judul": item["judul"],
            "link": item["link"]
        })

    return result
