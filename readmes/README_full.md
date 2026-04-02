---
pretty_name: Nepali-Corpus
task_categories:
- text-generation
- text-classification
- other
language:
- ne
tags:
- nepali
- corpus
- devanagari
- roman-nepali
- code-mixed
- low-resource
license: other
size_categories:
- 1M<n<10M
multilinguality:
- monolingual
source_datasets:
- original
---

# Nepali-Corpus

## What Is This?
Everything combined—7.1 million rows of Nepali. News, Wikipedia, YouTube comments, all together. It's meant to be a solid foundation if you want to build NLP tools for Nepali.

## Dataset Composition
Total rows: 7,167,456

| Subset | Rows | Domain profile | Script profile |
|---|---:|---|---|
| Full corpus | 7,167,456 | Formal + colloquial + encyclopedia + news | Devanagari, Latin, mixed |
| Formal subset | 6,735,808 | Formal/news/encyclopedia writing | Mostly Devanagari |
| Colloquial subset | 431,648 | Social media comments | Devanagari, Latin, mixed |
| Roman subset | 307,999 | Colloquial social text | Latin |
| Code-mixed subset | 19,845 | Colloquial mixed-script text | Mixed |

## Where It Came From
- **IRIISNEPAL** — a dataset of formal Nepali writing (6M rows)
- **YouTube comments** — real conversations (431k rows)
- **Wikipedia** — encyclopedia articles (291k rows)
- **News articles** — from Nepali news websites (87k rows)

Each row tells you where it came from and what license it's under.

## Schema
Each record includes:
- text: textual content
- source: source identifier (for example iriisnepal, youtube_comments, wikipedia_nepali, ratopati)
- domain: formal, colloquial, encyclopedia, or news
- script: devanagari, latin, or mixed
- lang: language tag (for example ne, ne-roman, unknown)
- date_collected: collection or extraction date
- license: row-level license indicator

## Construction Notes
- Pipeline-level deduplication is applied.
- Social text undergoes basic noise reduction (for example repetitive symbols, spam-like artifacts, and links).
- Wikipedia data is parsed from dump format and normalized to sentence-like rows.
- Script tags are assigned using character-range heuristics.
- The Hugging Face dataset viewer shows the first rows of the parquet file, so the corpus is ordered to surface more representative formal and encyclopedic examples first in the full preview.

## Research Use Cases
- Nepali language model pretraining and domain adaptation
- Formal-vs-colloquial register analysis
- Script and code-mixing identification
- Retrieval and classification in low-resource settings

## Limitations
- This is an aggregate corpus with mixed licenses; row-level license filtering is necessary for strict compliance workflows.
- Colloquial text contains non-standard spelling and platform-specific slang.
- Language and script labels are heuristic and may contain limited noise.
- The corpus is not released with fixed train/dev/test benchmarks.

## Ethical and Responsible Use
This dataset should not be used to profile individuals or infer sensitive personal attributes. For production systems, users should implement additional filtering, auditing, and task-specific evaluation.

## License Statement
The corpus is mixed-license. On Hugging Face, `other` means the dataset does not fit a single standard built-in license tag. The license column should be treated as the primary indicator for row-level usage conditions.

- IRIISNEPAL rows: MIT
- Wikipedia rows: CC BY-SA 4.0
- YouTube-derived rows: CC BY 4.0 metadata context
- Scraped news rows: source-dependent

## Citation
If people ask how to cite this:

```
Aadarsha Chhetri. (2026). Nepali-Corpus. Hugging Face Datasets.
https://huggingface.co/datasets/Boredoom17/Nepali-Corpus
```

**BibTeX:**
```bibtex
@dataset{aadarsha2026nepali_text_corpus,
  author = {Aadarsha Chhetri},
  title = {Nepali-Corpus},
  year = {2026},
  url = {https://huggingface.co/datasets/Boredoom17/Nepali-Corpus}
}
```

**Or just:** "We used Aadarsha Chhetri's Nepali-Corpus (2026)."
