# License

This corpus is a **mixed-source dataset** with multiple licenses. Each row is tagged with a `license` field indicating its source license.

## License Breakdown by Source

### IRIISNEPAL Dataset
- **License:** MIT
- **Rows:** ~6.0 million
- **Source:** https://github.com/bnltm/IIIiSNepal
- **Applies to:** `nepali-formal-corpus`

### Nepali Wikipedia
- **License:** CC BY-SA 4.0
- **Rows:** ~291,000
- **Source:** Nepali Wikipedia dump
- **Attribution:** Derived from Wikipedia contributors
- **Applies to:** `nepali-formal-corpus`

### Scraped News Sources
- **License:** Source-dependent
- **Rows:** ~87,000
- **Sources:** 
  - Kantipur News (private use)
  - Setopati (private use)
  - Nepal Khabar (private use)
  - Nagarik (private use)
  - Other Nepali news outlets
- **Note:** News articles are included under fair-use research assumptions. Please verify licensing with original publishers for commercial use.
- **Applies to:** `nepali-formal-corpus`

### YouTube Comments
- **License:** CC BY 4.0
- **Rows:** ~431,000
- **Source:** YouTube API (public comments)
- **Attribution:** YouTube commenters
- **Applies to:** `nepali-colloquial-corpus`, `roman-nepali-corpus`

## Usage Guidance

- **For academic research:** All sources are permissible under academic fair-use principles.
- **For commercial use:** Filter by license field. Use only MIT and CC BY 4.0 rows, or obtain permissions from news outlets.
- **For compliance:** Review the `license` column in each dataset to filter by acceptable licenses for your use case.

## Recommended Attribution

If you use this corpus, cite it as:

```
@dataset{nepali_text_corpus_2026,
  author = {Aadarsha Chhetri},
  title = {Nepali Text Corpus},
  year = {2026},
  organization = {Hugging Face Datasets},
  url = {https://huggingface.co/datasets/Boredoom17/nepali-text-corpus}
}
```

And acknowledge individual sources:
- IRIISNEPAL for formal text
- Wikipedia contributors for encyclopedia content
- Nepali news outlets for journalism
- YouTube commenters for colloquial speech

---

**Last Updated:** April 2, 2026
