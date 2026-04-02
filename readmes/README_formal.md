---
pretty_name: Nepali Formal Corpus
task_categories:
- text-generation
- text-classification
- other
language:
- ne
tags:
- nepali
- corpus
- formal
- news
- devanagari
- low-resource
license: other
size_categories:
- 1M<n<10M
---

# Nepali Formal Corpus

## Abstract
This subset isolates formal Nepali text with a strong emphasis on journalistic and editorial style. It is intended for experiments where grammatical consistency, formal register, and topical reporting language are prioritized over conversational variation.

## Dataset Composition
Total rows: 6,735,808

Primary source groups:
- IRIISNEPAL release
- Nepali Wikipedia extraction
- Scraped Nepali news sources

Typical characteristics:
- Predominantly Devanagari script
- Formal register
- News and editorial discourse structure

## Schema
- text
- source
- domain
- script
- lang
- date_collected
- license

Notes:
- domain values include formal, encyclopedia, and news
- script is predominantly devanagari

## Construction Notes
- Source material is normalized to text rows.
- Duplicate and malformed records are reduced during preprocessing.
- Metadata is preserved to enable source-aware and license-aware filtering.

## Research Use Cases
- Formal Nepali pretraining and continued pretraining
- News classification and topic modeling
- Information extraction from standard prose
- Register transfer experiments (formal to colloquial and vice versa)

## Limitations
- Coverage is news-heavy and may not transfer directly to social language tasks.
- Editorial and publication bias from source outlets may be present.
- A small number of scrape-era formatting artifacts can remain.

## License Statement
Mixed-source formal aggregate:
- MIT (IRIISNEPAL)
- CC BY-SA 4.0 (Wikipedia)
- source-dependent (scraped news)

## Citation
```bibtex
@dataset{chhetri2026nepali_formal,
  author    = {Aadarsha Chhetri},
  title     = {Nepali Formal Corpus},
  year      = {2026},
  publisher = {Hugging Face},
  url       = {https://huggingface.co/datasets/Boredoom17/nepali-formal-corpus}
}
```
