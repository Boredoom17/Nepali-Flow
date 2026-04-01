import csv
import os
import re
from collections import deque
from datetime import date, datetime, timedelta
from urllib.parse import urljoin, urlparse, parse_qs, unquote

import requests
from bs4 import BeautifulSoup

OUTPUT_CSV = "data/nepali_news.csv"
SEEN_ARTICLE_FILE = "data/seen_news_urls_nagariknews.txt"
SEEN_PAGE_FILE = "data/seen_pages_nagariknews.txt"

SOURCE = "nagariknews"
DOMAIN = "nagariknews.nagariknetwork.com"
TODAY = date.today().isoformat()
TARGET_TOTAL = 10000
YEARS_BACK = 3

DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")
DATE_PUBLISHED_RE = re.compile(r'"datePublished"\s*:\s*"([^"]+)"')

HEADERS = {
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
	"Accept-Language": "ne,en;q=0.9",
}

SEED_PATHS = [
	"/",
	"/main-news",
	"/politics",
	"/social-affairs",
	"/economy",
	"/arts",
	"/sports",
	"/opinion",
	"/international",
	"/health",
	"/technology",
	"/education",
	"/others",
	"/diaspora",
]


def load_seen(file_path):
	if os.path.exists(file_path):
		with open(file_path, "r", encoding="utf-8") as f:
			return set(line.strip() for line in f if line.strip())
	return set()


def save_seen(file_path, value):
	with open(file_path, "a", encoding="utf-8") as f:
		f.write(value + "\n")


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


def get_existing_source_stats():
	count = 0
	urls = set()

	if not os.path.exists(OUTPUT_CSV):
		return count, urls

	with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
		reader = csv.DictReader(f)
		for row in reader:
			if row.get("source") == SOURCE:
				count += 1
				u = (row.get("url") or "").strip()
				if u:
					urls.add(normalize_url(u))

	return count, urls


def fetch(url, timeout=8):
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


def normalize_url(url):
	url = url.split("#", 1)[0]
	url = url.split("?", 1)[0]
	return url.rstrip("/")


def same_domain(url):
	try:
		return urlparse(url).netloc == DOMAIN
	except Exception:
		return False


def extract_embedded_article_url(url):
	"""Extract article URL from social share links (Facebook u= or Twitter text= parameters)."""
	try:
		parsed = urlparse(url)
		# Facebook share links: u=https://...article.html
		if "facebook.com/sharer" in url:
			params = parse_qs(parsed.query)
			if "u" in params:
				embedded = unquote(params["u"][0])
				if embedded.startswith("http"):
					return embedded
		# Twitter share links: text=Visit https://...article.html
		if "twitter.com/intent/tweet" in url:
			params = parse_qs(parsed.query)
			if "text" in params:
				text = unquote(params["text"][0])
				# Extract URL from text like "Visit https://..."
				import re as regex_module
				match = regex_module.search(r'https?://[^\s]+', text)
				if match:
					return match.group(0)
		return None
	except Exception:
		return None


def is_article_url(url):
	if not url or not same_domain(url):
		return False
	path = urlparse(url).path.lower()

	if not path.endswith(".html"):
		return False
	if any(bad in path for bad in ["/author/", "/tag/", "/trending/", "/video/"]):
		return False
	return True


def is_crawlable_page(url):
	if not url or not same_domain(url):
		return False
	path = urlparse(url).path.lower()

	if any(path.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".pdf", ".mp4"]):
		return False
	if any(bad in path for bad in ["/author/", "/plans", "/epapers"]):
		return False
	return True


def extract_published_date(html):
	m = DATE_PUBLISHED_RE.search(html)
	if not m:
		return None
	raw = m.group(1)
	try:
		return datetime.fromisoformat(raw)
	except Exception:
		return None


def within_time_window(dt, years=YEARS_BACK):
	if not dt:
		return True

	# Keep timezone handling consistent with parsed datePublished values.
	if dt.tzinfo is not None:
		cutoff = datetime.now(dt.tzinfo) - timedelta(days=365 * years)
	else:
		cutoff = datetime.now() - timedelta(days=365 * years)

	return dt >= cutoff


def extract_text(html):
	soup = BeautifulSoup(html, "lxml")
	for tag in soup.find_all(["script", "style", "nav", "header", "footer", "aside"]):
		tag.decompose()

	selectors = [
		("article", None),
		("div", "content"),
		("div", "news-content"),
		("div", "article-body"),
	]

	for tag_name, cls in selectors:
		node = soup.find(tag_name, class_=cls) if cls else soup.find(tag_name)
		if not node:
			continue
		text = clean_text(node.get_text(separator=" "))
		if len(text) > 120 and has_nepali(text):
			return text

	body = soup.find("body")
	if body:
		text = clean_text(body.get_text(separator=" "))
		if len(text) > 250 and has_nepali(text):
			return text

	return None


def discover_links(html, base_url):
	soup = BeautifulSoup(html, "lxml")
	article_links = []
	crawl_links = []

	for a in soup.find_all("a", href=True):
		href = a.get("href", "").strip()
		if not href:
			continue

		full = normalize_url(urljoin(base_url, href))
		if not same_domain(full):
			# Try to extract embedded article URL from social share links
			embedded = extract_embedded_article_url(full)
			if embedded and same_domain(embedded):
				embedded = normalize_url(embedded)
				if is_article_url(embedded):
					article_links.append(embedded)
			continue

		if is_article_url(full):
			article_links.append(full)
		elif is_crawlable_page(full):
			crawl_links.append(full)

	# Keep insertion order while deduplicating.
	article_links = list(dict.fromkeys(article_links))
	crawl_links = list(dict.fromkeys(crawl_links))
	return article_links, crawl_links


def scrape_nagarik(need_to_add):
	seen_articles = load_seen(SEEN_ARTICLE_FILE)
	seen_pages = load_seen(SEEN_PAGE_FILE)
	_, existing_urls = get_existing_source_stats()
	seen_articles.update(existing_urls)

	queue = deque([f"https://{DOMAIN}{p}" for p in SEED_PATHS])
	added = 0
	pages_scanned = 0
	max_pages = 5000

	print(f"Need to add: {need_to_add}")
	print(f"Already tracked articles: {len(seen_articles)}")
	print(f"Already tracked pages: {len(seen_pages)}")
	print("=" * 50)

	while queue and added < need_to_add and pages_scanned < max_pages:
		page_url = normalize_url(queue.popleft())
		if page_url in seen_pages:
			continue

		seen_pages.add(page_url)
		pages_scanned += 1

		html = fetch(page_url)
		if not html:
			continue

		article_links, crawl_links = discover_links(html, page_url)

		if article_links:
			print(f"  Found {len(article_links)} article links on page", flush=True)

		# Only add crawl links if queue isn't too large (prevents infinite crawling)
		if len(queue) < 500:
			for u in crawl_links:
				if u not in seen_pages:
					queue.append(u)

		batch_saves = []
		for article_url in article_links:
			if added >= need_to_add:
				break
			if article_url in seen_articles:
				continue

			article_html = fetch(article_url)
			if not article_html:
				print(f"  Failed to fetch: {article_url[:60]}...", flush=True)
				continue

			published_dt = extract_published_date(article_html)
			if not within_time_window(published_dt, YEARS_BACK):
				seen_articles.add(article_url)
				batch_saves.append(article_url)
				print(f"  Outside time window: {published_dt}", flush=True)
				continue

			text = extract_text(article_html)
			if not text:
				print(f"  No text extracted: {article_url[:60]}...", flush=True)
				seen_articles.add(article_url)
				batch_saves.append(article_url)
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
			seen_articles.add(article_url)
			batch_saves.append(article_url)
			added += 1

			if added % 20 == 0 or added == need_to_add:
				print(f"Saved {added}/{need_to_add} | pages scanned: {pages_scanned} | queue: {len(queue)}", flush=True)
		
		# Batch write seen URLs
		for url in batch_saves:
			save_seen(SEEN_ARTICLE_FILE, url)
		
		# Save page after processing (batch friendly)
		if pages_scanned % 10 == 0:
			save_seen(SEEN_PAGE_FILE, page_url)

	return added, pages_scanned, len(queue)


def main():
	os.makedirs("data", exist_ok=True)

	existing_count, _ = get_existing_source_stats()
	need_to_add = TARGET_TOTAL - existing_count

	print(f"Current {SOURCE}: {existing_count}")
	print(f"Target {SOURCE}: {TARGET_TOTAL}")

	if need_to_add <= 0:
		print("Already at or above target. Nothing to scrape.")
		return

	added, pages_scanned, queue_left = scrape_nagarik(need_to_add)
	final_count = existing_count + added

	print("\n" + "=" * 50)
	print(f"Added this run: {added}")
	print(f"Final {SOURCE}: {final_count}")
	print(f"Pages scanned: {pages_scanned}")
	print(f"Queue remaining: {queue_left}")
	if final_count == TARGET_TOTAL:
		print("Reached exactly 10,000 nagariknews articles.")
	else:
		print("Stopped before exact target. Rerun to continue from saved progress.")


if __name__ == "__main__":
	main()
