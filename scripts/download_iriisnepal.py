from datasets import load_dataset
import pandas as pd

print("Downloading IRIISNEPAL... this will take a few minutes")

dataset = load_dataset("IRIISNEPAL/Nepali-Text-Corpus")

# Convert to pandas
train_df = dataset['train'].to_pandas()
test_df = dataset['test'].to_pandas()

# Merge both splits
df = pd.concat([train_df, test_df], ignore_index=True)

print(f"Downloaded: {len(df)} rows")
print(f"Columns: {df.columns.tolist()}")
print(df.head(3))

# Save
df.to_csv("data/iriisnepal_raw.csv", index=False)
print("✅ Saved to data/iriisnepal_raw.csv")