# Attribution & Data Sources

This corpus synthesizes Nepali text from multiple public and research sources. Proper attribution is critical for ethical research.

## Primary Sources

### 1. IRIISNEPAL
- **Full Name:** IIIiSNepal - Itihasa, Kalakaram, Sthanadarshan, Shikshhya, Nepali Text Dataset
- **Repository:** https://github.com/bnltm/IIIiSNepal
- **Description:** A large-scale curated dataset of Nepali articles covering historical, cultural, educational, and geographical topics.
- **License:** MIT
- **Citation:**
  ```
  Yadav, Kanchan, et al. "IIIiSNepal: Large-Scale Annotated Nepali Text Dataset."
  Proceedings of the 2nd Workshop on NLP for Under-resourced Languages, 2020.
  ```
- **Rows in Corpus:** 6,087,439
- **Applies to:** `nepali-formal-corpus`, `nepali-text-corpus`

### 2. Nepali Wikipedia
- **Source:** Nepali Wikipedia Dump (latest as of corpus creation)
- **URL:** https://dumps.wikimedia.org/newiki/
- **Description:** Extracted sentences from Nepali Wikipedia articles across all topics and domains.
- **License:** CC BY-SA 4.0
- **Rows in Corpus:** 291,767
- **Applies to:** `nepali-formal-corpus`, `nepali-text-corpus`

### 3. Nepali News Source Crawls
- **Outlets Covered:**
  - Kantipur News (https://www.kantipuronline.com/)
  - Setopati (https://www.setopati.com/)
  - Nepal Khabar (https://www.nepalkhabar.com/)
  - Nagarik (https://www.nagariknews.com/)
  - Himalayan Times (archived articles)
  - Other regional outlets
- **Description:** Dynamically crawled from public-facing news websites.
- **License:** Source-dependent (per publisher terms of service)
- **Rows in Corpus:** 87,250
- **Applies to:** `nepali-formal-corpus`, `nepali-text-corpus`

### 4. YouTube Comments (Public)
- **Source:** YouTube Data API v3 (public comment threads)
- **Description:** Colloquial, conversational Nepali as used in social discussions, reviews, and community comments.
- **License:** CC BY 4.0 (standard YouTube comment license)
- **Rows in Corpus:** 431,648
- **Applies to:** `nepali-colloquial-corpus`, `roman-nepali-corpus`, `nepali-text-corpus`

## Contributor Acknowledgments

- **IRIISNEPAL Curators:** Kanchan Yadav, Sharad Khatiwada, and the broader NLP community contributors
- **Wikipedia Contributors:** Nepali Wikipedia editor community
- **News Publishers:** Journalists and editorial teams at Nepali news outlets
- **YouTube Commenters:** Anonymous community members sharing public discourse

## Data Cleaning & Processing

All source data underwent standardization and validation:
- Text normalization (whitespace, special characters)
- Duplicate removal at the corpus level
- Malformed record filtering
- Length-based quality thresholds (minimum 5 words for formal text)
- Script detection and classification (Devanagari, Latin, mixed)

See [DATA_PROCESSING.md](DATA_PROCESSING.md) for technical details.

## Responsible Use

- **Academic Research:** Encouraged under fair-use principles
- **Commercial Products:** Requires license-aware filtering and potential publisher permissions
- **Media Attribution:** When publishing results, recommend citing source origins
- **Ethical Concerns:** This corpus includes conversational YouTube content with occasional vulgar or offensive language; filter rows before public-facing applications

## Questions or Corrections?

For attribution corrections or to report improper use, contact the dataset maintainers through the Hugging Face dataset page.

---

**Compiled:** April 2, 2026  
**Corpus Version:** 1.0
