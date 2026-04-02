# License Information

**Quick Version:** Different parts of this dataset have different licenses. Each row tells you which license applies to it.

## What Can I Use?

| Source | License | Can I use it freely? |
|--------|---------|-----|
| IRIISNEPAL | MIT | ✅ Yes |
| YouTube | CC BY 4.0 | ✅ Yes (credit them) |
| Wikipedia | CC BY-SA 4.0 | ✅ Yes (share-alike) |
| News | Source-dependent | ⚠️ Ask first |

## How to Use Each One

### MIT (IRIISNEPAL)
Use it however you want—research, commercial, whatever. Just include the MIT license somewhere in your code.

### CC BY 4.0 (YouTube)
You can use it for anything, but you have to credit YouTube/the commenters.

### CC BY-SA 4.0 (Wikipedia)
You can use it, but if you build something with it, you have to release that under the same license too.

### Source-dependent (News)
If it's for research: probably okay.  
If it's for a commercial product: contact the news outlet first.

## In Practice

### For a research paper:
```
This work uses the Nepali Text Corpus [1], which combines IRIISNEPAL [2], 
Wikipedia, YouTube, and news data.

[1] Chhetri (2026)
[2] Yadav et al. (2020)
```

### For code:
Check the `license` column in the parquet file. Filter to only MIT and CC BY 4.0 if you're unsure about commercial use.

### For anything else:
When in doubt, credit the source and ask the dataset maintainer.

## BibTeX Citation

```bibtex
@dataset{chhetri2026nepali_corpus,
  author  = {Aadarsha Chhetri},
  title   = {Nepali Text Corpus},
  year    = {2026},
  url     = {https://huggingface.co/datasets/Boredoom17/nepali-text-corpus}
}
```

---

**Not legal advice.** This is just a guide. Contact a lawyer if you're doing something commercial and unsure.

**Last Updated:** April 2, 2026
