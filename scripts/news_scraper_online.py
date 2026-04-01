import os
import csv
import re
from datetime import date

import requests
from bs4 import BeautifulSoup

OUTPUT_CSV = "data/nepali_news.csv"
SEEN_URLS_FILE = "data/seen_news_urls_onlinekhabar.txt"
TODAY = date.today().isoformat()

SOURCE = "onlinekhabar"
TARGET_TOTAL = 10000
DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")

HEADERS = {
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
	"Accept-Language": "ne,en;q=0.9",
}




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


def fetch(url, timeout=15):
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
	"""Extract text from OnlineKhabar article with multiple fallback selectors"""
	soup = BeautifulSoup(html, "lxml")
	for tag in soup.find_all(["script", "style", "nav", "header", "footer", "aside"]):
		tag.decompose()

	# Try specific content selectors (old and new versions)
	selectors = [
		("div", "ok18-single-post-content-wrap"),
		("div", "ok-news-post"),
		("div", "single-post-content"),
		("div", "content-wrapper"),
		("article", None),
		("div", "article-content"),
		("div", "post-content"),
		("div", "entry-content"),
		("div", "content"),
	]

	for tag_name, class_name in selectors:
		if class_name:
			elem = soup.find(tag_name, class_=class_name)
		else:
			elem = soup.find(tag_name)
		if elem:
			text = clean_text(elem.get_text(separator=" "))
			if len(text) > 100 and has_nepali(text):
				return text

	# Fallback: try all divs with article-like classes
	for div in soup.find_all("div", class_=re.compile(r"(content|article|post|entry|story|news).*", re.I)):
		text = clean_text(div.get_text(separator=" "))
		if len(text) > 120 and has_nepali(text):
			return text

	# Last resort: get body text
	body = soup.find("body")
	if body:
		text = clean_text(body.get_text(separator=" "))
		if len(text) > 150 and has_nepali(text):
			return text

	return None


def get_existing_onlinekhabar_stats():
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


def scrape_onlinekhabar(need_to_add):
	seen_urls = load_seen_urls()
	_, existing_urls = get_existing_onlinekhabar_stats()
	seen_urls.update(existing_urls)

	added = 0
	print(f"Already tracked URLs ({SOURCE}): {len(seen_urls)}")
	print(f"Need to add: {need_to_add} articles")
	print("=" * 50)

	categories = [
		"politics", "economy", "sports", "entertainment", "health",
		"technology", "education", "international", "culture", "business",
		"lifestyle", "travel", "food", "opinion", "news",
	]

	for cat in categories:
		if added >= need_to_add:
			break

		print(f"\n[{SOURCE}/{cat}]", end=" ", flush=True)
		cat_added = 0
		empty_pages = 0

		# Paginate within each category
		for page_num in range(1, 201):  # Try up to 200 pages per category
			if added >= need_to_add:
				break

			# Break if too many consecutive empty pages
			if empty_pages >= 3:
				break

			cat_url = f"https://www.onlinekhabar.com/{cat}/?page={page_num}"
			html = fetch(cat_url)
			if not html:
				break

			soup = BeautifulSoup(html, "lxml")
			raw_links = []

			# Extract all article links from the page
			for a in soup.find_all("a", href=True):
				href = a["href"]
				# Match OnlineKhabar article URL pattern
				if re.search(r"/\d{4}/\d{2}/\d+/", href):
					full = href if href.startswith("http") else "https://www.onlinekhabar.com" + href
					raw_links.append(full)

			# Deduplicate
			links = []
			local_seen = set()
			for u in raw_links:
				if u not in local_seen and u not in seen_urls:
					local_seen.add(u)
					links.append(u)

			# If no raw links at all, we've hit the end of this category
			if not raw_links:
				break

			# If all links are seen, continue pagination
			if not links:
				empty_pages += 1
				continue

			page_added_before = added

			for article_url in links:
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
				cat_added += 1

				if added % 20 == 0 or added == need_to_add:
					print(f"\nSaved {added}/{need_to_add}", end=" ", flush=True)

			# Track if this page added anything
			if added == page_added_before:
				empty_pages += 1
			else:
				empty_pages = 0

		print(f"| {cat_added} added", flush=True)

	return added


def main():
	os.makedirs("data", exist_ok=True)

	existing_count, _ = get_existing_onlinekhabar_stats()
	need_to_add = TARGET_TOTAL - existing_count

	print(f"Current {SOURCE}: {existing_count}")
	print(f"Target {SOURCE}: {TARGET_TOTAL}")

	if need_to_add <= 0:
		print(f"Already at or above target. Nothing to scrape.")
		return

	added = scrape_onlinekhabar(need_to_add)
	final_count = existing_count + added

	print("\n" + "=" * 50)
	print(f"Added: {added}")
	print(f"Final {SOURCE}: {final_count}")
	if final_count == TARGET_TOTAL:
		print("Reached exactly 10,000 onlinekhabar articles.")
	else:
		print("Stopped before exact target; rerun to continue from saved progress.")


if __name__ == "__main__":
	main()
