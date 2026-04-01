import os
from datetime import date

import duckdb

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YOUTUBE_CSV = os.path.join(BASE_DIR, "data", "youtube_comments_clean.csv")
IRIIS_CSV = os.path.join(BASE_DIR, "data", "iriisnepal_raw.csv")
WIKI_CSV = os.path.join(BASE_DIR, "data", "wikipedia_nepali.csv")
NEWS_CSV = os.path.join(BASE_DIR, "data", "nepali_news.csv")
OUT_DIR = os.path.join(BASE_DIR, "data", "merged")
TODAY = date.today().isoformat()

os.makedirs(OUT_DIR, exist_ok=True)

FULL_PATH = os.path.join(OUT_DIR, "nepali_corpus_full.parquet")
COLLOQUIAL_PATH = os.path.join(OUT_DIR, "nepali_corpus_colloquial.parquet")
FORMAL_PATH = os.path.join(OUT_DIR, "nepali_corpus_formal.parquet")
WIKI_PATH = os.path.join(OUT_DIR, "nepali_corpus_wikipedia.parquet")
ROMAN_PATH = os.path.join(OUT_DIR, "nepali_corpus_roman.parquet")
CODEMIXED_PATH = os.path.join(OUT_DIR, "nepali_corpus_codemixed.parquet")

con = duckdb.connect()
# These settings keep memory usage manageable on large files.
con.execute("PRAGMA threads = 2")
con.execute("PRAGMA preserve_insertion_order = false")
con.execute("PRAGMA memory_limit = '8GB'")
con.execute(f"PRAGMA temp_directory = '{os.path.join(OUT_DIR, 'duckdb_tmp')}'")

print("Building unified corpus with DuckDB...")
print("  YouTube:      {0}".format(YOUTUBE_CSV))
print("  Wikipedia:    {0}".format(WIKI_CSV))
print("  IRIISNEPAL:   {0}".format(IRIIS_CSV))
print("  News:         {0}".format(NEWS_CSV))

create_sql = f"""
CREATE OR REPLACE TEMP TABLE corpus AS
WITH youtube AS (
	-- YouTube is already cleaned and tagged in clean.py.
    SELECT
        text,
        'youtube_comments' AS source,
        'colloquial' AS domain,
        script,
        lang,
        '{TODAY}' AS date_collected,
        'CC BY 4.0' AS license
    FROM read_csv_auto('{YOUTUBE_CSV}', header=true)
    WHERE text IS NOT NULL AND trim(text) <> ''
),
wikipedia AS (
	-- Wikipedia gets fixed metadata because it is one source.
    SELECT
        text,
        'wikipedia_nepali' AS source,
        'encyclopedia' AS domain,
        'devanagari' AS script,
        'ne' AS lang,
        '{TODAY}' AS date_collected,
        'CC BY-SA 4.0' AS license
    FROM read_csv_auto('{WIKI_CSV}', header=true)
    WHERE text IS NOT NULL AND trim(text) <> ''
),
iriis AS (
	-- IRIIS is huge, so we stream it with read_csv_auto.
    SELECT
        Article AS text,
        'iriisnepal' AS source,
        'formal' AS domain,
        'devanagari' AS script,
        'ne' AS lang,
        '{TODAY}' AS date_collected,
        'MIT' AS license
    FROM read_csv_auto('{IRIIS_CSV}', header=true, ignore_errors=true)
    WHERE Article IS NOT NULL
      AND length(trim(Article)) > 0
      AND length(split(trim(Article), ' ')) >= 5
    AND regexp_matches(Article, '[ऀ-ॿ]')
),
news AS (
	-- News rows come from the local scraper CSV.
    SELECT
        text,
        source,
        'news' AS domain,
        CASE
            WHEN regexp_matches(text, '[ऀ-ॿ]') THEN 'devanagari'
            WHEN regexp_matches(text, '[A-Za-z]') THEN 'latin'
            ELSE 'other'
        END AS script,
        'ne' AS lang,
        '{TODAY}' AS date_collected,
        'source-dependent' AS license
    FROM read_csv_auto('{NEWS_CSV}', header=true)
    WHERE text IS NOT NULL AND trim(text) <> ''
),
combined AS (
    SELECT * FROM youtube
    UNION ALL SELECT * FROM wikipedia
    UNION ALL SELECT * FROM iriis
    UNION ALL SELECT * FROM news
)
SELECT * FROM combined
"""

print("Materializing unified corpus...")
con.execute(create_sql)


def copy(query: str, path: str) -> None:
	# Recreate output file so old parquet files do not linger.
    if os.path.exists(path):
        os.remove(path)
    con.execute(f"COPY ({query}) TO '{path}' (FORMAT PARQUET, COMPRESSION ZSTD)")
    size_mb = os.path.getsize(path) / (1024 * 1024)
    count = con.execute(f"SELECT count(*) FROM ({query})").fetchone()[0]
    print(f"  {os.path.basename(path):<32} {count:>12,} rows  {size_mb:>8.1f} MB")


print("Writing parquet outputs...")
# One full file + focused subsets for easier Hugging Face publishing.
copy("SELECT * FROM corpus", FULL_PATH)
copy("SELECT * FROM corpus WHERE domain = 'colloquial'", COLLOQUIAL_PATH)
copy("SELECT * FROM corpus WHERE domain = 'formal'", FORMAL_PATH)
copy("SELECT * FROM corpus WHERE domain = 'encyclopedia'", WIKI_PATH)
copy("SELECT * FROM corpus WHERE script = 'latin'", ROMAN_PATH)
copy("SELECT * FROM corpus WHERE script = 'mixed'", CODEMIXED_PATH)

print("\nFinal corpus stats")
stats = con.execute(
    """
    SELECT
        count(*) AS total_rows,
        sum(CASE WHEN domain = 'colloquial' THEN 1 ELSE 0 END) AS colloquial_rows,
        sum(CASE WHEN domain = 'formal' THEN 1 ELSE 0 END) AS formal_rows,
        sum(CASE WHEN domain = 'news' THEN 1 ELSE 0 END) AS news_rows,
        sum(CASE WHEN domain = 'encyclopedia' THEN 1 ELSE 0 END) AS wiki_rows
    FROM corpus
    """
).fetchone()
print(f"  Total rows:      {stats[0]:,}")
print(f"  Colloquial rows: {stats[1]:,}")
print(f"  Formal rows:     {stats[2]:,}")
print(f"  News rows:       {stats[3]:,}")
print(f"  Wiki rows:       {stats[4]:,}")

print("\nBy source")
print(con.execute("SELECT source, count(*) AS n FROM corpus GROUP BY source ORDER BY n DESC").df().to_string(index=False))

print("\nBy script")
print(con.execute("SELECT script, count(*) AS n FROM corpus GROUP BY script ORDER BY n DESC").df().to_string(index=False))

print("\nDone. Next: build the dataset card and publish to Hugging Face.")