# Data Processing Pipeline

This document describes the technical workflow for constructing and maintaining the Nepali Text Corpus.

## Overview

The corpus is built using a DuckDB-based pipeline (`scripts/merge.py`) that ingests raw CSVs, applies filtering and normalization, and produces stratified parquet outputs optimized for different research domains.

```
Raw Data (CSV) → Validation & Normalization → Domain Stratification → Parquet Output
```

## Input Sources

| Source | File | Format | Records | Notes |
|--------|------|--------|---------|-------|
| IRIISNEPAL | `iriisnepal_raw.csv` | CSV | ~6.1M | Manually curated formal Nepali |
| YouTube | `youtube_comments_clean.csv` | CSV | ~431K | Pre-cleaned by `clean.py` |
| Wikipedia | `wikipedia_nepali.csv` | CSV | ~291K | Extracted from wiki dump |
| News | `nepali_news.csv` | CSV | ~87K | Scraped from live news feeds |

## Preprocessing Steps

### 1. Text Validation
All records are filtered on:
- **Non-null check:** `text IS NOT NULL`
- **Non-empty check:** `trim(text) <> ''`
- **Minimum length (IRIIS only):** `length(split(trim(text), ' ')) >= 5` (5+ words)
- **Script validation (IRIIS only):** Must contain at least one Devanagari character

### 2. Script Detection
Automatic classification for news and YouTube sources:
```
IF text contains [ऀ-ॿ] THEN 'devanagari'
ELSE IF text contains [A-Za-z] THEN 'latin'
ELSE 'other'
```

### 3. Metadata Assignment
Each row is enriched with:
- **source:** Origin identifier (e.g., `iriisnepal`, `youtube_comments`, `wikipedia_nepali`)
- **domain:** Content category (formal, colloquial, encyclopedia, news)
- **script:** Writing system detected
- **lang:** ISO 639-1 code (`ne` for Nepali)
- **date_collected:** Processing date
- **license:** Source-specific license

### 4. Deduplication
- No exact-duplicate removal (preserves all unique utterances)
- Partial duplicates retained (colloquial speech naturally repeats common phrases)

## Output Datasets

### nepali_corpus_full.parquet
**Purpose:** Complete merged corpus for general research  
**Rows:** 7,167,456  
**Ordering:**
1. Formal domain (IRIISNEPAL)
2. Encyclopedia domain (Wikipedia)
3. News domain
4. Colloquial domain (YouTube)

Within each domain, ordered by `source`, then `length DESC` for visibility.

### nepali_corpus_formal.parquet
**Purpose:** Formal writing for LM pretraining  
**Rows:** 6,378,206 (formal + encyclopedia + news)  
**Domains included:** `formal`, `encyclopedia`, `news`  
**Ordering:** Domain priority → source → length DESC

**Professional dataset preview:** Leading rows are formal Wikipedia and news articles (clean, representative examples).

### nepali_corpus_colloquial.parquet
**Purpose:** Conversational Nepali for sociolinguistic analysis  
**Rows:** 431,648 (YouTube comments only)  
**Script distribution:**
- Devanagari: 123,804 comments
- Latin (Roman): 307,999 comments
- Mixed: 19,845 comments

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

## Known Limitations

1. **YouTube content:** No content filtering; raw comments may contain offensive language
2. **News licensing:** Publisher permissions uncertain; use cautiously in commercial settings
3. **Script detection:** Simple regex-based; mixed-language text occasionally misclassified
4. **Deduplication:** No semantic deduplication; similar paraphrases retained
5. **Temporal bias:** Majority of data from 2020–2026; pre-2020 IRIIS content underrepresented

## Future Improvements

- [ ] Semantic deduplication using embeddings
- [ ] Fine-grained toxicity filtering for colloquial subset
- [ ] Add date ranges per source for temporal filtering
- [ ] Multilingual metadata (code-mixed Hindi, English)
- [ ] Validation splits for supervised task benchmarking

---

**Last Updated:** April 2, 2026  
**Pipeline Version:** 1.0  
**Maintainer:** Boredoom17
