---
pretty_name: Nepali Code-Mixed Corpus
task_categories:
- text-classification
- token-classification
language:
- ne
- en
tags:
- nepali
- code-mixed
- code-switching
- english
- social-media
- low-resource
license: cc-by-4.0
size_categories:
- 10K<n<100K
---

# Nepali Code-Mixed Corpus

## Abstract
This dataset contains Nepali social-text rows with mixed scripts and language switching patterns, where Nepali and English tokens co-occur within the same sequence. It is intended for code-mixing and mixed-script robustness studies.

## Dataset Composition
Total rows: 19,845

Characteristics:
- Script: mixed
- Domain: colloquial/social
- Source: extracted from YouTube comment corpus

## Extraction Procedure
Rows are selected from colloquial data where Devanagari and Latin characters both occur within the same text.

## Schema
- text
- source
- domain
- script
- lang
- date_collected
- license

Typical values:
- script: mixed
- source: youtube_comments
- domain: colloquial
- license: CC BY 4.0

## Research Use Cases
- Code-switch detection
- Mixed-script tokenization
- Language ID at token or sequence level
- Robustness testing for Nepali NLP systems

## Limitations
- Mixed-script heuristics can include edge cases.
- Some rows are short reactions rather than full sentences.
- English fragments range from named entities to full phrases.

## License
CC BY 4.0.

## Citation
```bibtex
@dataset{chhetri2026nepali_codemixed,
  author    = {Aadarsha Chhetri},
  title     = {Nepali Code-Mixed Corpus},
  year      = {2026},
  publisher = {Hugging Face},
  url       = {https://huggingface.co/datasets/Boredoom17/nepali-codemixed-corpus}
}
```
