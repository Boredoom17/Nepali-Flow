---
pretty_name: Nepali Flow: Colloquial
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

# Nepali Flow: Colloquial

## What's This?
Real YouTube comments in Nepali. How people actually talk—casual, funny, sometimes messy. Useful if you want your model to understand everyday Nepali, not just formal news.

## What's Inside
**431,648 comments** from YouTube videos:
- 307,999 in Latin letters ("Roman Nepali")
- 103,804 in Devanagari
- 19,845 mixed (people switching between scripts)

All CC BY 4.0 license (from YouTube's terms).

## Why This Matters
Most Nepali datasets are just news and books. This one shows how real people write—with slang, code-switching, and the way language actually works on the internet.

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

## How to Cite
```
Aadarsha Chhetri. (2026). Nepali Flow: Colloquial. https://huggingface.co/datasets/Boredoom17/nepali-flow-colloquial
```

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
  title     = {Nepali Flow: Colloquial},
  year      = {2026},
  publisher = {Hugging Face},
  url       = {https://huggingface.co/datasets/Boredoom17/nepali-flow-colloquial}
}
```
