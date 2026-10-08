import subprocess
from pathlib import Path

root = Path("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/1990年-2018年真题资料【合集】")

for p in sorted(root.rglob("*.pdf")):
    if any(k in p.name for k in ["解析", "详解", "答案"]):
        res = subprocess.run(["pdftotext", str(p), "-"], capture_output=True, text=True)
        txt = res.stdout
        # check if it has Section A or Conversation
        has_sec_a = "Section A" in txt or "Conversation" in txt
        has_trans = "参考译文" in txt or "听力译文" in txt
        print(f"{p.name} (len {len(txt)}) | SecA: {has_sec_a} | Trans: {has_trans}")
        if has_sec_a:
            pos = max(txt.find("Section A"), txt.find("Conversation"))
            print("  Snippet:", txt[pos:pos+150].replace('\n', ' '))
