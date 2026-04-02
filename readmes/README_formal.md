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

## What's This?
This dataset has formal Nepali writing—the kind you'd find in news articles, encyclopedias, and research papers. Good for training language models on clear, well-written Nepali.

## What's Inside
**6,735,808 rows** from three places:
- IRIISNEPAL dataset (MIT license)
- Nepali Wikipedia
- Nepali news outlets (Kantipur, Setopati, etc.)

Mostly in Devanagari script. Formal writing—no slang or memes.

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

## Good For
- Training language models on formal Nepali
- News classification and topic modeling
- Tasks where proper grammar matters
- Understanding how formal Nepali differs from casual speech

## Fair Warnings
- Mostly news articles—might not help with casual speech understanding
- Some articles lean toward specific outlets' editorial styles
- A few random formatting hiccups might be hiding in there

## License Statement
Mixed-source formal aggregate:
- MIT (IRIISNEPAL)
- CC BY-SA 4.0 (Wikipedia)
- source-dependent (scraped news)

## How to Cite
If you use this in research, cite it like:
```
Aadarsha Chhetri. (2026). Nepali Formal Corpus. https://huggingface.co/datasets/Boredoom17/nepali-formal-corpus
```

Or in BibTeX:
```bibtex
@dataset{aadarsha2026formal,
  author = {Aadarsha Chhetri},
  title = {Nepali Formal Corpus},
  year = {2026},
  url = {https://huggingface.co/datasets/Boredoom17/nepali-formal-corpus}
}
```
