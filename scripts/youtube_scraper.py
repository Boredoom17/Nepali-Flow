import os
import csv
import time
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────
# CONFIG — add as many keys as you have
# ─────────────────────────────────────────
API_KEYS = [
    os.getenv("YOUTUBE_API_KEY"),
    os.getenv("YOUTUBE_API_KEY2"),
    os.getenv("YOUTUBE_API_KEY3"),
    os.getenv("YOUTUBE_API_KEY4"),
    os.getenv("YOUTUBE_API_KEY5"),

]
API_KEYS = [k for k in API_KEYS if k]  # remove empty ones

SEARCH_QUERIES = [
    # --- GENERAL NEPAL ---
    #"नेपाल",
   # "नेपाली",
    #"nepal vlog nepali",
    #"nepal daily life",

    # --- REGIONAL / GEOGRAPHIC DIVERSITY ---
    #"kathmandu vlog nepali",
    #"pokhara vlog nepali",
    #"butwal vlog nepali",
    #"chitwan vlog nepali",
    #"dharan vlog nepali",
    #"biratnagar vlog nepali",
    #"nepalgunj vlog nepali",
    #"hetauda vlog nepali",
    #"dhangadhi vlog nepali",
    #"janakpur vlog nepali",
    #"mustang nepal nepali",
    #"humla jumla nepal nepali",
    #"karnali nepal nepali",
    #"eastern nepal vlog nepali",
    #"western nepal vlog nepali",
    #"far western nepal nepali",
    #"terai nepal vlog nepali",
    #"hilly region nepal nepali",
    #"mountain village nepal nepali",
    #"rural nepal vlog nepali",
    #"गाउँ नेपाल",
    #"पहाड नेपाल",
    #"तराई नेपाल",

    # --- STREET INTERVIEWS ---
    #"nepali street interview",
    #"नेपाली अन्तर्वार्ता",
    #"सडक अन्तर्वार्ता नेपाल",
    #"nepali public interview",
    #"nepal random interview",
    #"nepal public opinion nepali",

    # --- NEWS & CURRENT AFFAIRS ---
    #"नेपाल समाचार",
    #"nepali news today",
    #"nepal news nepali",
    #"नेपाली खबर",
    #"राजनीति नेपl",
    #"nepal election nepali",
    #"nepal government nepali",

    # --- COMEDY & ENTERTAINMENT ---
    #"nepali comedy",
    #"nepali roast",
    #"nepali prank",
    #"nepali short film",
    #"nepali web series",
    #"nepali sitcom",
    #"नेपाली कमेडी",
    #"nepali funny video",
    #"nepali skit",

    # --- MUSIC ---
    #"नेपाली गीत",
    #"nepali song new",
    #"nepali lok dohori",
    #"नेपाली लोक गीत",
    #"nepali pop song",
    #"nepali rap song",
    #"nepali adhunik geet",
    #"nepali movie song",
    #"nepali bhajan",

    # --- LIFESTYLE & FOOD ---
   # "nepali food vlog",
    #"नेपाली खाना",
    #"nepali recipe nepali",
    #"dal bhat nepali",
    #"nepali street food",
    #"nepali kitchen",
    #"नेपाली जीवनशैली",

    # --- TRAVEL & TOURISM ---
    #"nepal travel nepali",
    #"nepal hiking nepali",
    #"nepal trekking vlog nepali",
    #"nepal tourism nepali",
    #"everest base camp nepali",
    #"annapurna trek nepali",
    #"nepal road trip nepali",
   # "nepal travel guide nepali",

    # --- EDUCATION & TECH ---
    #"nepali tutorial nepali",
    #"nepal tech nepali",
    #"nepali education video",
    #"सिक्नुस नेपालीमा",
    "nepali coding tutorial",
    "nepal study vlog",

    # --- AGRICULTURE & RURAL LIFE ---
    "नेपाली किसान",
    "nepal farming nepali",
    "नेपाली कृषि",
    "nepal village life nepali",
    "गाउँको जीवन नेपाल",

    # --- CULTURE & FESTIVALS ---
    "dashain nepal nepali",
    "tihar nepal nepali",
    "नेपाली चाडपर्व",
    "nepal culture nepali",
    "नेपाली संस्कृति",
    "teej nepal nepali",
    "chhath nepal nepali",

    # --- SPORTS ---
    "nepal football nepali",
    "nepal cricket nepali",
    "नेपाल क्रिकेट",
    "nepal sports nepali",

    # --- DIASPORA ---
    "nepali in japan vlog",
    "nepali in korea vlog",
    "nepali in australia vlog",
    "nepali in uk vlog",
    "nepali in usa vlog",
    "nepali abroad life",
    "विदेशमा नेपाली",
]

# ─────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────
OUTPUT_CSV = "data/youtube_comments.csv"
SEEN_VIDEOS_FILE = "data/seen_videos.txt"
SEEN_TEXTS_FILE = "data/seen_texts.txt"

# ─────────────────────────────────────────
# LOAD EXISTING STATE
# ─────────────────────────────────────────
def load_seen_videos():
    if os.path.exists(SEEN_VIDEOS_FILE):
        with open(SEEN_VIDEOS_FILE, "r") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def load_seen_texts():
    """Load existing comment texts to avoid duplicates across runs."""
    seen = set()
    if os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                seen.add(row["text"])
    return seen

def save_seen_video(video_id):
    with open(SEEN_VIDEOS_FILE, "a") as f:
        f.write(video_id + "\n")

def append_comments(comments):
    file_exists = os.path.exists(OUTPUT_CSV)
    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "video_id", "source"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(comments)

# ─────────────────────────────────────────
# API WITH AUTO KEY ROTATION
# ─────────────────────────────────────────
current_key_index = 0

def get_youtube():
    global current_key_index
    return build("youtube", "v3", developerKey=API_KEYS[current_key_index])

def rotate_key():
    global current_key_index
    current_key_index += 1
    if current_key_index >= len(API_KEYS):
        print("\n❌ All API keys exhausted. Run again tomorrow.")
        return False
    print(f"\n🔄 Switching to API key {current_key_index + 1}...")
    return True

# ─────────────────────────────────────────
# SCRAPER FUNCTIONS
# ─────────────────────────────────────────
def search_videos(query, max_results=50):
    while True:
        try:
            youtube = get_youtube()
            request = youtube.search().list(
                q=query,
                part="id,snippet",
                type="video",
                relevanceLanguage="ne",
                maxResults=max_results
            )
            response = request.execute()
            return [item["id"]["videoId"] for item in response.get("items", [])]
        except Exception as e:
            if "quotaExceeded" in str(e):
                if not rotate_key():
                    return []
            else:
                print(f"  Search error for '{query}': {e}")
                return []

def get_comments(video_id):
    comments = []
    while True:
        try:
            youtube = get_youtube()
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                textFormat="plainText"
            )
            while request:
                response = request.execute()
                for item in response.get("items", []):
                    text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                    comments.append({
                        "text": text,
                        "video_id": video_id,
                        "source": "youtube"
                    })
                request = youtube.commentThreads().list_next(request, response)
            return comments
        except Exception as e:
            if "quotaExceeded" in str(e):
                if not rotate_key():
                    return comments  # return what we have so far
            else:
                print(f"  Skipping {video_id}: {e}")
                return comments

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
def main():
    print(f"🔑 Loaded {len(API_KEYS)} API key(s)")

    seen_videos = load_seen_videos()
    seen_texts = load_seen_texts()

    print(f"📹 Already processed: {len(seen_videos)} videos")
    print(f"💬 Already collected: {len(seen_texts)} comments")

    total_new = 0

    for query in SEARCH_QUERIES:
        print(f"\nSearching: '{query}'")
        video_ids = search_videos(query, max_results=50)
        new_videos = [v for v in video_ids if v not in seen_videos]
        print(f"  Found {len(video_ids)} videos, {len(new_videos)} new (skipping {len(video_ids) - len(new_videos)} already done)")

        for vid_id in new_videos:
            print(f"  Fetching: {vid_id}...", end=" ")
            comments = get_comments(vid_id)

            new_comments = []
            for c in comments:
                if c["text"] not in seen_texts:
                    seen_texts.add(c["text"])
                    new_comments.append(c)

            if new_comments:
                append_comments(new_comments)
                total_new += len(new_comments)

            save_seen_video(vid_id)
            seen_videos.add(vid_id)

            print(f"+{len(new_comments)} new (total new this run: {total_new})")
            time.sleep(0.5)

    print(f"\n✅ Done! Added {total_new} new comments this run.")
    print(f"📁 Total in CSV: {len(seen_texts)} comments")

if __name__ == "__main__":
    main()