import subprocess
import unicodedata
import re

def test_parse(pdf_path, name):
    res = subprocess.run(["pdftotext", pdf_path, "-"], capture_output=True, text=True)
    raw = res.stdout
    norm = unicodedata.normalize("NFKC", raw)
    
    print(f"================ {name} ================")
    # Look for Section A, Section B, Section C
    for sec in ["Section A", "Section B", "Section C"]:
        pos = norm.find(sec)
        print(f"--- {sec} (pos {pos}) ---")
        if pos != -1:
            snippet = norm[pos:pos+1000]
            print(snippet)

test_parse("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2021年06月CET6题+解+音频/03、答案解析/2021.06英语六级答案解析第1套.pdf", "2021-06 Set 1")
test_parse("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2022年09月CET6题+解+音频/03、答案解析/2022.09英语六级解析第1套.pdf", "2022-09 Set 1")
