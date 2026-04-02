---
pretty_name: Roman Nepali Corpus
task_categories:
- text-classification
- translation
language:
- ne
tags:
- nepali
- roman-nepali
- romanized
- transliteration
- social-media
- low-resource
license: cc-by-4.0
size_categories:
- 100K<n<1M
---

# Roman Nepali Corpus

## Abstract
This dataset is the Latin-script subset of colloquial Nepali text. It is designed for research on Roman Nepali, where Nepali is represented in non-standard Latin transliteration across social communication channels.

## Dataset Composition
Total rows: 307,999

Characteristics:
- Script: latin
- Domain: colloquial/social
- Source: youtube_comments subset

## Motivation
Roman Nepali is common in practice but remains underrepresented in public Nepali datasets. This subset supports:
- transliteration and normalization research
- script-robust language modeling
- handling non-standard spelling in user-generated text

## Schema
- text
- source
- domain
- script
- lang
- date_collected
- license

Typical values:
- script: latin
- lang: ne-roman (or unknown in ambiguous cases)
- license: CC BY 4.0

## Research Use Cases
- Roman-to-Devanagari conversion
- Informal Nepali chatbot input handling
- Social-text tokenization and normalization research

## Limitations
- Roman spelling is non-standard and highly variable.
- Multiple spellings may represent the same Nepali word.
- Some rows include mixed-language tokens.

## License
CC BY 4.0.

## Citation
```bibtex
@dataset{chhetri2026roman_nepali,
  author    = {Aadarsha Chhetri},
  title     = {Roman Nepali Corpus},
  year      = {2026},
  publisher = {Hugging Face},
  url       = {https://huggingface.co/datasets/Boredoom17/roman-nepali-corpus}
}
```
