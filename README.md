<div align="center">

# Nepali Flow
### Large-Scale Nepali Dataset Suite for NLP Research

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![DuckDB](https://img.shields.io/badge/DuckDB-Data%20Engine-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)](https://duckdb.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![HuggingFace](https://img.shields.io/badge/Hugging%20Face-Datasets-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/datasets)
[![License](https://img.shields.io/badge/License-Mixed-orange?style=for-the-badge)](readmes/LICENSE.md)

**Collect Data** • **Merge at Scale** • **Publish to Hugging Face**

---

</div>

## What Is This?

I collected Nepali text from different places and shaped it into a small dataset suite, not just one giant file. The idea is to give NLP researchers a few clean choices depending on what kind of Nepali they want to work with.

Each dataset has a different job:

| Dataset | What it is | Size |
|---|---|---:|
| **Nepali Flow** | Everything combined in one place | 7.1M rows |
| **Nepali Flow: Formal** | News + IRIISNEPAL + Wikipedia, mostly polished text | 6.3M rows |
| **Nepali Flow: Colloquial** | YouTube comments and casual online Nepali | 431k rows |
| **Nepali Flow: Roman** | Nepali written in Latin letters | 307k rows |

If someone only wants clean formal text, they can use the formal set. If they want messy real-world Nepali, they can use the colloquial or Roman set. If they want the whole mix, they can use the full corpus.

All the raw data is in CSV format, and I merge it using DuckDB to create parquet files that are easy to load into your ML pipeline.

## Hugging Face Datasets

All four Hugging Face datasets are part of the same suite and each one is meant for a different use case:

- [Boredoom17/Nepali-Corpus](https://huggingface.co/datasets/Boredoom17/Nepali-Corpus) - full mix of everything
- [Boredoom17/Nepali-Flow-Formal](https://huggingface.co/datasets/Boredoom17/Nepali-Flow-Formal) - polished text for formal NLP work
- [Boredoom17/Nepali-Flow-Colloquial](https://huggingface.co/datasets/Boredoom17/Nepali-Flow-Colloquial) - everyday Nepali and code-mixed text
- [Boredoom17/Nepali-Flow-Roman](https://huggingface.co/datasets/Boredoom17/Nepali-Flow-Roman) - Romanized Nepali

## Key Features

- Source-aware merge pipeline with row-level metadata
- Domain split support (formal, encyclopedia, news, colloquial)
- Script tagging (Devanagari, Latin, mixed)
- Large-file handling via DuckDB + parquet
- Reproducible publication workflow for Hugging Face datasets
- License-aware output with per-row `license` field


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

## How I Built It

```text
Download/Scrape Sources → Clean & Tag → Merge with DuckDB → Export as Parquet → Upload to HuggingFace.
```

Each row has metadata tags: where it came from, what type of text it is, what script (Devanagari or Latin), and license info.

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

## How to Cite

If you use this corpus, cite it as:

```
Aadarsha Chhetri. (2026). Nepali-Corpus. Hugging Face Datasets.
https://huggingface.co/datasets/Boredoom17/Nepali-Corpus
```

**BibTeX:**
```bibtex
@dataset{aadarsha2026nepali_corpus,
  author = {Aadarsha Chhetri},
  title = {Nepali-Corpus},
  year = {2026},
  url = {https://huggingface.co/datasets/Boredoom17/Nepali-Corpus}
}
```

**Casual mention:** "We used Aadarsha Chhetri's Nepali-Corpus (2026)."

## Maintainer

Aadarsha Chhetri  
GitHub: [@Boredoom17](https://github.com/Boredoom17)

---

<div align="center">

If this corpus helped your work, a star on the repository is always appreciated.

</div>
