import subprocess
from pathlib import Path

def inspect_pdf(path, name):
    res = subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True)
    txt = res.stdout
    print(f"=== {name} ===")
    print(f"Total characters: {len(txt)}")
    keywords = ["Listening Comprehension", "Section A", "Conversation", "听力原文", "听力录音", "录音原文", "听力理解", "参考译文", "译文", "答案与详解"]
    for kw in keywords:
        pos = txt.find(kw)
        status = f"FOUND at pos {pos}" if pos != -1 else "NOT FOUND"
        print(f"  Keyword '{kw}': {status}")
    return txt

files = [
    ("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2026年06月CET6题+解+音频【新】/2026年6月英语六级解析第1套.pdf", "2026-06 Set 1"),
    ("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2021年12月CET6题+解+音频/03、答案解析/2021.12英语六级解析第1套.pdf", "2021-12 Set 1"),
    ("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2021年06月CET6题+解+音频/03、答案解析/2021.06英语六级答案解析第1套.pdf", "2021-06 Set 1"),
    ("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2020年12月CET6题+解+音频/03、答案解析/2020.12英语六级考试第1套解析.pdf", "2020-12 Set 1"),
    ("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2019年12月CET6题+解+音频/03、答案解析/2019.12英语六级考试解析第1套.pdf", "2019-12 Set 1"),
    ("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2022年06月CET6题+解+音频/03、答案解析/2022.06英语六级考试解析第1套.pdf", "2022-06 Set 1"),
    ("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2022年09月CET6题+解+音频/03、答案解析/2022.09英语六级解析第1套.pdf", "2022-09 Set 1"),
]

for p, n in files:
    inspect_pdf(p, n)
