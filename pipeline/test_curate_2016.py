import json, sqlite3, difflib, re

def clean_word(w):
    return re.sub(r"[^\w]", "", w).lower()

with open("data/derived/exams/2016-06-set1/whisper_full.json") as f:
    w1 = json.load(f)
words1 = [w for seg in w1 for w in seg.get('words', [])]

print("2016-06-set1 total words:", len(words1))
