<div align="center">

# Nepali Text Corpus
### Large-Scale Nepali Dataset Suite for NLP Research

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![DuckDB](https://img.shields.io/badge/DuckDB-Data%20Engine-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)](https://duckdb.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![HuggingFace](https://img.shields.io/badge/Hugging%20Face-Datasets-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/datasets)
[![License](https://img.shields.io/badge/License-Mixed-orange?style=for-the-badge)](readmes/LICENSE.md)

**Collect Data** • **Merge at Scale** • **Publish to Hugging Face**

---

</div>

## Overview

This project builds and maintains a large Nepali text corpus from multiple real-world sources: formal articles, encyclopedia text, news writing, and colloquial social-media language.

The pipeline is built for practical research use. You can scrape/collect sources, clean them, merge everything with DuckDB, and publish curated subsets directly to Hugging Face.

Current structure follows four primary public datasets:

- Full corpus: everything combined
- Formal corpus: IRIISNEPAL + Wikipedia + Nepali news
- Colloquial corpus: YouTube comments (informal speech)
- Roman corpus: Latin-script Nepali subset

## Hugging Face Datasets

- [Boredoom17/nepali-text-corpus](https://huggingface.co/datasets/Boredoom17/nepali-text-corpus)
- [Boredoom17/nepali-formal-corpus](https://huggingface.co/datasets/Boredoom17/nepali-formal-corpus)
- [Boredoom17/nepali-colloquial-corpus](https://huggingface.co/datasets/Boredoom17/nepali-colloquial-corpus)
- [Boredoom17/roman-nepali-corpus](https://huggingface.co/datasets/Boredoom17/roman-nepali-corpus)

## Key Features

- Source-aware merge pipeline with row-level metadata
- Domain split support (formal, encyclopedia, news, colloquial)
- Script tagging (Devanagari, Latin, mixed)
- Large-file handling via DuckDB + parquet
- Reproducible publication workflow for Hugging Face datasets
- License-aware output with per-row `license` field

## Tech Stack

### Data Pipeline
- Python
- DuckDB
- Pandas
- PyArrow

### Collection Sources
- IRIISNEPAL dataset
- Nepali Wikipedia extraction
- Nepali news scrapers
- YouTube Data API comments

### Distribution
- Hugging Face Hub (`huggingface_hub`)
- Parquet (ZSTD compressed)

## How It Works

```text
Raw Source CSVs -> Cleaning + Normalization -> DuckDB Merge -> Stratified Parquet Outputs -> Hugging Face Publish
```

## Quick Start

### 1. Setup Environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Build Merged Corpus

```bash
python scripts/merge.py
```

### 3. Publish to Hugging Face

```bash
python scripts/publish.py
```

Make sure your Hugging Face token is available in your environment before publishing.

## Project Structure

```text
nepali-text/
├── data/
│   ├── iriisnepal_raw.csv
│   ├── nepali_news.csv
│   ├── wikipedia_nepali.csv
│   ├── youtube_comments_clean.csv
│   └── merged/
├── scripts/
│   ├── clean.py
│   ├── merge.py
│   ├── publish.py
│   ├── youtube_scraper.py
│   ├── extract_wikipedia.py
│   └── news_scraper_*.py
├── readmes/
│   ├── README_full.md
│   ├── README_formal.md
│   ├── README_colloquial.md
│   ├── README_roman.md
│   ├── LICENSE.md
│   ├── ATTRIBUTION.md
│   └── DATA_PROCESSING.md
└── README.md
```

## Dataset Schema

All exported parquet files use this schema:

- `text`
- `source`
- `domain`
- `script`
- `lang`
- `date_collected`
- `license`

## Notes on Licensing

This is a mixed-source corpus. Each row includes a `license` value so you can filter content based on your use case.

See detailed licensing and attribution here:
- [readmes/LICENSE.md](readmes/LICENSE.md)
- [readmes/ATTRIBUTION.md](readmes/ATTRIBUTION.md)
- [readmes/DATA_PROCESSING.md](readmes/DATA_PROCESSING.md)

## Maintainer

Aadarsha Chhetri  
GitHub: [@Boredoom17](https://github.com/Boredoom17)

---

<div align="center">

If this corpus helped your work, a star on the repository is always appreciated.

</div>
