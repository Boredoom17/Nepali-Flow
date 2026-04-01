import os
import csv
import re
from bs4 import BeautifulSoup
from datetime import date
from playwright.sync_api import sync_playwright

OUTPUT_CSV = "data/nepali_news.csv"
SEEN_URLS_FILE = "data/seen_news_urls_setopati.txt"
TODAY = date.today().isoformat()
DEVANAGARI_RE = re.compile(r'[\u0900-\u097F]')

TARGET = 10000

SETOPATI_CATEGORIES = [
    "politics", "social", "opinion", "sports",
    "global", "art", "exclusive", "cover-story",
]

# Utility helpers
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
            quoting=csv.QUOTE_ALL,
        )
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def has_nepali(text):
    return bool(DEVANAGARI_RE.search(text))

def is_article_url(href):
    if not href:
        return None
    if href.startswith("/"):
        href = "https://www.setopati.com" + href
    if "setopati.com" not in href:
        return None
    # Accept normal article links and /detail/ links.
    if re.search(r'/\d{5,}', href) or '/detail/' in href:
        return href
    return None

def extract_text(html):
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.find_all(["script", "style", "nav", "header", "footer"]):
        tag.decompose()
    
    # First try the content-editor section used on many Setopati pages.
    section = soup.find("section", class_="content-editor")
    if section:
        text = clean_text(section.get_text(separator=" "))
        if len(text) > 100 and has_nepali(text):
            return text
    
    # Then try a few common article containers.
    selectors = [("div", "news-content"), ("article", None), ("div", "content"), ("div", "article-body")]
    for tag_name, class_name in selectors:
        elem = soup.find(tag_name, class_=class_name) if class_name else soup.find(tag_name)
        if elem:
            text = clean_text(elem.get_text(separator=" "))
            if len(text) > 100 and has_nepali(text):
                return text
    
    # If everything else fails, use body text as a fallback.
    body = soup.find("body")
    if body:
        text = clean_text(body.get_text(separator=" "))
        if len(text) > 200 and has_nepali(text):
            return text
    
    return None
def scrape_and_save(page, url, seen_urls):
    # Skip URLs we already processed in previous runs.
    if url in seen_urls:
        return False
    seen_urls.add(url)
    save_seen_url(url)
    
    try:
        # Playwright is used here because Setopati pages can be dynamic.
        page.goto(url, wait_until='domcontentloaded', timeout=8000)
        html = page.content()
    except:
        return False
    
    text = extract_text(html)
    if text:
        append_article({
            "text": text,
            "url": url,
            "source": "setopati",
            "domain": "news",
            "date_scraped": TODAY,
        })
        return True
    return False

def crawl():
    # This scraper is resumable because we keep seen URLs in a text file.
    os.makedirs("data", exist_ok=True)
    seen_urls = load_seen_urls()
    total = 0
    
    print(f"Already seen: {len(seen_urls)} URLs")
    print(f"Target: {TARGET}")
    print("=" * 50)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Loop categories first, then paginate each category.
        for cat in SETOPATI_CATEGORIES:
            if total >= TARGET:
                break
            
            print(f"\n[{cat}]", end=" ", flush=True)
            cat_total = 0
            no_links_count = 0
            
            for pg_num in range(1, 500):
                if total >= TARGET:
                    break

                url = f"https://www.setopati.com/{cat}?page={pg_num}"
                try:
                    page.goto(url, wait_until='domcontentloaded', timeout=8000)
                    html = page.content()
                except Exception as e:
                    print(f"\n  Error loading page {pg_num}: {str(e)[:30]}", end=" ", flush=True)
                    no_links_count += 1
                    if no_links_count > 3:
                        break
                    continue

                soup = BeautifulSoup(html, "lxml")
                links = []
                for a in soup.find_all("a", href=True):
                    full = is_article_url(a["href"])
                    if full and full not in seen_urls:
                        links.append(full)

                if not links:
                    no_links_count += 1
                    # Stop this category after several empty pages in a row.
                    if no_links_count > 5:
                        print(f"| {cat_total} articles", flush=True)
                        break
                    continue
                
                no_links_count = 0
                
                for link in links:
                    if total >= TARGET:
                        break
                    if scrape_and_save(page, link, seen_urls):
                        total += 1
                        cat_total += 1
                        if total % 20 == 0:
                            print(f"\nSaved {total}/{TARGET}", end=" ", flush=True)
        
        browser.close()
    
    print("\n" + "=" * 50)
    print(f"Final: {total} articles saved")

if __name__ == "__main__":
    crawl()



    