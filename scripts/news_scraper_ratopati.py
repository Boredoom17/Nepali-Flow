import csv
import os
import re
from datetime import date

import requests
from bs4 import BeautifulSoup

OUTPUT_CSV = "data/nepali_news.csv"
SEEN_URLS_FILE = "data/seen_news_urls_ratopati.txt"
TODAY = date.today().isoformat()
SOURCE = "ratopati"
TARGET_TOTAL = 10000
DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ne,en;q=0.9",
}

RATOPATI_CATEGORIES = [
    "news",
    "politics",
    "economy",
    "society",
    "sports",
    "entertainment",
    "international",
    "technology",
    "health",
    "education",
    "province",
    "court-office",
    "crime",
]


def load_seen_urls():
    if os.path.exists(SEEN_URLS_FILE):
        with open(SEEN_URLS_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()


def save_seen_url(url):
    with open(SEEN_URLS_FILE, "a", encoding="utf-8") as f:
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


def fetch(url, timeout=12):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
        r.encoding = "utf-8"
        return r.text
    except Exception:
        return None


def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def has_nepali(text):
    return bool(DEVANAGARI_RE.search(text))


def extract_text(html):
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.find_all(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()

    selectors = [
        ("div", "dn__news--wrap"),
        ("div", "content-flex"),
        ("article", None),
        ("div", "article-content"),
    ]

    for tag_name, class_name in selectors:
        elem = soup.find(tag_name, class_=class_name) if class_name else soup.find(tag_name)
        if not elem:
            continue
        text = clean_text(elem.get_text(separator=" "))
        if len(text) > 120 and has_nepali(text):
            return text

    body = soup.find("body")
    if body:
        text = clean_text(body.get_text(separator=" "))
        if len(text) > 200 and has_nepali(text):
            return text

    return None


def get_existing_ratopati_stats():
    count = 0
    urls = set()

    if not os.path.exists(OUTPUT_CSV):
        return count, urls

    with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("source") == SOURCE:
                count += 1
                url = (row.get("url") or "").strip()
                if url:
                    urls.add(url)

    return count, urls


def scrape_ratopati(need_to_add):
    seen_urls = load_seen_urls()
    _, existing_urls = get_existing_ratopati_stats()
    seen_urls.update(existing_urls)

    added = 0
    print(f"Already tracked URLs ({SOURCE}): {len(seen_urls)}")
    print(f"Need to add: {need_to_add} articles")
    print("=" * 50)

    for category in RATOPATI_CATEGORIES:
        if added >= need_to_add:
            break

        category_added = 0
        print(f"\n[{SOURCE}/{category}]", end=" ", flush=True)

        for page_num in range(1, 501):
            if added >= need_to_add:
                break

            url = f"https://www.ratopati.com/category/{category}?page={page_num}"
            html = fetch(url)
            if not html:
                break

            soup = BeautifulSoup(html, "lxml")
            links = []

            for a in soup.find_all("a", href=True):
                href = a["href"]
                if re.search(r"/story/\d+", href):
                    full = href if href.startswith("http") else "https://www.ratopati.com" + href
                    if full not in seen_urls:
                        links.append(full)

            if not links:
                break

            local_seen = set()
            for article_url in links:
                if article_url in local_seen:
                    continue
                local_seen.add(article_url)

                if added >= need_to_add:
                    break

                article_html = fetch(article_url)
                if not article_html:
                    continue

                text = extract_text(article_html)
                if not text:
                    continue

                append_article(
                    {
                        "text": text,
                        "url": article_url,
                        "source": SOURCE,
                        "domain": "news",
                        "date_scraped": TODAY,
                    }
                )
                seen_urls.add(article_url)
                save_seen_url(article_url)
                added += 1
                category_added += 1

                if added % 20 == 0 or added == need_to_add:
                    print(f"\nSaved {added}/{need_to_add}", end=" ", flush=True)

        print(f"| {category_added} added", flush=True)

    return added


def main():
    os.makedirs("data", exist_ok=True)

    existing_count, _ = get_existing_ratopati_stats()
    need_to_add = TARGET_TOTAL - existing_count

    print(f"Current {SOURCE}: {existing_count}")
    print(f"Target {SOURCE}: {TARGET_TOTAL}")

    if need_to_add <= 0:
        print("Already at or above target. Nothing to scrape.")
        return

    added = scrape_ratopati(need_to_add)
    final_count = existing_count + added

    print("\n" + "=" * 50)
    print(f"Added: {added}")
    print(f"Final {SOURCE}: {final_count}")


if __name__ == "__main__":
    main()
