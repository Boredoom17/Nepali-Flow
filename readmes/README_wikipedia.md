---
pretty_name: Nepali Wikipedia Corpus
task_categories:
- text-generation
- question-answering
language:
- ne
tags:
- nepali
- wikipedia
- encyclopedia
- devanagari
- low-resource
license: cc-by-sa-4.0
size_categories:
- 100K<n<1M
---

# Nepali Wikipedia Corpus

## Abstract
This dataset contains sentence-level Nepali text extracted from the official Nepali Wikipedia dump. It provides relatively clean encyclopedic prose for experiments that require factual, topic-oriented formal language.

## Dataset Composition
Total rows: 291,767

Characteristics:
- Domain: encyclopedia
- Script: Devanagari
- Style: formal and expository

## Extraction Procedure
- Downloaded Nepali Wikipedia pages-articles dump.
- Parsed article text from XML structure.
- Removed wiki markup/templates and common HTML artifacts.
- Split and filtered text into sentence-like rows.
- Deduplicated repeated lines where possible.

## Schema
- text
- source
- domain
- script
- lang
- date_collected
- license

Typical values:
- source: wikipedia_nepali
- domain: encyclopedia
- script: devanagari
- license: CC BY-SA 4.0

## Research Use Cases
- Language model pretraining for factual/style-stable Nepali text
- Retrieval and QA data construction
- Named entity and terminology extraction
- Baseline formal Nepali reference corpus

## Limitations
- Wikipedia coverage reflects editor interests and topic imbalance.
- Sentence segmentation from dump text is heuristic.
- Some markup-related edge artifacts can survive cleaning.

## License
CC BY-SA 4.0.

## Citation
```bibtex
@dataset{chhetri2026nepali_wikipedia,
  author    = {Aadarsha Chhetri},
  title     = {Nepali Wikipedia Corpus},
  year      = {2026},
  publisher = {Hugging Face},
  url       = {https://huggingface.co/datasets/Boredoom17/nepali-wikipedia-corpus}
}
```
