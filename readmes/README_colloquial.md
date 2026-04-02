---
pretty_name: Nepali Colloquial Corpus
task_categories:
- text-classification
- other
language:
- ne
tags:
- nepali
- colloquial
- social-media
- youtube
- code-mixed
- roman-nepali
- low-resource
license: cc-by-4.0
size_categories:
- 100K<n<1M
---

# Nepali Colloquial Corpus

## Abstract
This subset targets colloquial Nepali as used in social media environments. It was constructed to complement formal Nepali corpora by capturing informal lexical choices, transliterated Roman Nepali, and mixed-script writing patterns.

## Dataset Composition
Total rows: 431,648

Script distribution:
- Latin (Roman Nepali): 307,999
- Devanagari: 103,804
- Mixed: 19,845

Primary source:
- YouTube comments collected through API-based pipelines

## Motivation
Existing Nepali resources are often skewed toward formal text. This subset improves coverage for:
- colloquial phrasing and discourse markers
- transliterated Nepali written in Latin script
- platform-native mixed-script behavior

## Schema
- text
- source
- domain
- script
- lang
- date_collected
- license

Typical values:
- source: youtube_comments
- domain: colloquial
- script: devanagari, latin, mixed
- license: CC BY 4.0

## Construction Notes
- Video selection used broad Nepali-language query categories.
- Comment rows were deduplicated and lightly cleaned for obvious noise.
- Script labels were assigned using Unicode-script heuristics.
- Language tags include ne, ne-roman, and unknown fallback cases.
- Because this is authentic social-media text, the Hugging Face dataset viewer may surface informal or strong language in preview rows; that is expected for this subset.

## Research Use Cases
- Informal Nepali language modeling
- Sentiment and opinion mining in social text
- Roman-to-Devanagari normalization and transliteration
- Code-switching and script identification

## Limitations
- Social comments contain high spelling variance and evolving slang.
- Platform-specific discourse patterns may bias lexical statistics.
- Not all rows are complete or grammatical sentences.

## License
CC BY 4.0.

## Citation
```bibtex
@dataset{chhetri2026nepali_colloquial,
  author    = {Aadarsha Chhetri},
  title     = {Nepali Colloquial Corpus},
  year      = {2026},
  publisher = {Hugging Face},
  url       = {https://huggingface.co/datasets/Boredoom17/nepali-colloquial-corpus}
}
```
