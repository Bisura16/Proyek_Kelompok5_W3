# scraper.py
# Modul untuk scraping judul berita dari situs berita Indonesia

import requests
from bs4 import BeautifulSoup


def scrape_headlines(url):
    """Fungsi utama untuk scraping headline berita."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    response = requests.get(url, headers=headers, timeout=10)
    html = response.text

    return html
