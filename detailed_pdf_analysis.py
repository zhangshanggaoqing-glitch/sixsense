import subprocess
import json
from pathlib import Path

root = Path("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频")

analysis_files = []
for p in sorted(root.rglob("*.pdf")):
    if any(k in p.name for k in ["解析", "详解", "答案"]) and "真题" not in p.name or "03" in str(p):
        analysis_files.append(p)

print(f"Total analysis PDFs: {len(analysis_files)}")

results = []
for p in analysis_files:
    # 1. Check pdfinfo
    info_proc = subprocess.run(["pdfinfo", str(p)], capture_output=True, text=True)
    pages = 0
    producer = ""
    for line in info_proc.stdout.split("\n"):
        if "Pages:" in line:
            try: pages = int(line.split(":")[1].strip())
            except: pass
        if "Producer:" in line:
            producer = line.split(":", 1)[1].strip()

    # 2. Extract full text
    text_proc = subprocess.run(["pdftotext", str(p), "-"], capture_output=True, text=True)
    full_text = text_proc.stdout
    char_len = len(full_text)
    
    # Check if listening keywords exist
    has_listening = any(k in full_text for k in [
        "Listening Comprehension", "Conversation One", "Conversation 1", 
        "Section A", "Section B", "Section C", "听力原文", "录音原文", "听力理解"
    ])
    
    # Check if translation exists
    has_translation = any(k in full_text for k in [
        "听力译文", "参考译文", "原文及翻译", "译文", "【参考译文】", "【听力译文】"
    ])

    # Check text quality: ratio of normal ascii letters / Chinese characters
    # vs unprintable or strange unicode
    status = "scanned"
    if char_len > 1000:
        if has_listening:
            status = "has_listening_text"
        else:
            status = "text_no_listening_kw"
    
    results.append({
        "path": str(p.relative_to(root)),
        "name": p.name,
        "pages": pages,
        "size_kb": round(p.stat().st_size / 1024, 1),
        "producer": producer,
        "char_len": char_len,
        "has_listening": has_listening,
        "has_translation": has_translation,
        "status": status
    })

print(f"\nStatus breakdown:")
counts = {}
for r in results:
    s = r["status"]
    counts[s] = counts.get(s, 0) + 1
print(json.dumps(counts, indent=2))

print("\n--- Detailed list of files with listening text ---")
for r in results:
    if r["status"] == "has_listening_text":
        print(f"[{r['char_len']} chars, {r['pages']} pgs, {r['size_kb']} KB] {r['path']}")
        print(f"    has_translation: {r['has_translation']}, producer: {r['producer']}")

with open("/home/stone/桌面/石头听力/pdf_analysis_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
