import pandas as pd
import re
from langdetect import detect, LangDetectException

# ─────────────────────────────────────────
# NEPALI WORD LIST (Roman script detection)
# If a latin row contains at least 1 of these → it's Roman Nepali → KEEP
# ─────────────────────────────────────────
NEPALI_WORDS = {
    # Common verbs
    "cha", "chha", "xa", "xaina", "bhayo", "gayo", "aayo", "garyo",
    "huncha", "hunchha", "hudaina", "bhanchan", "gardai", "gareko",
    "garcha", "lagyo", "lagcha", "bho", "thiyo", "thiye", "hunthyo",
    "aaudai", "jaadai", "garirahechan", "garnu", "garnos", "garnuhos",
    "diyera", "liyera", "khayera", "sutera", "uthera", "gayera",
    "aayera", "basera", "milera", "hernu", "sunnu", "bhannu",
    # Pronouns / people
    "mero", "tero", "hamro", "tapai", "tapain", "hajur", "hami",
    "usle", "unle", "maile", "timiharu", "kohi", "kasai", "sabai",
    "dai", "didi", "bhai", "bahini", "saathi", "mama", "kaka",
    "buwa", "aama", "buba", "aamaa", "kanchha", "jetho", "mailo",
    # Question words
    "kasto", "kina", "kasari", "kahile", "kahilyai", "kata", "kun",
    "ke", "ko", "k", "ki", "kahile",
    # Common adjectives / adverbs
    "ramro", "raamro", "naramro", "sundar", "thulo", "sano", "राम्रो",
    "dherai", "ali", "thikai", "sahi", "thik", "galat", "ekdam",
    "dherai", "nikkai", "sarai", "khub", "bistaarai", "chitto",
    # Common nouns
    "nepal", "nepali", "kathmandu", "pokhara", "desh", "gaun", "sahar",
    "ghar", "school", "college", "kaam", "paisa", "khana", "paani",
    "manche", "manchhe", "kehi", "kei", "insaan", "bachcha",
    "sarkar", "sarkaar", "rastra", "janata", "desh",
    # Particles / connectors
    "pani", "ni", "ta", "ra", "nai", "bhane", "bhaneko", "vane",
    "tara", "kinabhane", "tesaile", "tyasaile", "aafai", "afai",
    # Greetings / expressions
    "namaste", "namaskar", "dhanyabad", "shukriya", "maaf",
    "bistikai", "wah", "waw", "vah", "aba", "aaba", "asti",
    "hizosamma", "bholi", "parsi",
    # Emotions
    "maya", "prem", "dosti", "dukha", "sukha", "khusi", "dukhi",
    "runa", "hansnu", "man", "dil",
    # Filler / slang
    "yaar", "bro", "hai", "haina", "hoina", "sahi", "fire",
    "kasam", "sach", "jhut", "mast", "solid", "ghanta",
    # Places
    "butwal", "chitwan", "dharan", "biratnagar", "hetauda",
    "nepalgunj", "dhangadhi", "janakpur", "mustang", "pokhara",
    "terai", "pahad", "himal",
}

# ─────────────────────────────────────────
# SPAM PATTERNS to remove
# ─────────────────────────────────────────
SPAM_PATTERNS = [
    r'subscribe.*channel',
    r'check.*my.*channel',
    r'visit.*my.*channel',
    r'like.*subscribe',
    r'please.*subscribe',
    r'sub.*back',
    r'follow.*me',
    r'check.*my.*profile',
    r'promo',
    r'discount',
    r'offer',
    r'click.*link',
    r'bit\.ly',
    r'goo\.gl',
    r'tinyurl',
    r'https?://',
    r'www\.',
]
SPAM_RE = re.compile('|'.join(SPAM_PATTERNS), re.IGNORECASE)

# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────

DEVANAGARI_RANGE = re.compile(r'[\u0900-\u097F]')
EMOJI_RE = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002700-\U000027BF"  # dingbats
    "\U0001F900-\U0001F9FF"  # supplemental symbols
    "\U00002500-\U00002BEF"  # misc symbols
    "\U0001F004-\U0001F0CF"  # mahjong / playing cards
    "\U0001FA00-\U0001FA6F"  # chess / other
    "\U0001FA70-\U0001FAFF"  # misc
    "\u2640-\u2642"
    "\u2600-\u2B55"
    "\u200d"
    "\u23cf"
    "\u23e9"
    "\u231a"
    "\ufe0f"
    "\u3030"
    "]+", flags=re.UNICODE
)

def strip_emojis(text):
    """Remove emojis but keep the text."""
    text = EMOJI_RE.sub('', str(text))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def detect_script(text):
    has_devanagari = bool(DEVANAGARI_RANGE.search(str(text)))
    has_latin = bool(re.search(r'[a-zA-Z]', str(text)))
    if has_devanagari and has_latin:
        return "mixed"
    elif has_devanagari:
        return "devanagari"
    elif has_latin:
        return "latin"
    else:
        return "other"

def is_roman_nepali(text):
    """Check if latin text contains at least one Nepali word."""
    words = set(re.findall(r'[a-zA-Z]+', text.lower()))
    return bool(words & NEPALI_WORDS)

def is_spam(text):
    return bool(SPAM_RE.search(str(text)))

def detect_lang(text):
    try:
        return detect(str(text))
    except LangDetectException:
        return "unknown"

# ─────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────

df = pd.read_csv("data/youtube_comments.csv")
print(f"Loaded: {len(df)} rows")

# 1. Drop duplicates
df = df.drop_duplicates(subset="text")
print(f"After dedup: {len(df)} rows")

# 2. Drop empty
df = df.dropna(subset=["text"])
df["text"] = df["text"].str.strip()

# 3. Strip emojis (keep text, remove symbols)
df["text"] = df["text"].apply(strip_emojis)

# 4. Drop rows that became too short after emoji stripping
df = df[df["text"].apply(lambda x: len(str(x).split()) >= 4)]
print(f"After length filter (post emoji strip): {len(df)} rows")

# 5. Remove spam / promotional / URLs
df = df[~df["text"].apply(is_spam)]
print(f"After spam removal: {len(df)} rows")

# 6. Remove repetitive characters (hahahaha, !!!!!!!)
df = df[~df["text"].apply(lambda x: bool(re.search(r'(.)\1{5,}', str(x))))]
print(f"After repetition filter: {len(df)} rows")

# 7. Detect script
df["script"] = df["text"].apply(detect_script)

# 8. Remove "other" (non-latin, non-devanagari)
df = df[df["script"] != "other"]
print(f"After script filter: {len(df)} rows")

# 9. For LATIN rows: keep only Roman Nepali, remove pure English
latin_mask = df["script"] == "latin"
roman_nepali_mask = df["text"].apply(is_roman_nepali)
df = df[~latin_mask | roman_nepali_mask]
print(f"After Roman Nepali filter: {len(df)} rows")

# 10. For DEVANAGARI + MIXED rows: use langdetect to filter Hindi etc.
print("\nDetecting languages for devanagari/mixed rows...")
non_latin_mask = df["script"] != "latin"
df.loc[non_latin_mask, "lang"] = df.loc[non_latin_mask, "text"].apply(detect_lang)
df["lang"] = df["lang"].fillna("ne-roman")  # latin rows default to ne-roman

REMOVE_LANGS = {"hi", "en", "bn", "ko", "ar", "id", "ja", "zh-cn", "zh-tw", "th", "vi", "ur", "pa"}
df = df[~df["lang"].isin(REMOVE_LANGS)]
print(f"After language filter: {len(df)} rows")

# ─────────────────────────────────────────
# FINAL STATS
# ─────────────────────────────────────────
print(f"\n✅ Final clean dataset: {len(df)} rows")
print("\nScript distribution:")
print(df["script"].value_counts())
print("\nLanguage distribution:")
print(df["lang"].value_counts().head(10))

print("\n--- Sample Devanagari ---")
print(df[df["script"] == "devanagari"]["text"].sample(5).to_string())

print("\n--- Sample Mixed ---")
print(df[df["script"] == "mixed"]["text"].sample(5).to_string())

print("\n--- Sample Roman Nepali ---")
print(df[df["script"] == "latin"]["text"].sample(5).to_string())

# Save
df.to_csv("data/youtube_comments_clean.csv", index=False, encoding="utf-8")
print("\n💾 Saved to data/youtube_comments_clean.csv")