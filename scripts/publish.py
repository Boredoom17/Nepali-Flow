import io
import os
from textwrap import dedent

import pyarrow.parquet as pq
from huggingface_hub import HfApi

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MERGED_DIR = os.path.join(BASE_DIR, "data", "merged")
README_DIR = os.path.join(BASE_DIR, "readmes")

README_BY_REPO = {
    "Boredoom17/Nepali-Corpus": "README_full.md",
    "Boredoom17/Nepali-Flow-Formal": "README_formal.md",
    "Boredoom17/Nepali-Flow-Colloquial": "README_colloquial.md",
    "Boredoom17/Nepali-Flow-Roman": "README_roman.md",
}

DATASETS = [
    {
        "repo_id": "Boredoom17/Nepali-Corpus",
        "title": "Nepali-Corpus",
        "path": os.path.join(MERGED_DIR, "nepali_corpus_full.parquet"),
        "description": "Full combined Nepali text corpus covering colloquial, formal, and encyclopedia-style text.",
        "license_note": "Mixed-source corpus. See source-level notes in the card."
    },
    {
        "repo_id": "Boredoom17/Nepali-Flow-Formal",
        "title": "Nepali-Flow-Formal",
        "path": os.path.join(MERGED_DIR, "nepali_corpus_formal.parquet"),
        "description": "Formal Nepali text combining IRIISNEPAL, Wikipedia, and scraped news sources.",
        "license_note": "Mixed-source formal aggregate (MIT + CC BY-SA 4.0 + source-dependent)."
    },
    {
        "repo_id": "Boredoom17/Nepali-Flow-Colloquial",
        "title": "Nepali-Flow-Colloquial",
        "path": os.path.join(MERGED_DIR, "nepali_corpus_colloquial.parquet"),
        "description": "Colloquial and code-mixed Nepali text collected from YouTube comments.",
        "license_note": "YouTube-derived content with CC BY 4.0 metadata in the dataset."
    },
    {
        "repo_id": "Boredoom17/Nepali-Flow-Roman",
        "title": "Nepali-Flow-Roman",
        "path": os.path.join(MERGED_DIR, "nepali_corpus_roman.parquet"),
        "description": "Roman-script Nepali subset from the colloquial corpus.",
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
        - text-generation
        language:
        - ne
        tags:
        - nepali
        - corpus
        - text
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


def load_readme(dataset: dict, rows: int) -> str:
    readme_name = README_BY_REPO.get(dataset["repo_id"])
    if readme_name:
        readme_path = os.path.join(README_DIR, readme_name)
        if os.path.exists(readme_path):
            with open(readme_path, "r", encoding="utf-8") as f:
                return f.read()

    # Fallback if a curated card is missing.
    return build_readme(
        title=dataset["title"],
        description=dataset["description"],
        rows=rows,
        path=dataset["path"],
        license_note=dataset["license_note"],
    )


def build_docs(dataset: dict, rows: int) -> dict[str, str]:
    repo_id = dataset["repo_id"]
    title = dataset["title"]
    filename = os.path.basename(dataset["path"])

    if repo_id == "Boredoom17/Nepali-Corpus":
        license_summary = (
            "This repository is a mixed-license aggregate. Use the per-row license "
            "column before redistribution or downstream release."
        )
        source_summary = (
            "This corpus combines IRIISNEPAL news text, YouTube comments, Nepali "
            "Wikipedia, and recent news scraping into a single unified release."
        )
    elif repo_id == "Boredoom17/Nepali-Flow-Formal":
        license_summary = (
            "This subset is a mixed-license formal aggregate built from MIT "
            "(IRIISNEPAL), CC BY-SA 4.0 (Wikipedia), and source-dependent news rows."
        )
        source_summary = (
            "This subset contains formal Nepali text from IRIISNEPAL, Nepali "
            "Wikipedia, and scraped news sources."
        )
    elif repo_id == "Boredoom17/Nepali-Flow-Colloquial":
        license_summary = "This subset is CC BY 4.0 in the dataset metadata."
        source_summary = "This subset contains conversational Nepali collected from YouTube comments."
    elif repo_id == "Boredoom17/Nepali-Flow-Roman":
        license_summary = "This subset is CC BY 4.0 and derived from the colloquial YouTube-comment corpus."
        source_summary = "This subset isolates Latin-script Nepali from the colloquial corpus."
    else:
        license_summary = "This subset uses source-level licensing as documented in the repository."
        source_summary = "This subset follows the corpus composition described in the dataset card."

    docs = {
        "LICENSE.md": dedent(
            f"""# License Summary

            {license_summary}

            ## Row-Level Guidance
            - Check the `license` field in the parquet file before reuse.
            - Preserve attribution for source material when required.
            - Apply additional review before commercial redistribution.
            """
        ).strip()
        + "\n",
        "docs/OVERVIEW.md": dedent(
            f"""# {title} Overview

            Rows: {rows:,}

            {source_summary}

            ## Repository Contents
            - `README.md`: dataset card
            - `LICENSE.md`: license summary
            - `docs/OVERVIEW.md`: high-level summary
            - `docs/DATA_SCHEMA.md`: field descriptions
            - `docs/DATA_SOURCES.md`: provenance notes
            - `docs/USAGE.md`: loading examples
            - `docs/QUALITY_AND_LIMITATIONS.md`: dataset caveats
            - `CITATION.cff`: citation metadata
            - `{filename}`: primary parquet file
            """
        ).strip()
        + "\n",
        "docs/DATA_SCHEMA.md": dedent(
            """# Data Schema

            Each row in the parquet file contains:

            - `text`: the textual content
            - `source`: the originating source or collection label
            - `domain`: the broad category of the row
            - `script`: script label such as `devanagari`, `latin`, or `mixed`
            - `lang`: language tag used during preprocessing
            - `date_collected`: collection or extraction date
            - `license`: per-row license label

            ## Notes
            - These fields are intentionally simple so the dataset can be loaded in most NLP pipelines without custom parsing.
            - Script and language labels are heuristic and are best treated as descriptive metadata rather than ground truth.
            """
        ).strip()
        + "\n",
        "docs/DATA_SOURCES.md": dedent(
            f"""# Data Sources

            {source_summary}

            ## Provenance Notes
            - The release is built from the local preprocessing pipeline in this repository.
            - Source-specific filtering and deduplication are applied before export.
            - The resulting parquet file is intended for research, evaluation, and dataset inspection.
            """
        ).strip()
        + "\n",
        "docs/USAGE.md": dedent(
            f"""# Usage

            ## Load with `datasets`
            ```python
            from datasets import load_dataset

            ds = load_dataset(\"{repo_id}\")
            print(ds)
            ```

            ## Load directly with pandas
            ```python
            import pandas as pd

            df = pd.read_parquet(\"hf://datasets/{repo_id}/{filename}\")
            print(df.head())
            ```

            ## Suggested Workflow
            - Inspect `README.md` first.
            - Review `LICENSE.md` before redistribution.
            - Use the row-level metadata to filter by domain, script, or source.
            """
        ).strip()
        + "\n",
        "docs/QUALITY_AND_LIMITATIONS.md": dedent(
            f"""# Quality and Limitations

            ## Quality Notes
            - The release is deduplicated and normalized through the preprocessing pipeline.
            - The parquet order is arranged to make the dataset viewer open on more representative examples first.

            ## Known Limitations
            - Colloquial text includes slang, transliteration, and non-standard spelling.
            - The corpus is not a benchmark suite with fixed splits.
            - Metadata is descriptive and should be validated per task.

            ## Intended Use
            {dataset["description"]}
            """
        ).strip()
        + "\n",
        "CITATION.cff": dedent(
            f"""cff-version: 1.2.0
message: If you use this dataset, please cite it.
title: {title}
authors:
  - family-names: Chhetri
    given-names: Aadarsha
year: 2026
repository-code: https://huggingface.co/{repo_id}
url: https://huggingface.co/datasets/{repo_id}
"""
        ).strip()
        + "\n",
    }

    return docs


def main() -> None:
    # Use cached login token — run `python -c "from huggingface_hub import login; login()"` first
    api = HfApi()

    for dataset in DATASETS:
        path = dataset["path"]
        if not os.path.exists(path):
            print(f"⚠️  Skipping — file not found: {path}")
            continue

        rows = row_count(path)
        readme = load_readme(dataset, rows)
        docs = build_docs(dataset, rows)

        print(f"\nPublishing {dataset['repo_id']} ({rows:,} rows)...")
        api.create_repo(
            repo_id=dataset["repo_id"],
            repo_type="dataset",
            private=False,
            exist_ok=True
        )
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
        for path_in_repo, content in docs.items():
            api.upload_file(
                path_or_fileobj=io.BytesIO(content.encode("utf-8")),
                path_in_repo=path_in_repo,
                repo_id=dataset["repo_id"],
                repo_type="dataset",
            )
        print(f"  ✅ https://huggingface.co/datasets/{dataset['repo_id']}")

    print("\n🎉 All datasets published!")


if __name__ == "__main__":
    main()