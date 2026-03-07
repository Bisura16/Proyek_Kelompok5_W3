# scraper.py
# Modul untuk scraping judul berita dari situs berita Indonesia
# Mendukung: detik.com, kompas.com, cnnindonesia.com

import requests
from bs4 import BeautifulSoup


def extract_date(article, date_selector=None):
    """Ambil tanggal dari elemen article dengan beberapa fallback."""
    # Prioritas 1: pakai selector spesifik per situs jika ada
    if date_selector:
        date_el = article.find(class_=date_selector)
        if date_el:
            return date_el.get_text(strip=True)

    # Prioritas 2: cari tag <time>
    time_tag = article.find("time")
    if time_tag:
        return time_tag.get("datetime", time_tag.get_text(strip=True))

    # Fallback: cari elemen dengan class yang mengandung kata 'date' atau 'time'
    date_classes = ["date", "time", "timestamp", "media__date"]
    for cls in date_classes:
        date_el = article.find(class_=lambda c: c and cls in c.lower())
        if date_el:
            return date_el.get_text(strip=True)

    # Fallback: cari <span> yang teksnya mengandung nama bulan
    spans = article.find_all("span")
    for span in spans:
        text = span.get_text(strip=True)
        if any(bulan in text.lower() for bulan in ["jan", "feb", "mar", "apr", "mei", "jun",
                                                     "jul", "agu", "sep", "okt", "nov", "des"]):
            return text

    return "-"


def get_site_selectors(url):
    """
    Menentukan selector HTML berdasarkan situs yang di-scrape.

    Parameter:
        url (str): URL situs berita

    Return:
        dict: selector dengan key 'tag', 'sub', dan 'date_class'
    """
    if "detik.com" in url:
        return {"tag": "article", "sub": "a", "date_class": "media__date"}
    elif "kompas.com" in url:
        return {"tag": "h3", "sub": "a", "date_class": "article__date"}
    elif "cnnindonesia.com" in url:
        return {"tag": "article", "sub": "a", "date_class": "date"}
    else:
        return {"tag": "article", "sub": "a", "date_class": None}


def parse_headlines(soup, selectors):
    """
    Parsing headline dari HTML berdasarkan selector.

    Parameter:
        soup (BeautifulSoup): objek BeautifulSoup dari HTML
        selectors (dict): selector HTML dari get_site_selectors()

    Return:
        list of dict: daftar headline dengan key 'judul', 'link', dan 'tanggal'
    """
    elements = soup.find_all(selectors["tag"])
    date_class = selectors.get("date_class")
    headlines = []

    for el in elements:
        link_tag = el.find(selectors["sub"])
        if link_tag:
            judul = link_tag.get_text(strip=True)
            link = link_tag.get("href", "")
            tanggal = extract_date(el, date_class)
            if judul:
                headlines.append({"judul": judul, "link": link, "tanggal": tanggal})

    return headlines


def scrape_headlines(url):
    """
    Fungsi utama untuk scraping headline berita dari situs berita Indonesia.

    Mendukung situs: detik.com, kompas.com, cnnindonesia.com.
    Untuk situs lain, akan menggunakan selector default (tag <article>).

    Parameter:
        url (str): URL situs berita yang akan di-scrape

    Return:
        list of dict: [{"no": 1, "judul": "...", "tanggal": "...", "link": "..."}]

    Raises:
        ValueError: Jika URL kosong atau format tidak valid
        ConnectionError: Jika gagal terhubung ke situs
    """
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

    selectors = get_site_selectors(url)
    headlines = parse_headlines(soup, selectors)

    result = []
    for i, item in enumerate(headlines, start=1):
        result.append({
            "no": i,
            "judul": item["judul"],
            "tanggal": item["tanggal"],
            "link": item["link"]
        })

    return result


if __name__ == "__main__":
    test_url = "https://www.detik.com/terpopuler"
    print(f"Scraping: {test_url}\n")

    try:
        hasil = scrape_headlines(test_url)
        if hasil:
            for h in hasil[:5]:
                print(f"{h['no']}. {h['judul']}")
                print(f"   Link: {h['link']}\n")
        else:
            print("Tidak ada headline ditemukan.")
    except (ValueError, ConnectionError) as e:
        print(f"Error: {e}")
