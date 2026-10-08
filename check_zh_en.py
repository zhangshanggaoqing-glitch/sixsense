import subprocess
from pathlib import Path
import re

root = Path("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频")

candidates = []

for p in sorted(root.rglob("*.pdf")):
    if not (any(k in p.name for k in ["解析", "详解", "答案"]) or "03" in str(p)):
        continue
    res = subprocess.run(["pdftotext", "-f", "1", "-l", "15", str(p), "-"], capture_output=True, text=True)
    txt = res.stdout
    if len(txt) < 1000:
        continue
    
    # Check Chinese character validity
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', txt)
    # Check English words
    english_words = re.findall(r'[a-zA-Z]{3,}', txt)
    
    # Check keywords
    has_listening = any(k in txt for k in ["Conversation", "Section A", "听力"])
    
    candidates.append({
        "path": str(p.relative_to(root)),
        "total_chars": len(txt),
        "chinese_char_count": len(chinese_chars),
        "english_word_count": len(english_words),
        "has_listening": has_listening
    })

print(f"Total PDFs with text > 1000 chars: {len(candidates)}")
print(f"{'Path':<65} | {'ZH':<6} | {'EN':<6} | {'Listening'}")
print("-" * 90)
for c in candidates:
    if c["has_listening"]:
        print(f"{c['path'][:65]:<65} | {c['chinese_char_count']:<6} | {c['english_word_count']:<6} | {c['has_listening']}")
