from datasets import load_dataset
import pandas as pd

# This downloads both train and test splits from Hugging Face.
print("Downloading IRIISNEPAL... this will take a few minutes")

dataset = load_dataset("IRIISNEPAL/Nepali-Text-Corpus")

# Convert each split to pandas so we can combine and save locally.
train_df = dataset['train'].to_pandas()
test_df = dataset['test'].to_pandas()

# Keep everything in one file for the later merge pipeline.
df = pd.concat([train_df, test_df], ignore_index=True)

print(f"Downloaded: {len(df)} rows")
print(f"Columns: {df.columns.tolist()}")
print(df.head(3))

# Save a single raw CSV file used by scripts/merge.py.
df.to_csv("data/iriisnepal_raw.csv", index=False)
print("Saved to data/iriisnepal_raw.csv")