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
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    response = requests.get(url, headers=headers, timeout=10)
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
