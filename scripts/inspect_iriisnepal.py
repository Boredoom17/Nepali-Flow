import os
import glob
import pandas as pd

BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IRIIS_DIR = os.path.join(BASE_DIR, "data", "iriisnepal")

print(f"Looking in: {IRIIS_DIR}")

parquet_files = sorted(glob.glob(os.path.join(IRIIS_DIR, "**/*.parquet"), recursive=True))
if not parquet_files:
    parquet_files = sorted(glob.glob(os.path.join(IRIIS_DIR, "*.parquet")))

if not parquet_files:
    print("No parquet files found. Is the download still running?")
    exit(1)

print(f"Found {len(parquet_files)} parquet files")
print(f"Total size: {sum(os.path.getsize(f) for f in parquet_files)/1e9:.2f} GB")
print()

# Load just the first file to inspect
sample = pd.read_parquet(parquet_files[0])
print("Columns:", sample.columns.tolist())
print("Shape of first file:", sample.shape)
print("Dtypes:")
print(sample.dtypes)
print()
print("First 3 rows:")
pd.set_option('display.max_colwidth', 80)
print(sample.head(3).to_string())
print()
print("Null counts:")
print(sample.isnull().sum())
