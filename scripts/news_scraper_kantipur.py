import os
import csv
import time
import requests
import re
from bs4 import BeautifulSoup
from datetime import date, timedelta

OUTPUT_CSV = "data/nepali_news.csv"
SEEN_URLS_FILE = "data/seen_news_urls.txt"
TODAY = date.today().isoformat()
DEVANAGARI_RE = re.compile(r'[\u0900-\u097F]')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ne,en;q=0.9",
}

# Utility helpers
def load_seen_urls():
    # Load previous URLs so reruns continue instead of starting from zero.
    if os.path.exists(SEEN_URLS_FILE):
        with open(SEEN_URLS_FILE, "r") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_seen_url(url):
    # Save each seen URL immediately so progress is not lost.
    with open(SEEN_URLS_FILE, "a") as f:
        f.write(url + "\n")

def append_article(row):
    # Append mode keeps adding new rows to the same corpus file.
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
    # Return None on errors so crawler can skip and keep moving.
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
    # Remove noisy layout tags before extracting readable body text.
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

def scrape_and_save(article_url, source, selectors, seen_urls):
    # Skip already seen links, then fetch and save if text extraction works.
    if article_url in seen_urls:
        return False
    seen_urls.add(article_url)
    save_seen_url(article_url)
    article_html = fetch(article_url)
    if not article_html:
        return False
    text = extract_text(article_html, selectors)
    if text:
        append_article({
            "text": text,
            "url": article_url,
            "source": source,
            "domain": "news",
            "date_scraped": TODAY
        })
        return True
    return False

# Kantipur scraping settings
KANTIPUR_CATEGORIES = [
    "news", "province", "international", "sports",
    "entertainment", "business", "opinion", "health", "technology",
]
KANTIPUR_SELECTORS = ["div.news-inner-wrapper", "div.description", "article"]
DAYS_BACK = 365 * 3  # 3 years

def get_kantipur_links_from_page(html):
    # Keep only article links that match Kantipur's dated URL pattern.
    soup = BeautifulSoup(html, "lxml")
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if re.search(r'/\d{4}/\d{2}/\d{2}/.*\.html', href):
            full = href if href.startswith("http") else "https://ekantipur.com" + href
            links.add(full)
    return links

def scrape_kantipur(seen_urls):
    total = 0
    for cat in KANTIPUR_CATEGORIES:
        print(f"  [kantipur/{cat}]", end=" ", flush=True)
        cat_total = 0

        # First collect from the main category page.
        html = fetch(f"https://ekantipur.com/{cat}")
        if html:
            for article_url in get_kantipur_links_from_page(html):
                if scrape_and_save(article_url, "kantipur", KANTIPUR_SELECTORS, seen_urls):
                    total += 1
                    cat_total += 1
                time.sleep(0.1)

        # Then walk back by date.
        consecutive_empty_days = 0
        for days_ago in range(0, DAYS_BACK):
            d = date.today() - timedelta(days=days_ago)
            html = fetch(f"https://ekantipur.com/{cat}/{d.year}/{d.month:02d}/{d.day:02d}/")
            if not html:
                # Stop date walk after many empty days in a row.
                consecutive_empty_days += 1
                if consecutive_empty_days >= 10:
                    break
                continue

            new_links = [u for u in get_kantipur_links_from_page(html) if u not in seen_urls]
            if not new_links:
                consecutive_empty_days += 1
                if consecutive_empty_days >= 10:
                    break
                continue

            consecutive_empty_days = 0
            for article_url in new_links:
                if scrape_and_save(article_url, "kantipur", KANTIPUR_SELECTORS, seen_urls):
                    total += 1
                    cat_total += 1
                time.sleep(0.1)

        print(f"{cat_total} articles")
    return total

# Main entry point
def main():
    os.makedirs("data", exist_ok=True)

    # Keep this script resumable by loading previous seen URLs.
    seen_urls = load_seen_urls()
    print(f"[kantipur] Already seen: {len(seen_urls)} URLs")

    print(f"\n{'='*50}\nScraping: Kantipur")
    t = scrape_kantipur(seen_urls)
    print(f"\nKantipur total: {t}")
    print(f"Saved to: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()