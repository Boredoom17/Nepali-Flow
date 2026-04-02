# How I Built This Corpus

This document explains how the data was collected, cleaned, and organized.

## The Simple Version

I took 4 different sources, cleaned them up, tagged each row with metadata, and merged everything into one big parquet file that's easy to load.

```
Raw CSVs → Tag & Clean → Merge → Parquet files
```

## Where the Data Comes From

| Source | Rows | Notes |
|--------|------|-------|
| IRIISNEPAL | 6.1M | Curated formal Nepali |
| YouTube | 431K | Real comments |
| Wikipedia | 291K | Articles |
| News sites | 87K | Recent articles |

## What I Did to Clean It

1. **Removed empty rows** — Got rid of null/blank entries
2. **Filtered by length** — Kept rows with at least 5 words for formal text
3. **Checked the script** — Identified if text was Devanagari, Latin, or mixed
4. **Added metadata** — Tagged each row with: source, domain, script, language, date, license

## What Each Row Gets

```
text              — the actual text
source            — where it came from (e.g., "iriisnepal", "youtube_comments")
domain            — type of text (formal, colloquial, encyclopedia, news)
script            — writing system (devanagari, latin, mixed)
lang              — language code (ne for Nepali, ne-roman for Roman Nepali)
date_collected    — when it was processed
license           — which license applies
```

## The Output Files

All four datasets are parquet files (compressed, efficient):

- **nepali_corpus_full.parquet** (5.0 GB)
  - Everything combined
  - 7.1M rows
  - Ordered: formal first, then encyclopedia, news, colloquial

- **nepali_corpus_formal.parquet** (4.9 GB)
  - Formal + Wikipedia + news
  - 6.3M rows
  - Best for language model training

- **nepali_corpus_colloquial.parquet** (16 MB)
  - YouTube comments
  - 431K rows
  - Real, informal speech

- **nepali_corpus_roman.parquet** (9.0 MB)
  - Latin-script only
  - 307K rows
  - Roman Nepali subset

## Why DuckDB?

I used DuckDB because it's fast, handles large files, and doesn't need a database server. All code is in [scripts/merge.py](../scripts/merge.py).

## What I Didn't Do

- **Deduplication:** I didn't remove similar rows because real speech has repetition
- **Heavy filtering:** Some YouTube comments are messy on purpose—that's real data
- **Rebalancing:** Kept the natural distribution of sources

## If You Want to Rebuild This

```bash
python scripts/merge.py
```

It will regenerate all parquet files from the raw CSVs.

## Known Issues

- Some Wikipedia rows have odd formatting (extraction artifacts)
- News articles have varying publish dates
- YouTube comments are raw—no content filtering
- Roman Nepali spelling is all over the place (on purpose)

---

**Built:** April 2, 2026

**Ordering:** Devanagari (longest first) → Latin → Mixed (ensures Hugging Face viewer surfaces Devanagari examples first)

### nepali_corpus_roman.parquet
**Purpose:** Roman-script Nepali subset  
**Rows:** 307,999 (latin script from YouTube)  
**Derived from:** Colloquial corpus with `script = 'latin'`

### nepali_corpus_wikipedia.parquet
**Purpose:** Encyclopedia-style Nepali (NOT published separately; kept for analysis)  
**Rows:** 291,767  
**Note:** Wikipedia data is merged into `nepali_corpus_formal.parquet` for public release.

## Performance Optimizations

### DuckDB Configuration
```sql
PRAGMA threads = 2              -- CPU parallelism
PRAGMA preserve_insertion_order = false
PRAGMA memory_limit = '8GB'     -- RAM cap
PRAGMA temp_directory = '...'   -- Disk spillover
```

### Parquet Compression
- **Codec:** Zstandard (ZSTD)
- **Compression Level:** Default (best balance)
- **Result:** 5.95 GB file for 7.1M rows (≈850 bytes/row average)

### Processing Speed
- Typical merge run: ~2-5 minutes on 8GB RAM
- DuckDB streaming keeps memory footprint constant

## Quality Metrics

### Content Representation
- **Formal (88%):** Academic, journalistic, encyclopedic content
- **Colloquial (6%):** Conversational, social media discourse
- **Roman script (4%):** Transliterated Nepali
- **Mixed script (<1%):** Code-switching examples

### Text Statistics
- **Average length:** ~120 UTF-8 characters
- **Median length:** ~85 characters
- **Max length:** ~50,000 characters (rare outliers)
- **Devanagari percentage:** ~87% of rows

### Coverage
- **Unique sources:** 5 primary (IRIIS, Wikipedia, YouTube, Kantipur, Setopati, +3 others)
- **Time span:** Circa 2016–2026 (mixed historical and current)
- **Geographic scope:** Nepal-centric; diaspora content included in YouTube

## Maintenance & Updates

### Incremental Updates
To add new data:
1. Append new rows to source CSV (e.g., `nepali_news.csv`)
2. Re-run `scripts/merge.py`
3. Output parquets are regenerated from scratch
4. Run `scripts/publish.py` to sync to Hugging Face

### Re-running the Pipeline
```bash
cd /Users/ad/research/nepali-text
venv/bin/python scripts/merge.py
```

## Schema Reference

All parquet files use this schema:

| Column | Type | Description |
|--------|------|-------------|
| text | string | UTF-8 Nepali text |
| source | string | Data source identifier |
| domain | string | Content type (formal, colloquial, encyclopedia, news) |
| script | string | Writing system (devanagari, latin, mixed) |
| lang | string | ISO 639-1 language code (always 'ne') |
| date_collected | string | ISO 8601 processing date |
| license | string | Source license (MIT, CC BY 4.0, CC BY-SA 4.0, source-dependent) |

---

**Last Updated:** April 2, 2026  
**Pipeline Version:** 1.0  
**Maintainer:** Aadarsha Chhetri
