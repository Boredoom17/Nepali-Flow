# Where the Data Came From

This dataset combines text from several sources. Each one has different rules about how you can use it. I've documented everything below so you know what to cite and what licenses apply.

## The Main Sources

### IRIISNEPAL Dataset
The largest part (6M+ rows) of formal Nepali comes from IRIISNEPAL. This is a curated collection of Nepali articles built by researchers.

**Citation:**  
```
Yadav, Kanchan, et al. "IIIiSNepal: A Large-Scale Annotated Nepali Text Dataset."
Presented at the 2nd Workshop on NLP for Under-resourced Languages, 2020.
```

**License:** MIT (you can use this freely)  
**Rows:** ~6,087,439

### Nepali Wikipedia
Wikipedia articles in Nepali (291k rows). Extracted from the public Wikipedia dump.

**License:** CC BY-SA 4.0  
**Source:** https://dumps.wikimedia.org/newiki/  
**Rows:** ~291,767

### Nepali News Outlets
Recent news articles scraped from public websites (87k rows).

- Kantipur News
- Setopati
- Nepal Khabar
- Nagarik
- Himalayan Times

**License:** Source-dependent  
**Rows:** ~87,250

### YouTube Comments
Public comments from YouTube videos in Nepali (431k rows).

**License:** CC BY 4.0  
**Rows:** ~431,648

**Fair Warning:** Real YouTube comments—unfiltered. Some may contain vulgar or offensive language.

## What This Means For You

### For academic research:
All of this is fine to use. Just cite the IRIISNEPAL paper and individual sources.

### For commercial products:
- ✅ Use MIT stuff (IRIISNEPAL) freely
- ✅ Use CC BY 4.0 stuff (YouTube)—just credit them  
- ⚠️ News articles—check each outlet's terms first
- ⚠️ Wikipedia—you must share your code under CC BY-SA too

### How to Cite This Work
```
Aadarsha Chhetri. (2026). Nepali Text Corpus. Hugging Face Datasets.
https://huggingface.co/datasets/Boredoom17/nepali-text-corpus
```

## Questions?
Each row has a `license` column. Check that before using data commercially. See [LICENSE.md](LICENSE.md) for more details.

---

**Last Updated:** April 2, 2026
