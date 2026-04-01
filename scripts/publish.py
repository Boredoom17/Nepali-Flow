import io
import os
from textwrap import dedent

import pyarrow.parquet as pq
from huggingface_hub import HfApi

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MERGED_DIR = os.path.join(BASE_DIR, "data", "merged")

DATASETS = [
    {
        "repo_id": "Boredoom17/nepali-text-corpus",
        "title": "Nepali Text Corpus",
        "path": os.path.join(MERGED_DIR, "nepali_corpus_full.parquet"),
        "description": "Full combined Nepali text corpus covering colloquial, formal, and encyclopedia-style text.",
        "license_note": "Mixed-source corpus. See source-level notes in the card."
    },
    {
        "repo_id": "Boredoom17/nepali-formal-corpus",
        "title": "Nepali Formal Corpus",
        "path": os.path.join(MERGED_DIR, "nepali_corpus_formal.parquet"),
        "description": "Formal Nepali text from IRIISNEPAL and news sources.",
        "license_note": "Mixed license aggregate. IRIISNEPAL is MIT; news rows are source-dependent."
    },
    {
        "repo_id": "Boredoom17/nepali-colloquial-corpus",
        "title": "Nepali Colloquial Corpus",
        "path": os.path.join(MERGED_DIR, "nepali_corpus_colloquial.parquet"),
        "description": "Colloquial and code-mixed Nepali text collected from YouTube comments.",
        "license_note": "YouTube-derived content with CC BY 4.0 metadata in the dataset."
    },
    {
        "repo_id": "Boredoom17/nepali-wikipedia-corpus",
        "title": "Nepali Wikipedia Corpus",
        "path": os.path.join(MERGED_DIR, "nepali_corpus_wikipedia.parquet"),
        "description": "Clean Nepali sentences extracted from the Nepali Wikipedia dump.",
        "license_note": "CC BY-SA 4.0."
    },
    {
        "repo_id": "Boredoom17/roman-nepali-corpus",
        "title": "Roman Nepali Corpus",
        "path": os.path.join(MERGED_DIR, "nepali_corpus_roman.parquet"),
        "description": "Roman-script Nepali subset from the colloquial corpus.",
        "license_note": "Derived from YouTube comments."
    },
    {
        "repo_id": "Boredoom17/nepali-codemixed-corpus",
        "title": "Nepali Code-Mixed Corpus",
        "path": os.path.join(MERGED_DIR, "nepali_corpus_codemixed.parquet"),
        "description": "Mixed-script Nepali subset from the colloquial corpus.",
        "license_note": "Derived from YouTube comments."
    },
]


def row_count(path: str) -> int:
    return pq.ParquetFile(path).metadata.num_rows


def size_category(rows: int) -> str:
    if rows < 100_000:
        return "10K<n<100K"
    if rows < 1_000_000:
        return "100K<n<1M"
    if rows < 10_000_000:
        return "1M<n<10M"
    return "10M<n<100M"


def build_readme(title: str, description: str, rows: int, path: str, license_note: str) -> str:
    return dedent(
        f"""---
        pretty_name: {title}
        task_categories:
        - text-classification
        - language-modeling
        language:
        - ne
        tags:
        - nepali
        - corpus
        - text
        size_categories:
        - 100K<n<1M
        license: other
        size_categories:
        - {size_category(rows)}
        ---

        # {title}

        {description}

        ## Summary
        - Rows: {rows:,}
        - Source file: `{os.path.basename(path)}`
        - License note: {license_note}

        ## Schema
        - `text`
        - `source`
        - `domain`
        - `script`
        - `lang`
        - `date_collected`
        - `license`

        ## Notes
        - This dataset is intended for research and evaluation.
        - See the project context for collection details and source breakdowns.
        """
    ).strip() + "\n"


def main() -> None:
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise SystemExit("HF_TOKEN is not set. Export it before publishing.")

    api = HfApi(token=token)

    for dataset in DATASETS:
        path = dataset["path"]
        if not os.path.exists(path):
            raise SystemExit(f"Missing file: {path}")

        rows = row_count(path)
        readme = build_readme(
            title=dataset["title"],
            description=dataset["description"],
            rows=rows,
            path=path,
            license_note=dataset["license_note"],
        )

        print(f"Publishing {dataset['repo_id']} ({rows:,} rows)")
        api.create_repo(repo_id=dataset["repo_id"], repo_type="dataset", private=True, exist_ok=True)
        api.upload_file(
            path_or_fileobj=path,
            path_in_repo=os.path.basename(path),
            repo_id=dataset["repo_id"],
            repo_type="dataset",
        )
        api.upload_file(
            path_or_fileobj=io.BytesIO(readme.encode("utf-8")),
            path_in_repo="README.md",
            repo_id=dataset["repo_id"],
            repo_type="dataset",
        )

    print("Done. All datasets uploaded.")


if __name__ == "__main__":
    main()
