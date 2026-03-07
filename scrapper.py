# scraper.py
# Modul untuk scraping judul berita dari situs berita Indonesia

import requests
from bs4 import BeautifulSoup


def get_site_selectors(url):
    """Menentukan selector HTML berdasarkan situs yang di-scrape."""
    if "detik.com" in url:
        return {"tag": "article", "sub": "a"}
    elif "kompas.com" in url:
        return {"tag": "h3", "sub": "a"}
    elif "cnnindonesia.com" in url:
        return {"tag": "article", "sub": "a"}
    else:
        # Default: cari semua tag <article> dengan <a>
        return {"tag": "article", "sub": "a"}


def parse_headlines(soup, selectors):
    """Parsing headline dari HTML berdasarkan selector."""
    elements = soup.find_all(selectors["tag"])
    headlines = []

    for el in elements:
        link_tag = el.find(selectors["sub"])
        if link_tag:
            judul = link_tag.get_text(strip=True)
            link = link_tag.get("href", "")
            if judul:
                headlines.append({"judul": judul, "link": link})

    return headlines


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

    # Ambil selector berdasarkan situs
    selectors = get_site_selectors(url)
    headlines = parse_headlines(soup, selectors)

    # Tambahkan nomor urut
    result = []
    for i, item in enumerate(headlines, start=1):
        result.append({
            "no": i,
            "judul": item["judul"],
            "link": item["link"]
        })

    return result
