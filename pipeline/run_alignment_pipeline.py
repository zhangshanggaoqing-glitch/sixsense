import os
import sys
import re
import json
import subprocess
import unicodedata
from pathlib import Path
from faster_whisper import WhisperModel

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_AUDIO_PATH = Path("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2020年07月CET6题+解+音频/202007-CET6 听力.mp3")
RAW_PDF_PATH = Path("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2020年07月CET6题+解+音频/2020.07英语六级考试全1套解析.pdf")
DERIVED_DIR = BASE_DIR / "data" / "derived" / "exams" / "2020-07-set1"
DERIVED_DIR.mkdir(parents=True, exist_ok=True)

def normalize_text(text: str) -> str:
    t = unicodedata.normalize("NFKC", text)
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return t

def norm_word(w: str) -> str:
    return re.sub(r"[^\w']+", "", w.lower())

def split_into_sentences(text: str):
    protected = text
    for abbr in ["Mrs.", "Mr.", "Dr.", "Prof.", "Ms.", "vs.", "U.S.", "e.g.", "i.e."]:
        protected = protected.replace(abbr, abbr.replace(".", "@DOT@"))
    raw_sentences = re.split(r'([.!?]+["\']?\s+)', protected)
    result = []
    i = 0
    while i < len(raw_sentences):
        s = raw_sentences[i]
        if i + 1 < len(raw_sentences):
            s += raw_sentences[i + 1]
            i += 2
        else:
            i += 1
        s = s.replace("@DOT@", ".").strip()
        if s:
            result.append(s)
    return result

def split_chinese_sentences(text: str):
    cleaned = re.sub(r'第\s*\d+\s*/\s*\d+\s*页|淘宝店铺.*|光速考研.*', '', text)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    raw = re.split(r'([。！？；]+)', cleaned)
    res = []
    i = 0
    while i < len(raw):
        s = raw[i]
        if i + 1 < len(raw):
            s += raw[i + 1]
            i += 2
        else:
            i += 1
        s = s.strip()
        if s:
            res.append(s)
    return res

def extract_clean_subparts():
    proc = subprocess.run(["pdftotext", "-layout", str(RAW_PDF_PATH), "-"], capture_output=True, text=True)
    raw = normalize_text(proc.stdout)

    subpart_meta = [
        {"id": "conv-1", "sec": "Section A", "sec_title": "Long Conversations", "title": "Conversation One: Olympic Champion & Technology in Sports", "pat": r"Conversation One\s+科技推动体育进步"},
        {"id": "conv-2", "sec": "Section A", "sec_title": "Long Conversations", "title": "Conversation Two: International Trade & Business Insights", "pat": r"Conversation Two\s+外贸生意"},
        {"id": "pass-1", "sec": "Section B", "sec_title": "Listening Passages", "title": "Passage One: Humor & Stress Relief in the Workplace", "pat": r"Passage One\s+职场幽默"},
        {"id": "pass-2", "sec": "Section B", "sec_title": "Listening Passages", "title": "Passage Two: The Discovery of the Obesity Gene in Mice", "pat": r"Passage Two\s+肥胖基因"},
        {"id": "rec-1", "sec": "Section C", "sec_title": "Recorded Lectures/Talks", "title": "Recording One: Gender Differences in Friendship & Relationships", "pat": r"Recording One\s+友谊的魅力及威胁"},
        {"id": "rec-2", "sec": "Section C", "sec_title": "Recorded Lectures/Talks", "title": "Recording Two: Dinosaur National Monument & Fossil Quarry", "pat": r"Recording Two\s+规模最大的恐龙化石埋藏地"},
        {"id": "rec-3", "sec": "Section C", "sec_title": "Recorded Lectures/Talks", "title": "Recording Three: Aging Styles & Family Structures in America", "pat": r"Recording Three\s+独立自主文化使美国人孤独终老"}
    ]

    offsets = []
    for sp in subpart_meta:
        m = re.search(sp["pat"], raw)
        if m:
            offsets.append((m.start(), sp))

    offsets.sort(key=lambda x: x[0])
    reading_pos = raw.find("Part III Reading Comprehension")
    if reading_pos == -1: reading_pos = len(raw)

    results = []
    for i, (start_idx, sp) in enumerate(offsets):
        end_idx = offsets[i+1][0] if i+1 < len(offsets) else reading_pos
        chunk = raw[start_idx:end_idx]

        pos_rec = chunk.find("二、录音分析")
        pos_sol = chunk.find("三、试题精解")
        rec_chunk = chunk[pos_rec:pos_sol] if pos_rec != -1 and pos_sol != -1 else ""

        trans_m = re.search(r"四[、\s]*全文\s*翻译", chunk)
        trans_chunk = chunk[trans_m.start():] if trans_m else ""

        en_sentences = []
        cur_speaker = ""
        for line in rec_chunk.split("\n"):
            l = line.strip()
            if not l or l.startswith("二、"):
                continue
            if re.search(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]", l):
                continue
            m = re.match(r"^(\d+|[lI])\s*[-–—]\s*([MW]):\s*(.*)", l)
            if m:
                cur_speaker = m.group(2)
                l = m.group(3)
            # Clean OCR artifacts: L before capital letter, and bracketed question markers [ 1 ]
            l = re.sub(r"^L([A-Z])", r"\1", l)
            l = re.sub(r"\s*\[\s*\d+\s*\]\s*", " ", l)
            # Remove Roman numeral markers like II, III, IV, but NOT standalone pronoun 'I'
            l = re.sub(r"\b(II|III|IV|V|VI)\b|[ⅡⅢIVV]", " ", l).strip()
            l = re.sub(r"^[□]\s+", "", l).strip()
            if l and not any(l.startswith(f"Q{q}:") for q in range(1, 26)):
                for s in split_into_sentences(l):
                    if len(s) > 3:
                        en_sentences.append({"speaker": cur_speaker, "text": s})

        zh_sentences = []
        for line in trans_chunk.split("\n"):
            l = line.strip()
            if not l or "全文翻译" in l:
                continue
            l = re.sub(r'^(男|女)\s*[;∶:：]\s*', '', l)
            for s in split_chinese_sentences(l):
                if len(s) > 1:
                    zh_sentences.append(s)

        results.append({
            "meta": sp,
            "en_sentences": en_sentences,
            "zh_sentences": zh_sentences
        })

    return results

def align_official_to_words(subparts):
    print("Loading faster-whisper model...")
    model = WhisperModel("base.en", device="cpu", compute_type="int8")

    print(f"Transcribing {RAW_AUDIO_PATH}...")
    segments, _ = model.transcribe(str(RAW_AUDIO_PATH), word_timestamps=True)
    all_words = []
    for s in segments:
        for w in s.words:
            nw = norm_word(w.word)
            if nw:
                all_words.append({
                    "word": w.word.strip(),
                    "norm": nw,
                    "start": round(w.start, 2),
                    "end": round(w.end, 2)
                })

    print(f"Total whisper words extracted: {len(all_words)}")
    
    # Global alignment cursor
    word_cursor = 0
    total_w = len(all_words)
    global_s_id = 1
    aligned_subparts = []

    # Filter out initial directions (skip until "conversation one")
    for idx, w in enumerate(all_words):
        if w["norm"] == "conversation" and idx + 1 < total_w and all_words[idx + 1]["norm"] == "one":
            word_cursor = idx + 2
            print(f"Conversation One begins at word #{word_cursor}, time={all_words[word_cursor]['start']}s")
            break

    for sp in subparts:
        meta = sp["meta"]
        en_list = sp["en_sentences"]
        zh_list = sp["zh_sentences"]
        aligned_s = []

        print(f"\nAligning {meta['title']} ({len(en_list)} EN, {len(zh_list)} ZH)...")

        for idx, en_item in enumerate(en_list):
            en_text = en_item["text"]
            speaker = en_item["speaker"]
            tokens = [norm_word(t) for t in en_text.split() if norm_word(t)]
            if not tokens:
                continue

            # Look forward in word_cursor for tokens
            # Try to match first 2 tokens
            best_start = None
            window_size = min(150, total_w - word_cursor)
            
            for offset in range(window_size):
                curr = word_cursor + offset
                if all_words[curr]["norm"] == tokens[0]:
                    # check second token if exists
                    if len(tokens) > 1 and curr + 1 < total_w:
                        if all_words[curr + 1]["norm"] == tokens[1]:
                            best_start = curr
                            break
                    else:
                        best_start = curr
                        break

            if best_start is not None:
                start_time = all_words[best_start]["start"]
                # Match end of sentence: try to match last token
                end_pos = min(best_start + len(tokens), total_w - 1)
                last_tok = tokens[-1]
                for off in range(max(0, len(tokens) - 5), min(len(tokens) + 15, total_w - best_start)):
                    curr = best_start + off
                    if curr < total_w and all_words[curr]["norm"] == last_tok:
                        end_pos = curr
                        break
                end_time = max(all_words[end_pos]["end"], start_time + 0.8)
                word_cursor = end_pos + 1
            else:
                # Fallback: estimate from cursor
                curr_time = all_words[min(word_cursor, total_w - 1)]["start"] if word_cursor < total_w else 0.0
                start_time = curr_time
                end_time = curr_time + max(1.5, len(tokens) * 0.35)

            # Map Chinese translation
            zh_text = ""
            if zh_list:
                zh_idx = int(idx * len(zh_list) / max(len(en_list), 1))
                zh_idx = min(zh_idx, len(zh_list) - 1)
                zh_text = zh_list[zh_idx]

            aligned_s.append({
                "id": f"2020-07-s{global_s_id:04d}",
                "order": idx + 1,
                "speaker": speaker,
                "start_time": round(start_time, 2),
                "end_time": round(end_time, 2),
                "english": en_text,
                "chinese": zh_text,
                "confidence": 0.98 if best_start is not None else 0.80
            })
            global_s_id += 1

        aligned_subparts.append({
            "subpart_id": meta["id"],
            "section": meta["sec"],
            "section_title": meta["sec_title"],
            "title": meta["title"],
            "start_time": aligned_s[0]["start_time"] if aligned_s else 0.0,
            "end_time": aligned_s[-1]["end_time"] if aligned_s else 0.0,
            "sentences": aligned_s
        })

    final_output = {
        "exam_id": "2020-07-set1",
        "title": "2020年07月大学英语六级考试真题（全国单套卷）",
        "audio_file": "202007-CET6 听力.mp3",
        "audio_duration": 1611.15,
        "total_sentences": global_s_id - 1,
        "subparts": aligned_subparts
    }

    with open(DERIVED_DIR / "alignment.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, ensure_ascii=False, indent=2)

    print(f"\nAligned {global_s_id - 1} sentences saved to {DERIVED_DIR / 'alignment.json'}")
    return final_output

if __name__ == "__main__":
    subparts = extract_clean_subparts()
    align_official_to_words(subparts)
