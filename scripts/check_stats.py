import pandas as pd
import os

print("NEPALI TEXT CORPUS - DOWNLOAD STATUS\n")
print("="*60)

# YouTube
if os.path.exists("data/youtube_comments_clean.csv"):
    df = pd.read_csv("data/youtube_comments_clean.csv")
    print(f"YouTube Comments: {len(df):,} rows")
else:
    print("YouTube Comments: NOT FOUND")

# Wikipedia
if os.path.exists("data/wikipedia_nepali.csv"):
    df = pd.read_csv("data/wikipedia_nepali.csv")
    print(f"Wikipedia: {len(df):,} rows")
else:
    print("Wikipedia: NOT FOUND")

# IRIISNEPAL (chunked count)
if os.path.exists("data/iriisnepal_raw.csv"):
    count = 0
    for chunk in pd.read_csv("data/iriisnepal_raw.csv", chunksize=100000):
        count += len(chunk)
    print(f"IRIISNEPAL: {count:,} rows")
else:
    print("IRIISNEPAL: NOT FOUND")

# News
if os.path.exists("data/nepali_news.csv"):
    df = pd.read_csv("data/nepali_news.csv")
    print(f"News Scraper: {len(df):,} rows")
    print("\n   News breakdown by source:")
    for source, count in df['source'].value_counts().items():
        print(f"      {source}: {count:,}")
else:
    print("News Scraper: NOT FOUND")

# Seen URLs
if os.path.exists("data/seen_news_urls.txt"):
    with open("data/seen_news_urls.txt") as f:
        seen = len(f.readlines())
    print(f"\nSeen news URLs: {seen:,}")

print("\n" + "="*60)
