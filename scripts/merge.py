import os
import re
import pandas as pd
from datetime import date

BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YOUTUBE_CSV     = os.path.join(BASE_DIR, "data", "youtube_comments_clean.csv")
IRIIS_CSV       = os.path.join(BASE_DIR, "data", "iriisnepal_raw.csv")
WIKI_CSV        = os.path.join(BASE_DIR, "data", "wikipedia_nepali.csv")
OUT_DIR         = os.path.join(BASE_DIR, "data", "merged")
TODAY           = date.today().isoformat()

os.makedirs(OUT_DIR, exist_ok=True)

# ─────────────────────────────────────────
# LOAD YOUTUBE
# ─────────────────────────────────────────
print("Loading YouTube comments...")
yt = pd.read_csv(YOUTUBE_CSV, usecols=["text", "script", "lang"])
yt["source"]         = "youtube_comments"
yt["domain"]         = "colloquial"
yt["date_collected"] = TODAY
yt["license"]        = "CC BY 4.0"
yt = yt[["text", "source", "domain", "script", "lang", "date_collected", "license"]]
print(f"  YouTube rows: {len(yt):,}")

# ─────────────────────────────────────────
# LOAD WIKIPEDIA
# ─────────────────────────────────────────
print("\nLoading Wikipedia...")
wiki = pd.read_csv(WIKI_CSV)
wiki["source"]         = "wikipedia_nepali"
wiki["domain"]         = "encyclopedia"
wiki["script"]         = "devanagari"
wiki["lang"]           = "ne"
wiki["date_collected"] = TODAY
wiki["license"]        = "CC BY-SA 4.0"
wiki = wiki[["text", "source", "domain", "script", "lang", "date_collected", "license"]]
print(f"  Wikipedia rows: {len(wiki):,}")

# ─────────────────────────────────────────
# LOAD IRIISNEPAL IN CHUNKS
# ─────────────────────────────────────────
print("\nLoading IRIISNEPAL in chunks...")
chunks = []
chunk_size = 100_000
total_raw = 0
total_kept = 0

for chunk in pd.read_csv(IRIIS_CSV, usecols=["Article", "Source"], chunksize=chunk_size):
    total_raw += len(chunk)
    chunk = chunk.rename(columns={"Article": "text"})
    chunk["text"] = chunk["text"].astype(str)
    chunk = chunk[chunk["text"].str.split().str.len() >= 5]
    chunk = chunk[chunk["text"].apply(lambda t: bool(re.search(r'[\u0900-\u097F]', str(t))))]
    chunk = chunk.drop_duplicates(subset=["text"])
    chunk["source"]         = "iriisnepal"
    chunk["domain"]         = "formal"
    chunk["script"]         = "devanagari"
    chunk["lang"]           = "ne"
    chunk["date_collected"] = TODAY
    chunk["license"]        = "MIT"
    chunks.append(chunk[["text", "source", "domain", "script", "lang", "date_collected", "license"]])
    total_kept += len(chunk)
    print(f"  Processed {total_raw:,} rows so far, kept {total_kept:,}...")

print("\nConcatenating IRIISNEPAL chunks...")
iriis = pd.concat(chunks, ignore_index=True)
iriis = iriis.drop_duplicates(subset=["text"])
print(f"  Final IRIISNEPAL rows: {len(iriis):,}")

# ─────────────────────────────────────────
# MERGE ALL THREE
# ─────────────────────────────────────────
print("\nMerging all sources...")
combined = pd.concat([yt, wiki, iriis], ignore_index=True)
print(f"  Combined before dedup: {len(combined):,}")
combined = combined.drop_duplicates(subset=["text"])
print(f"  After deduplication:   {len(combined):,}")

# ─────────────────────────────────────────
# SAVE OUTPUTS
# ─────────────────────────────────────────
print("\nSaving outputs...")

def save(df, name):
    path = os.path.join(OUT_DIR, f"{name}.parquet")
    df.to_parquet(path, index=False)
    size_mb = os.path.getsize(path) / (1024 * 1024)
    print(f"  {name:<50} {len(df):>10,} rows  {size_mb:>7.1f} MB")

save(combined,                                          "nepali_corpus_full")
save(combined[combined["domain"] == "colloquial"],      "nepali_corpus_colloquial")
save(combined[combined["domain"] == "formal"],          "nepali_corpus_formal")
save(combined[combined["domain"] == "encyclopedia"],    "nepali_corpus_wikipedia")
save(combined[combined["script"] == "latin"],           "nepali_corpus_roman")
save(combined[combined["script"] == "mixed"],           "nepali_corpus_codemixed")

# ─────────────────────────────────────────
# FINAL STATS
# ─────────────────────────────────────────
print("\n" + "="*60)
print(f"Total rows: {len(combined):,}")
print("\nBy domain:")
print(combined["domain"].value_counts().to_string())
print("\nBy script:")
print(combined["script"].value_counts().to_string())
print("\nBy source:")
print(combined["source"].value_counts().to_string())
print("\nBy license:")
print(combined["license"].value_counts().to_string())
print("="*60)
print("\nDone. Next: python scripts/publish.py")