import subprocess
import unicodedata
import re
import json
from pathlib import Path

def extract_2020_07():
    pdf_path = "/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2020年07月CET6题+解+音频/2020.07英语六级考试全1套解析.pdf"
    res = subprocess.run(["pdftotext", "-layout", pdf_path, "-"], capture_output=True, text=True)
    raw = unicodedata.normalize("NFKC", res.stdout)
    
    # Remove watermarks / header-footer noise
    lines = []
    for line in raw.split("\n"):
        if "淘宝店铺" in line or "光速考研" in line or "第 3/56页" in line or re.search(r'第\s*\d+\s*/\s*\d+\s*页', line):
            continue
        lines.append(line)
    text = "\n".join(lines)
    
    # Boundary between listening and reading
    reading_pos = text.find("Section A\n选词填空")
    if reading_pos == -1:
        # search for 选词填空
        reading_pos = text.find("选词填空")
    print(f"Reading comprehension starts at: {reading_pos}")
    
    listening_text = text[:reading_pos] if reading_pos != -1 else text
    
    # The 7 subparts titles
    subpart_patterns = [
        ("conv-1", "Section A", "Conversation One", "科技推动体育进步", [1, 2, 3, 4]),
        ("conv-2", "Section A", "Conversation Two", "外贸生意", [5, 6, 7, 8]),
        ("pass-1", "Section B", "Passage One", "职场幽默", [9, 10, 11]),
        ("pass-2", "Section B", "Passage Two", "肥胖基因", [12, 13, 14, 15]),
        ("rec-1", "Section C", "Recording One", "友谊的魅力及威胁", [16, 17, 18]),
        ("rec-2", "Section C", "Recording Two", "规模最大的恐龙化石埋藏地", [19, 20, 21]),
        ("rec-3", "Section C", "Recording Three", "独立自主文化使美国人孤独终老", [22, 23, 24, 25])
    ]

    indices = []
    for sp_id, sec, name, topic, q_ids in subpart_patterns:
        pat = rf"{name}\s+{topic}"
        m = re.search(pat, listening_text)
        if m:
            indices.append((m.start(), sp_id, sec, name, topic, q_ids))
        else:
            print(f"NOT FOUND: {name} {topic}")

    indices.sort()
    print(f"Found {len(indices)} subparts.")

    extracted_subparts = []
    for i, (start_idx, sp_id, sec, name, topic, q_ids) in enumerate(indices):
        end_idx = indices[i+1][0] if i+1 < len(indices) else len(listening_text)
        chunk = listening_text[start_idx:end_idx]
        
        # In this chunk, find "二、录音分析" (or where transcript is) and "四、全文翻译"
        pos_rec = chunk.find("二、录音分析")
        pos_sol = chunk.find("三、试题精解")
        pos_trans = chunk.find("四、全文翻译")
        if pos_trans == -1:
            pos_trans = chunk.find("四、全文 翻译")

        print(f"[{sp_id}] {name} {topic}: chunk len={len(chunk)}, rec_pos={pos_rec}, sol_pos={pos_sol}, trans_pos={pos_trans}")

extract_2020_07()
