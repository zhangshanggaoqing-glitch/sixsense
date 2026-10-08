import subprocess
import unicodedata
import re

def analyze_guangsu(pdf_path, name):
    res = subprocess.run(["pdftotext", "-layout", pdf_path, "-"], capture_output=True, text=True)
    txt = unicodedata.normalize("NFKC", res.stdout)
    
    print(f"================ {name} ================")
    
    # Find all Conversation, Passage, Recording
    items = ["Conversation One", "Conversation Two", "Section B", "Passage One", "Passage Two", "Section C", "Recording One", "Recording Two", "Recording Three"]
    for it in items:
        pos = txt.find(it)
        print(f"  {it}: pos={pos}")
    
    # Check if questions 1 to 25 exist
    q_matches = re.findall(r'\n\s*([1-9]|1[0-9]|2[0-5])\s*\.\s*[A-D]\)', txt)
    print(f"  Questions found with options: {len(set(q_matches))}/25")

    # Check translations
    trans_pos = txt.find("全文翻译")
    print(f"  Translation '全文翻译' found: {trans_pos != -1}")

analyze_guangsu("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2020年07月CET6题+解+音频/2020.07英语六级考试全1套解析.pdf", "2020-07")
analyze_guangsu("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2020年09月CET6题+解+音频/03、答案解析/2020.09英语六级考试第1套解析.pdf", "2020-09")
