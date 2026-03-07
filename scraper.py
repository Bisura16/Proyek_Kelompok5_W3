# scraper.py
# ============================================================
# Modul Anggota 2 — Scraping Engine
# Scraping judul berita dari situs berita Indonesia
# Mendukung: detik.com, kompas.com, cnnindonesia.com,
#            cnbcindonesia.com, liputan6.com
# ============================================================

import re
import requests
from bs4 import BeautifulSoup


# ── Header HTTP ────────────────────────────────────────────────────────────────

def _get_headers():
    """
    Menyusun header HTTP agar request tidak diblokir oleh situs berita.

    Menggunakan User-Agent browser modern lengkap dengan
    Accept, Accept-Language, dan Referer supaya menyerupai
    request dari browser sungguhan.

    Return:
        dict: header HTTP untuk requests.get()
    """
    return {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/",
    }


# ── Ekstraksi Tanggal ─────────────────────────────────────────────────────────

def extract_date_from_url(url):
    """
    Mengambil tanggal dari pola URL berita Indonesia.

    Banyak situs berita Indonesia menyimpan tanggal di URL,
    contoh: /read/2026/03/07/... atau /d-1234567/...

    Parameter:
        url (str): URL artikel berita

    Return:
        str: tanggal dalam format DD/MM/YYYY, atau None jika tidak ditemukan
    """
    # Pola: /YYYY/MM/DD/ (kompas, cnbcindonesia, liputan6)
    match = re.search(r'/(\d{4})/(\d{2})/(\d{2})/', url)
    if match:
        tahun, bulan, hari = match.groups()
        return f"{hari}/{bulan}/{tahun}"

    # Pola: /YYYYMMDD (cnbcindonesia format alternatif)
    match = re.search(r'/(\d{4})(\d{2})(\d{2})\d{6}', url)
    if match:
        tahun, bulan, hari = match.groups()
        return f"{hari}/{bulan}/{tahun}"

    return None


def extract_date(article, date_selector=None, fallback_url=None):
    """
    Mengambil tanggal publikasi dari elemen article.

    Menggunakan beberapa strategi fallback:
    1. Selector class spesifik per situs (jika tersedia)
    2. Tag <time> (standar HTML5)
    3. Elemen dengan class mengandung 'date'/'time'
    4. Tag <span> yang teksnya mengandung nama bulan
    5. Tanggal dari URL artikel (fallback terakhir)

    Parameter:
        article (Tag): elemen BeautifulSoup dari artikel
        date_selector (str): class CSS spesifik untuk tanggal (opsional)
        fallback_url (str): URL artikel untuk ekstraksi tanggal dari URL (opsional)

    Return:
        str: tanggal publikasi, atau "-" jika tidak ditemukan
    """
    # Prioritas 1: pakai selector spesifik per situs jika ada
    if date_selector:
        date_el = article.find(class_=date_selector)
        if date_el:
            return date_el.get_text(strip=True)

    # Prioritas 2: cari tag <time> (standar HTML5 untuk waktu)
    time_tag = article.find("time")
    if time_tag:
        # Ambil datetime attribute dulu, kalau ada
        dt = time_tag.get("datetime", "")
        text = time_tag.get_text(strip=True)
        # Pilih yang lebih informatif
        if text:
            return text
        if dt:
            return dt

    # Fallback 3: cari elemen dengan class yang mengandung kata date/time
    date_classes = ["date", "time", "timestamp", "media__date", "article__date"]
    for cls in date_classes:
        date_el = article.find(class_=lambda c: c and cls in c.lower())
        if date_el:
            return date_el.get_text(strip=True)

    # Fallback 4: cari <span> yang teksnya mengandung nama bulan Indonesia
    bulan_list = [
        "januari", "februari", "maret", "april", "mei", "juni",
        "juli", "agustus", "september", "oktober", "november", "desember",
        "jan", "feb", "mar", "apr", "jun", "jul", "agu", "sep", "okt", "nov", "des"
    ]
    spans = article.find_all(["span", "div", "p", "small"])
    for el in spans:
        text = el.get_text(strip=True).lower()
        if any(bulan in text for bulan in bulan_list):
            return el.get_text(strip=True)

    # Fallback 5: cari tanggal dari pola teks umum (DD/MM/YYYY atau YYYY-MM-DD)
    full_text = article.get_text()
    date_pattern = re.search(
        r'(\d{1,2}\s(?:Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)\s\d{4})',
        full_text, re.IGNORECASE
    )
    if date_pattern:
        return date_pattern.group(1)

    # Fallback 6: ekstrak tanggal dari URL
    if fallback_url:
        date_from_url = extract_date_from_url(fallback_url)
        if date_from_url:
            return date_from_url

    return "-"


# ── Selector per Situs ────────────────────────────────────────────────────────

def get_site_config(url):
    """
    Menentukan konfigurasi scraping berdasarkan situs berita.

    Setiap situs berita punya struktur HTML yang berbeda.
    Fungsi ini memetakan URL ke konfigurasi selector yang sesuai.

    Parameter:
        url (str): URL situs berita

    Return:
        dict: konfigurasi scraping dengan key:
              - tag: tag HTML utama pembungkus artikel
              - attrs: atribut filter untuk tag (opsional)
              - sub: tag di dalam 'tag' yang berisi judul + link
              - date_class: class CSS untuk elemen tanggal
              - nama: nama situs untuk pesan error
    """
    if "detik.com" in url:
        return {
            "tag": "article",
            "attrs": {},
            "sub": "a",
            "date_class": "media__date",
            "nama": "Detik"
        }
    elif "kompas.com" in url:
        return {
            "tag": "a",
            "attrs": {"class": lambda c: c and any(
                x in " ".join(c).lower() for x in ["headline", "article__link", "most__link"]
            )},
            "sub": None,  # tag <a> sendiri sudah link-nya
            "date_class": "article__date",
            "nama": "Kompas"
        }
    elif "cnnindonesia.com" in url:
        return {
            "tag": "article",
            "attrs": {},
            "sub": "a",
            "date_class": "date",
            "nama": "CNN Indonesia"
        }
    elif "cnbcindonesia.com" in url:
        return {
            "tag": "article",
            "attrs": {},
            "sub": "a",
            "date_class": "date",
            "nama": "CNBC Indonesia"
        }
    elif "liputan6.com" in url:
        return {
            "tag": "article",
            "attrs": {},
            "sub": "a",
            "date_class": None,
            "nama": "Liputan6"
        }
    else:
        return {
            "tag": "article",
            "attrs": {},
            "sub": "a",
            "date_class": None,
            "nama": "Umum"
        }


# ── Parsing Headline ──────────────────────────────────────────────────────────

def parse_headlines(soup, config, base_url=""):
    """
    Parsing headline berita dari HTML berdasarkan konfigurasi situs.

    Fungsi ini mencari elemen-elemen artikel di halaman,
    kemudian mengekstrak judul, link, dan tanggal dari setiap elemen.

    Parameter:
        soup (BeautifulSoup): objek BeautifulSoup dari HTML halaman
        config (dict): konfigurasi selector dari get_site_config()
        base_url (str): URL halaman asal untuk fallback tanggal

    Return:
        list of dict: daftar headline dengan key 'judul', 'link', dan 'tanggal'
    """
    headlines = []
    seen_titles = set()
    date_class = config.get("date_class")

    if config.get("sub") is None:
        # Mode khusus: tag utama langsung berisi link (contoh: Kompas)
        elements = soup.find_all(config["tag"], config.get("attrs", {}))
        for el in elements:
            judul = el.get_text(strip=True)
            link = el.get("href", "")

            # Skip jika judul kosong, terlalu pendek, atau duplikat
            if not judul or len(judul) < 10 or judul in seen_titles:
                continue

            # Skip link navigasi (bukan artikel berita)
            if not link or "/read/" not in link:
                continue

            seen_titles.add(judul)

            # Coba ambil tanggal dari elemen parent
            parent = el.find_parent()
            tanggal = "-"
            if parent:
                tanggal = extract_date(parent, date_class, fallback_url=link)
            if tanggal == "-":
                tanggal = extract_date_from_url(link) or "-"

            headlines.append({
                "judul": judul,
                "link": link,
                "tanggal": tanggal
            })
    else:
        # Mode standar: cari tag pembungkus, lalu sub-tag link di dalamnya
        elements = soup.find_all(config["tag"], config.get("attrs", {}))
        for el in elements:
            link_tag = el.find(config["sub"])
            if not link_tag:
                continue

            judul = link_tag.get_text(strip=True)
            link = link_tag.get("href", "")

            # Skip jika judul kosong, terlalu pendek, atau duplikat
            if not judul or len(judul) < 10 or judul in seen_titles:
                continue

            seen_titles.add(judul)
            tanggal = extract_date(el, date_class, fallback_url=link)

            headlines.append({
                "judul": judul,
                "link": link,
                "tanggal": tanggal
            })

    return headlines


def parse_headlines_generic(soup, base_url=""):
    """
    Parsing headline dengan pendekatan generik jika selector spesifik gagal.

    Mencari semua tag <a> yang href-nya mengarah ke pola URL artikel
    berita Indonesia (mengandung /read/, /berita/, /news/, dll).

    Parameter:
        soup (BeautifulSoup): objek BeautifulSoup dari HTML halaman
        base_url (str): URL halaman asal

    Return:
        list of dict: daftar headline dengan key 'judul', 'link', dan 'tanggal'
    """
    headlines = []
    seen_titles = set()

    # Pola URL artikel berita Indonesia
    article_patterns = [
        r'/read/', r'/berita/', r'/news/', r'/\d+/',
        r'/d-\d+/', r'/post/\d+', r'/article/'
    ]

    all_links = soup.find_all("a", href=True)
    for link_tag in all_links:
        href = link_tag.get("href", "")
        judul = link_tag.get_text(strip=True)

        # Skip judul kosong atau terlalu pendek
        if not judul or len(judul) < 15:
            continue

        # Cek apakah href cocok dengan pola artikel
        is_article = any(re.search(pattern, href) for pattern in article_patterns)
        if not is_article:
            continue

        # Skip duplikat
        if judul in seen_titles:
            continue

        seen_titles.add(judul)

        # Coba ambil tanggal dari parent element
        parent = link_tag.find_parent()
        tanggal = "-"
        if parent:
            tanggal = extract_date(parent, fallback_url=href)
        if tanggal == "-":
            tanggal = extract_date_from_url(href) or "-"

        headlines.append({
            "judul": judul,
            "link": href,
            "tanggal": tanggal
        })

    return headlines


# ── Fungsi Utama ──────────────────────────────────────────────────────────────

def scrape_headlines(url):
    """
    Fungsi utama untuk scraping headline berita dari situs berita Indonesia.

    Mendukung situs: detik.com, kompas.com, cnnindonesia.com,
    cnbcindonesia.com, liputan6.com. Untuk situs lain, akan
    menggunakan pendekatan generik (deteksi pola URL artikel).

    Parameter:
        url (str): URL situs berita yang akan di-scrape

    Return:
        list of dict: [{"no": 1, "judul": "...", "tanggal": "...", "link": "..."}]

    Raises:
        ValueError: Jika URL kosong atau format tidak valid
        ConnectionError: Jika gagal terhubung ke situs
    """
    # Validasi URL tidak boleh kosong
    if not url or not url.strip():
        raise ValueError("URL tidak boleh kosong!")

    # Validasi format URL harus diawali http/https
    if not url.startswith("http"):
        raise ValueError("URL harus diawali dengan http:// atau https://")

    # Kirim HTTP GET request ke URL
    headers = _get_headers()
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise ConnectionError("Request timeout! Coba lagi nanti.")
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Gagal terhubung ke situs. Cek koneksi internet.")
    except requests.exceptions.HTTPError as e:
        raise ConnectionError(f"HTTP Error: {e}")

    # Parse HTML menggunakan BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Ambil konfigurasi berdasarkan situs dan parse headline
    config = get_site_config(url)
    headlines = parse_headlines(soup, config, base_url=url)

    # Jika selector spesifik gagal, coba pendekatan generik
    if not headlines:
        headlines = parse_headlines_generic(soup, base_url=url)

    # Tambahkan nomor urut ke setiap headline
    result = []
    for i, item in enumerate(headlines, start=1):
        result.append({
            "no": i,
            "judul": item["judul"],
            "tanggal": item["tanggal"],
            "link": item["link"]
        })

    return result


# ── Testing ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_urls = [
        "https://www.detik.com/terpopuler",
        "https://www.liputan6.com/news",
    ]

    for test_url in test_urls:
        print(f"\nScraping: {test_url}")
        print("=" * 60)

        try:
            hasil = scrape_headlines(test_url)
            if hasil:
                for h in hasil[:5]:
                    print(f"\n{h['no']}. {h['judul']}")
                    print(f"   Tanggal: {h['tanggal']}")
                    print(f"   Link:    {h['link']}")
                print(f"\n{'=' * 60}")
                print(f"Total headline ditemukan: {len(hasil)}")
            else:
                print("Tidak ada headline ditemukan.")
        except (ValueError, ConnectionError) as e:
            print(f"Error: {e}")
