import bz2
import re
import csv
import os

DUMP_FILE = "data/newiki-latest-pages-articles.xml.bz2"
OUTPUT_CSV = "data/wikipedia_nepali.csv"

def clean_text(text):
    # Remove wiki markup
    text = re.sub(r'\[\[([^|\]]*\|)?([^\]]*)\]\]', r'\2', text)
    text = re.sub(r'\{\{[^}]*\}\}', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r"'{2,}", '', text)
    text = re.sub(r'==+[^=]+=+', '', text)
    text = re.sub(r'\[\S+\]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def has_nepali(text):
    return bool(re.search(r'[\u0900-\u097F]', text))

print("Extracting Wikipedia dump...")
sentences = []
seen = set()
current_text = []
in_text = False

with bz2.open(DUMP_FILE, 'rt', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if '<text' in line:
            in_text = True
            current_text = []
        if in_text:
            current_text.append(line)
        if '</text>' in line:
            in_text = False
            full_text = ' '.join(current_text)
            full_text = re.sub(r'<text[^>]*>', '', full_text)
            full_text = re.sub(r'</text>', '', full_text)
            full_text = clean_text(full_text)

            for sent in re.split(r'[।\n]', full_text):
                sent = sent.strip()
                if len(sent.split()) >= 5 and has_nepali(sent) and sent not in seen:
                    seen.add(sent)
                    sentences.append(sent)

            if len(sentences) % 10000 == 0 and sentences:
                print(f"  Extracted {len(sentences):,} sentences so far...")

print(f"\nTotal sentences: {len(sentences):,}")

with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['text'])
    for s in sentences:
        writer.writerow([s])

print(f"Saved to {OUTPUT_CSV}")
