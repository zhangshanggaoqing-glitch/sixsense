import subprocess
from pathlib import Path

p = "/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2022年09月CET6题+解+音频/03、答案解析/2022.09英语六级解析第1套.pdf"
res = subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True)
txt = res.stdout

print(f"Total length: {len(txt)}")

# Find sections
sections = ["Part II", "Section A", "Section B", "Section C", "听力原文", "参考译文", "Part III"]
for s in sections:
    pos = txt.find(s)
    print(f"Section '{s}': pos {pos}")

pos_a = txt.find("Section A")
pos_b = txt.find("Section B")
pos_c = txt.find("Section C")
pos_part3 = txt.find("Part III")

if pos_a != -1:
    print("\n--- Section A Snippet (500 chars) ---")
    print(txt[pos_a:pos_a+500])

if pos_b != -1:
    print("\n--- Section B Snippet (500 chars) ---")
    print(txt[pos_b:pos_b+500])

if pos_c != -1:
    print("\n--- Section C Snippet (500 chars) ---")
    print(txt[pos_c:pos_c+500])
