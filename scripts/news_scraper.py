import os
import csv
import time
import requests
import re
from bs4 import BeautifulSoup
from datetime import date

OUTPUT_CSV = "data/nepali_news.csv"
SEEN_URLS_FILE = "data/seen_news_urls.txt"
TODAY = date.today().isoformat()
DEVANAGARI_RE = re.compile(r'[\u0900-\u097F]')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ne,en;q=0.9",
}

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def load_seen_urls():
    if os.path.exists(SEEN_URLS_FILE):
        with open(SEEN_URLS_FILE, "r") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_seen_url(url):
    with open(SEEN_URLS_FILE, "a") as f:
        f.write(url + "\n")

def append_article(row):
    file_exists = os.path.exists(OUTPUT_CSV)
    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["text", "url", "source", "domain", "date_scraped"],
            quoting=csv.QUOTE_ALL
        )
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def fetch(url, timeout=15):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
        r.encoding = "utf-8"
        return r.text
    except Exception:
        return None

def has_nepali(text):
    return bool(DEVANAGARI_RE.search(text))

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def extract_text(html, selectors):
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.find_all(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()
    for selector in selectors:
        parts = selector.split(".")
        elem = soup.find(parts[0], class_=parts[1] if len(parts) > 1 else None)
        if elem:
            text = clean_text(elem.get_text(separator=" "))
            if len(text) > 200 and has_nepali(text):
                return text
    return None

# ─────────────────────────────────────────
# RATOPATI
# Categories paginated at /category/X?page=N
# Article URLs: /story/ID/slug
# ─────────────────────────────────────────
RATOPATI_CATEGORIES = [
    "news", "politics", "economy", "society", "sports",
    "entertainment", "international", "technology", "health",
    "education", "province", "court-office", "crime",
]
RATOPATI_SELECTORS = ["div.dn__news--wrap", "div.content-flex", "article"]

def scrape_ratopati(seen_urls):
    total = 0
    for cat in RATOPATI_CATEGORIES:
        print(f"  [{cat}]", end=" ", flush=True)
        cat_total = 0
        for page in range(1, 501):
            url = f"https://www.ratopati.com/category/{cat}?page={page}"
            html = fetch(url)
            if not html:
                break
            soup = BeautifulSoup(html, "lxml")
            links = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if re.search(r'/story/\d+', href):
                    full = href if href.startswith("http") else "https://www.ratopati.com" + href
                    if full not in seen_urls:
                        links.append(full)
            if not links:
                break
            for article_url in links:
                seen_urls.add(article_url)
                save_seen_url(article_url)
                article_html = fetch(article_url)
                if not article_html:
                    continue
                text = extract_text(article_html, RATOPATI_SELECTORS)
                if text:
                    append_article({"text": text, "url": article_url, "source": "ratopati", "domain": "news", "date_scraped": TODAY})
                    total += 1
                    cat_total += 1
                time.sleep(0.3)
        print(f"{cat_total} articles")
    return total

# ─────────────────────────────────────────
# ONLINEKHABAR
# Categories paginated at /content/X?page=N
# Article URLs: /2026/03/ID/slug
# ─────────────────────────────────────────
OK_CATEGORIES = [
    "news", "news/rastiya", "desh-samachar", "international",
    "opinion", "business", "business/technology", "entertainment",
    "sports", "health", "education",
]
OK_SELECTORS = ["div.ok18-single-post-content-wrap", "div.ok-news-post", "article"]

def scrape_onlinekhabar(seen_urls):
    total = 0
    for cat in OK_CATEGORIES:
        print(f"  [{cat}]", end=" ", flush=True)
        cat_total = 0
        for page in range(1, 501):
            url = f"https://www.onlinekhabar.com/content/{cat}?page={page}"
            html = fetch(url)
            if not html:
                break
            soup = BeautifulSoup(html, "lxml")
            links = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if re.search(r'/\d{4}/\d{2}/\d+/', href):
                    full = href if href.startswith("http") else "https://www.onlinekhabar.com" + href
                    if full not in seen_urls:
                        links.append(full)
            if not links:
                break
            for article_url in links:
                seen_urls.add(article_url)
                save_seen_url(article_url)
                article_html = fetch(article_url)
                if not article_html:
                    continue
                text = extract_text(article_html, OK_SELECTORS)
                if text:
                    append_article({"text": text, "url": article_url, "source": "onlinekhabar", "domain": "news", "date_scraped": TODAY})
                    total += 1
                    cat_total += 1
                time.sleep(0.3)
        print(f"{cat_total} articles")
    return total

# ─────────────────────────────────────────
# EKANTIPUR
# Categories paginated at /X?page=N
# Article URLs: /news/2026/04/01/slug.html
# ─────────────────────────────────────────
KANTIPUR_CATEGORIES = [
    "news", "province", "international", "sports",
    "entertainment", "business", "opinion", "health", "technology",
]
KANTIPUR_SELECTORS = ["div.news-inner-wrapper", "div.description", "article"]

def scrape_kantipur(seen_urls):
    total = 0
    for cat in KANTIPUR_CATEGORIES:
        print(f"  [{cat}]", end=" ", flush=True)
        cat_total = 0
        for page in range(1, 501):
            url = f"https://ekantipur.com/{cat}?page={page}"
            html = fetch(url)
            if not html:
                break
            soup = BeautifulSoup(html, "lxml")
            links = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if re.search(r'/\d{4}/\d{2}/\d{2}/.*\.html', href):
                    full = href if href.startswith("http") else "https://ekantipur.com" + href
                    if full not in seen_urls:
                        links.append(full)
            if not links:
                break
            for article_url in links:
                seen_urls.add(article_url)
                save_seen_url(article_url)
                article_html = fetch(article_url)
                if not article_html:
                    continue
                text = extract_text(article_html, KANTIPUR_SELECTORS)
                if text:
                    append_article({"text": text, "url": article_url, "source": "kantipur", "domain": "news", "date_scraped": TODAY})
                    total += 1
                    cat_total += 1
                time.sleep(0.3)
        print(f"{cat_total} articles")
    return total

# ─────────────────────────────────────────
# SETOPATI
# Categories paginated at /X?page=N
# Article URLs: /category/ID
# ─────────────────────────────────────────
SETOPATI_CATEGORIES = [
    "politics", "cover-story", "opinion", "social",
    "art", "sports", "global", "exclusive",
]
SETOPATI_SELECTORS = ["div.news-content", "div.article-content", "div.post-content", "article"]

def scrape_setopati(seen_urls):
    total = 0
    for cat in SETOPATI_CATEGORIES:
        print(f"  [{cat}]", end=" ", flush=True)
        cat_total = 0
        for page in range(1, 501):
            url = f"https://www.setopati.com/{cat}?page={page}"
            html = fetch(url)
            if not html:
                break
            soup = BeautifulSoup(html, "lxml")
            links = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if re.search(r'/[a-z\-]+/\d{4,}$', href) and "setopati.com" in href:
                    if href not in seen_urls:
                        links.append(href)
                elif re.search(r'/[a-z\-]+/\d{4,}$', href) and href.startswith("/"):
                    full = "https://www.setopati.com" + href
                    if full not in seen_urls:
                        links.append(full)
            if not links:
                break
            for article_url in links:
                seen_urls.add(article_url)
                save_seen_url(article_url)
                article_html = fetch(article_url)
                if not article_html:
                    continue
                text = extract_text(article_html, SETOPATI_SELECTORS)
                if text:
                    append_article({"text": text, "url": article_url, "source": "setopati", "domain": "news", "date_scraped": TODAY})
                    total += 1
                    cat_total += 1
                time.sleep(0.3)
        print(f"{cat_total} articles")
    return total

# ─────────────────────────────────────────
# NAGARIK NEWS
# ─────────────────────────────────────────
NAGARIK_CATEGORIES = ["news", "sports", "entertainment", "business", "opinion"]
NAGARIK_SELECTORS = ["div.news-content", "div.article-body", "div.content", "article"]

def scrape_nagarik(seen_urls):
    total = 0
    for cat in NAGARIK_CATEGORIES:
        print(f"  [{cat}]", end=" ", flush=True)
        cat_total = 0
        for page in range(1, 501):
            url = f"https://nagariknews.nagariknetwork.com/{cat}?page={page}"
            html = fetch(url)
            if not html:
                break
            soup = BeautifulSoup(html, "lxml")
            links = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if re.search(r'/\d{4}/\d{2}/', href):
                    full = href if href.startswith("http") else "https://nagariknews.nagariknetwork.com" + href
                    if full not in seen_urls:
                        links.append(full)
            if not links:
                break
            for article_url in links:
                seen_urls.add(article_url)
                save_seen_url(article_url)
                article_html = fetch(article_url)
                if not article_html:
                    continue
                text = extract_text(article_html, NAGARIK_SELECTORS)
                if text:
                    append_article({"text": text, "url": article_url, "source": "nagariknews", "domain": "news", "date_scraped": TODAY})
                    total += 1
                    cat_total += 1
                time.sleep(0.3)
        print(f"{cat_total} articles")
    return total

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
def main():
    seen_urls = load_seen_urls()
    print(f"Already seen: {len(seen_urls)} URLs")
    total = 0

    print(f"\n{'='*50}\nScraping: Ratopati")
    total += scrape_ratopati(seen_urls)
    print(f"Ratopati total: {total}")

    print(f"\n{'='*50}\nScraping: OnlineKhabar")
    t = scrape_onlinekhabar(seen_urls)
    total += t
    print(f"OnlineKhabar total: {t}")

    print(f"\n{'='*50}\nScraping: Ekantipur")
    t = scrape_kantipur(seen_urls)
    total += t
    print(f"Ekantipur total: {t}")

    print(f"\n{'='*50}\nScraping: Setopati")
    t = scrape_setopati(seen_urls)
    total += t
    print(f"Setopati total: {t}")

    print(f"\n{'='*50}\nScraping: Nagarik News")
    t = scrape_nagarik(seen_urls)
    total += t
    print(f"Nagarik total: {t}")

    print(f"\n{'='*50}")
    print(f"✅ Grand total new articles: {total}")
    print(f"💾 Saved to: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()