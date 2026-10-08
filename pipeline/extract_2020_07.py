import subprocess
import unicodedata
import re
import json
from pathlib import Path

def extract_2020_07_all():
    pdf_path = "/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2020年07月CET6题+解+音频/2020.07英语六级考试全1套解析.pdf"
    res = subprocess.run(["pdftotext", "-layout", pdf_path, "-"], capture_output=True, text=True)
    raw = unicodedata.normalize("NFKC", res.stdout)
    
    # Filter header/footer lines
    lines = []
    for line in raw.split("\n"):
        if "淘宝店铺" in line or "光速考研" in line or re.search(r'第\s*\d+\s*/\s*\d+\s*页', line):
            continue
        lines.append(line)
    text = "\n".join(lines)

    subpart_defs = [
        {
            "id": "conv-1",
            "section": "Section A",
            "section_title": "Long Conversations",
            "type": "conversation",
            "title": "Conversation One 科技推动体育进步",
            "questions": [1, 2, 3, 4],
            "pattern": r"Conversation One\s+科技推动体育进步"
        },
        {
            "id": "conv-2",
            "section": "Section A",
            "section_title": "Long Conversations",
            "type": "conversation",
            "title": "Conversation Two 外贸生意",
            "questions": [5, 6, 7, 8],
            "pattern": r"Conversation Two\s+外贸生意"
        },
        {
            "id": "pass-1",
            "section": "Section B",
            "section_title": "Listening Passages",
            "type": "passage",
            "title": "Passage One 职场幽默",
            "questions": [9, 10, 11],
            "pattern": r"Passage One\s+职场幽默"
        },
        {
            "id": "pass-2",
            "section": "Section B",
            "section_title": "Listening Passages",
            "type": "passage",
            "title": "Passage Two 肥胖基因",
            "questions": [12, 13, 14, 15],
            "pattern": r"Passage Two\s+肥胖基因"
        },
        {
            "id": "rec-1",
            "section": "Section C",
            "section_title": "Recorded Lectures/Talks",
            "type": "recording",
            "title": "Recording One 友谊的魅力及威胁",
            "questions": [16, 17, 18],
            "pattern": r"Recording One\s+友谊的魅力及威胁"
        },
        {
            "id": "rec-2",
            "section": "Section C",
            "section_title": "Recorded Lectures/Talks",
            "type": "recording",
            "title": "Recording Two 规模最大的恐龙化石埋藏地",
            "questions": [19, 20, 21],
            "pattern": r"Recording Two\s+规模最大的恐龙化石埋藏地"
        },
        {
            "id": "rec-3",
            "section": "Section C",
            "section_title": "Recorded Lectures/Talks",
            "type": "recording",
            "title": "Recording Three 独立自主文化使美国人孤独终老",
            "questions": [22, 23, 24, 25],
            "pattern": r"Recording Three\s+独立自主文化使美国人孤独终老"
        }
    ]

    # Find offsets
    offsets = []
    for sp in subpart_defs:
        m = re.search(sp["pattern"], text)
        if m:
            offsets.append((m.start(), sp))
        else:
            print("ERROR: Pattern not found for", sp["title"])

    offsets.sort(key=lambda x: x[0])
    
    # Also find where reading begins
    reading_m = re.search(r"选词填空", text)
    reading_start = reading_m.start() if reading_m else len(text)

    extracted_items = []
    for i, (start_idx, sp) in enumerate(offsets):
        end_idx = offsets[i+1][0] if i+1 < len(offsets) else reading_start
        chunk = text[start_idx:end_idx]

        # Extract "二、录音分析" to "三、试题精解"
        pos_rec = chunk.find("二、录音分析")
        pos_sol = chunk.find("三、试题精解")
        rec_chunk = chunk[pos_rec:pos_sol] if pos_rec != -1 and pos_sol != -1 else ""

        # Extract "四、全文翻译" to end of chunk
        pos_trans = re.search(r"四[、\s]*全文\s*翻译", chunk)
        trans_chunk = chunk[pos_trans.start():] if pos_trans else ""

        extracted_items.append({
            "meta": sp,
            "rec_raw": rec_chunk,
            "trans_raw": trans_chunk
        })

    print(f"Extracted chunks for {len(extracted_items)} subparts.")
    return extracted_items

if __name__ == "__main__":
    items = extract_2020_07_all()
    for it in items:
        print(f"Subpart {it['meta']['id']} ({it['meta']['title']}): rec_len={len(it['rec_raw'])}, trans_len={len(it['trans_raw'])}")
