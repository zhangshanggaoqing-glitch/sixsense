import os
import re
import json
import sqlite3
import unicodedata
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    import docx
except ImportError:
    docx = None

from faster_whisper import WhisperModel

BASE_DIR = Path("/home/stone/桌面/石头听力")
RAW_SOURCE_DIR = Path("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频")
DATA_DIR = BASE_DIR / "data"
DERIVED_DIR = DATA_DIR / "derived" / "exams"
CHECKPOINT_FILE = DATA_DIR / "derived" / "batch_checkpoint.json"
DB_PATH = DATA_DIR / "sixsense.db"

DERIVED_DIR.mkdir(parents=True, exist_ok=True)

def load_checkpoint() -> Dict[str, Any]:
    if CHECKPOINT_FILE.exists():
        try:
            with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_checkpoint(cp: Dict[str, Any]):
    CHECKPOINT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump(cp, f, ensure_ascii=False, indent=2)

def clean_text(text: str) -> str:
    """Normalize unicode, homoglyphs (Cyrillic A/B/C/E), and strip."""
    text = unicodedata.normalize("NFKC", text)
    homoglyphs = {
        "\u0410": "A", "\u0430": "A",
        "\u0412": "B", "\u0432": "B",
        "\u0421": "C", "\u0441": "C",
        "\u0415": "E", "\u0435": "E"
    }
    for k, v in homoglyphs.items():
        text = text.replace(k, v)
    return text.strip()

def parse_set_number(filename: str) -> int:
    if re.search(r"第\s*2\s*套|2\s*音频|六级\s*2|第二套", filename):
        return 2
    if re.search(r"第\s*3\s*套|3\s*音频|六级\s*3|第三套", filename):
        return 3
    return 1

def discover_all_exams() -> List[Dict[str, Any]]:
    """Scan RAW_SOURCE_DIR for all 2016-2026 exam sessions and matching files."""
    sessions = []
    # 2016-2018 in 1990年-2018年真题资料【合集】
    col_dir = RAW_SOURCE_DIR / "1990年-2018年真题资料【合集】"
    if col_dir.exists():
        for d in sorted(os.listdir(col_dir)):
            if any(y in d for y in ["2016", "2017", "2018"]):
                sessions.append(col_dir / d)

    # 2019-2026
    for d in sorted(os.listdir(RAW_SOURCE_DIR)):
        p = RAW_SOURCE_DIR / d
        if p.is_dir() and "赠" not in d and "1990" not in d:
            sessions.append(p)

    exams = []
    for s_path in sessions:
        folder_name = s_path.name
        ym = re.search(r"(\d{4})年?(\d{2})月", folder_name)
        if not ym:
            continue
        year = int(ym.group(1))
        month = int(ym.group(2))

        mp3s = sorted([p for p in s_path.rglob("*.mp3")])
        docxs = sorted([p for p in s_path.rglob("*.docx")])
        analysis_pdfs = sorted([p for p in s_path.rglob("*解析*.pdf")])
        exam_pdfs = sorted([p for p in s_path.rglob("*.pdf") if p not in analysis_pdfs])

        for mp3 in mp3s:
            mp3_name = mp3.name
            set_num = parse_set_number(mp3_name)
            exam_id = f"{year:04d}-{month:02d}-set{set_num}"
            title = f"{year}年{month:02d}月六级全国真题 (第{set_num}套)"

            # Match docx
            matching_docx = None
            for d in docxs:
                if f"第{set_num}套" in d.name or f"{set_num}套" in d.name or (set_num == 1 and ("全1套" in d.name or "单套" in d.name)):
                    matching_docx = d
                    break
            if not matching_docx and len(docxs) == 1:
                matching_docx = docxs[0]

            # Match exam pdf (question paper)
            matching_exam_pdf = None
            for ep in exam_pdfs:
                if f"第{set_num}套" in ep.name or f"{set_num}套" in ep.name or (set_num == 1 and ("全1套" in ep.name or "第1套" in ep.name)):
                    matching_exam_pdf = ep
                    break
            if not matching_exam_pdf and exam_pdfs:
                matching_exam_pdf = exam_pdfs[0]

            # Match analysis pdf
            matching_analysis_pdf = None
            for p in analysis_pdfs:
                if f"第{set_num}套" in p.name or f"{set_num}套" in p.name or (set_num == 1 and ("全1套" in p.name or "第1套" in p.name)):
                    matching_analysis_pdf = p
                    break
            if not matching_analysis_pdf and analysis_pdfs:
                matching_analysis_pdf = analysis_pdfs[0]

            exams.append({
                "exam_id": exam_id,
                "year": year,
                "month": month,
                "set_num": set_num,
                "title": title,
                "audio_file": mp3_name,
                "audio_path": mp3,
                "docx_path": matching_docx,
                "exam_pdf_path": matching_exam_pdf,
                "analysis_pdf_path": matching_analysis_pdf
            })

    exams.sort(key=lambda x: (x["year"], x["month"], x["set_num"]))
    return exams

def parse_questions_from_text(full_text: str) -> List[Dict[str, Any]]:
    """Universal parser for Questions 1 to 25 with options A, B, C, D."""
    questions = []
    for q_num in range(1, 26):
        pattern = rf"^{q_num}\.\s*(.*?)(?=^\d+\.|\Z)"
        m = re.search(pattern, full_text, re.M | re.S)
        if m:
            block = m.group(1)
            opts = re.findall(r"([A-D])[\.\)]\s*(.*?)(?=(?:[A-D][\.\)]|\Z))", block, re.S)
            opt_dict = {}
            for o_char, o_txt in opts:
                cleaned = re.sub(r"\s+", " ", o_txt).strip()
                cleaned = re.sub(r"(?:Questions?\s+\d+.*|Section\s+[A-C].*|Part\s+[I|V|X]+.*|试\s*题\s*册.*)", "", cleaned, flags=re.I).strip()
                if cleaned:
                    opt_dict[o_char] = cleaned
            if all(k in opt_dict for k in ["A", "B", "C", "D"]):
                questions.append({
                    "num": q_num,
                    "options": [opt_dict["A"], opt_dict["B"], opt_dict["C"], opt_dict["D"]]
                })
    return questions

def extract_docx_questions(docx_path: Path) -> List[Dict[str, Any]]:
    """Extract Questions 1 to 25 from Word .docx booklet."""
    if not docx_path or not docx_path.exists():
        return []
    doc = docx.Document(docx_path)
    in_listening = False
    lines = []
    for p in doc.paragraphs:
        txt = clean_text(p.text)
        if not txt:
            continue
        if re.search(r"Part\s+II.*Listening", txt, re.I) or re.search(r"Section\s+A", txt, re.I):
            in_listening = True
        if re.search(r"Part\s+III.*Reading", txt, re.I):
            in_listening = False
            break
        if in_listening:
            lines.append(txt)

    full_text = "\n".join(lines)
    return parse_questions_from_text(full_text)

def extract_pdf_questions(pdf_path: Path) -> List[Dict[str, Any]]:
    """Extract Questions 1 to 25 from text-based PDF booklet."""
    if not pdf_path or not pdf_path.exists():
        return []
    res = subprocess.run(["pdftotext", str(pdf_path), "-"], capture_output=True, text=True, errors="ignore")
    raw_lines = [clean_text(l) for l in res.stdout.splitlines() if l.strip()]

    # Pre-merge split option markers (e.g. 'B)' on line 1, 'Make predictions' on line 2)
    merged_lines = []
    for l in raw_lines:
        if merged_lines and re.match(r"^[A-D]\)$", merged_lines[-1]):
            merged_lines[-1] = merged_lines[-1] + " " + l
        else:
            merged_lines.append(l)

    in_listening = False
    listening_lines = []
    for l in merged_lines:
        if re.search(r"Part\s+II.*Listening", l, re.I) or re.search(r"Section\s+A", l, re.I):
            in_listening = True
        if re.search(r"Part\s+III.*Reading", l, re.I):
            in_listening = False
            break
        if in_listening:
            listening_lines.append(l)

    full_text = "\n".join(listening_lines)
    return parse_questions_from_text(full_text)

def transcribe_audio_whisper(exam_id: str, audio_path: Path, model: WhisperModel) -> List[Dict[str, Any]]:
    """Transcribe audio with faster-whisper and cache full segments with word timestamps."""
    out_dir = DERIVED_DIR / exam_id
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_path = out_dir / "whisper_full.json"

    if cache_path.exists():
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    print(f"[{exam_id}] Transcribing audio with Whisper base.en (CPU 8-threads)...")
    segments, info = model.transcribe(
        str(audio_path),
        language="en",
        word_timestamps=True,
        vad_filter=True
    )

    data = []
    for seg in segments:
        words = []
        if seg.words:
            for w in seg.words:
                words.append({
                    "word": w.word,
                    "start": round(w.start, 2),
                    "end": round(w.end, 2),
                    "probability": round(w.probability, 3)
                })
        data.append({
            "id": seg.id,
            "start": round(seg.start, 2),
            "end": round(seg.end, 2),
            "text": seg.text.strip(),
            "words": words
        })

    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data

def segment_subparts_from_whisper(segs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Robust 7-subpart detector supporting both numeric digits and words.
    Conv 1 (Q1-Q4), Conv 2 (Q5-Q8), Pass 1 (Q9-Q11/12), Pass 2 (Q12/13-15),
    Rec 1 (Q16-Q18), Rec 2 (Q19-Q21), Rec 3 (Q22-Q25).
    """
    q_cues = [
        ("conv-1", re.compile(r"questions?\s+(?:1|one)(?:\s*[-–]\s*|\s+to\s+)(?:4|four)", re.I)),
        ("conv-2", re.compile(r"questions?\s+(?:5|five)(?:\s*[-–]\s*|\s+to\s+)(?:8|eight)", re.I)),
        ("pass-1", re.compile(r"questions?\s+(?:9|nine)(?:\s*[-–]\s*|\s+to\s+)(?:1[12]|eleven|twelve)", re.I)),
        ("pass-2", re.compile(r"questions?\s+(?:1[23]|twelve|thirteen)(?:\s*[-–]\s*|\s+to\s+)(?:15|fifteen)", re.I)),
        ("rec-1",  re.compile(r"questions?\s+(?:16|sixteen)(?:\s*[-–]\s*|\s+to\s+)(?:1[89]|eighteen|nineteen)", re.I)),
        ("rec-2",  re.compile(r"questions?\s+(?:1[90]|nineteen|twenty)(?:\s*[-–]\s*|\s+to\s+)(?:21|twenty[- ]one)", re.I)),
        ("rec-3",  re.compile(r"questions?\s+(?:22|twenty[- ]two)(?:\s*[-–]\s*|\s+to\s+)(?:25|twenty[- ]five)", re.I)),
    ]

    q_ends = {}
    for name, pat in q_cues:
        for i, s in enumerate(segs):
            if pat.search(s["text"]):
                q_ends[name] = i
                break

    intro_pats = [
        ("conv-1", re.compile(r"conversation\s+(?:1|one)", re.I)),
        ("conv-2", re.compile(r"conversation\s+(?:2|two)", re.I)),
        ("pass-1", re.compile(r"passage\s+(?:1|one)", re.I)),
        ("pass-2", re.compile(r"passage\s+(?:2|two)", re.I)),
        ("rec-1",  re.compile(r"(?:recording|lecture)\s+(?:1|one)", re.I)),
        ("rec-2",  re.compile(r"(?:recording|lecture)\s+(?:2|two)", re.I)),
        ("rec-3",  re.compile(r"(?:recording|lecture)\s+(?:3|three)", re.I)),
    ]
    intro_starts = {}
    for name, pat in intro_pats:
        for i, s in enumerate(segs):
            if pat.search(s["text"]):
                intro_starts[name] = i + 1
                break

    meta_info = {
        "conv-1": {"sec": "sec-a", "type": "conversation", "title": "Conversation 1", "q_range": "Q1 ~ Q4"},
        "conv-2": {"sec": "sec-a", "type": "conversation", "title": "Conversation 2", "q_range": "Q5 ~ Q8"},
        "pass-1": {"sec": "sec-b", "type": "passage", "title": "Passage 1", "q_range": "Q9 ~ Q11"},
        "pass-2": {"sec": "sec-b", "type": "passage", "title": "Passage 2", "q_range": "Q12 ~ Q15"},
        "rec-1":  {"sec": "sec-c", "type": "recording", "title": "Recording 1", "q_range": "Q16 ~ Q18"},
        "rec-2":  {"sec": "sec-c", "type": "recording", "title": "Recording 2", "q_range": "Q19 ~ Q21"},
        "rec-3":  {"sec": "sec-c", "type": "recording", "title": "Recording 3", "q_range": "Q22 ~ Q25"},
    }

    keys = [k for k, _ in q_cues]
    subparts_spec = []
    prev_q_end_seg = 0

    for idx, k in enumerate(keys):
        end_q_idx = q_ends.get(k)
        if end_q_idx is None:
            # Fallback approximate position
            end_seg = min(len(segs) - 1, prev_q_end_seg + 25)
        else:
            end_seg = max(prev_q_end_seg, end_q_idx - 1)

        if k in intro_starts and intro_starts[k] > prev_q_end_seg:
            start_seg = intro_starts[k]
        else:
            start_seg = prev_q_end_seg
            for j in range(prev_q_end_seg, end_seg):
                txt = segs[j]["text"]
                if not re.search(r"^(?:college|directions|in this section|at the end|both the|after you|then mark|question\s+\d+|questions\s+\d+)", txt.strip(), re.I):
                    start_seg = j
                    break

        if start_seg > end_seg:
            start_seg = max(0, end_seg - 15)

        t0 = segs[start_seg]["start"]
        t1 = segs[end_seg]["end"]
        sub_segs = segs[start_seg:end_seg + 1]

        m = meta_info[k]
        subparts_spec.append({
            "id_suffix": k,
            "sec_suffix": m["sec"],
            "type": m["type"],
            "title_en": m["title"],
            "q_range": m["q_range"],
            "start": t0,
            "end": t1,
            "segments": sub_segs
        })

        if end_q_idx is not None:
            next_cand = end_q_idx + 1
            while next_cand < len(segs) and re.search(r"^(?:question\s+\d+|questions\s+\d+)", segs[next_cand]["text"].strip(), re.I):
                next_cand += 1
            prev_q_end_seg = next_cand
        else:
            prev_q_end_seg = end_seg + 5

    return subparts_spec

def build_sentences_from_segments(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Build clean sentences from isolated passage segments."""
    sentences = []
    for s in segments:
        txt = s["text"].strip()
        if re.search(r"^(?:conversation|passage|recording|lecture)\s+(?:one|two|three|1|2|3)", txt, re.I):
            continue
        if re.search(r"^questions?\s+\d+", txt, re.I):
            continue
        if len(txt) < 3:
            continue

        speaker = None
        if re.match(r"^[MW]:", txt):
            speaker = txt[0]
            txt = txt[2:].strip()

        sentences.append({
            "start_time": s["start"],
            "end_time": s["end"],
            "speaker": speaker,
            "english": txt,
            "chinese": "",
            "words": s.get("words", [])
        })
    return sentences

def insert_exam_to_db(exam_meta: Dict[str, Any], subparts_data: List[Dict[str, Any]], questions_data: List[Dict[str, Any]]):
    """Insert or update SQLite database atomically."""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    exam_id = exam_meta["exam_id"]
    year = exam_meta["year"]
    month = exam_meta["month"]
    set_num = exam_meta["set_num"]
    title = exam_meta["title"]
    audio_file = exam_meta["audio_file"]

    tot_duration = subparts_data[-1]["end_time"] if subparts_data else 1600.0

    cursor.execute("""
        INSERT INTO exams (id, year, month, set_number, title, audio_file, audio_duration, is_golden)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        ON CONFLICT(id) DO UPDATE SET
            title=excluded.title,
            audio_file=excluded.audio_file,
            audio_duration=excluded.audio_duration;
    """, (exam_id, year, month, set_num, title, audio_file, tot_duration))

    sections = [
        {"id": f"{exam_id}-sec-a", "type": "long_conversation", "title": "Section A: Long Conversations", "order_num": 1},
        {"id": f"{exam_id}-sec-b", "type": "passage", "title": "Section B: Listening Passages", "order_num": 2},
        {"id": f"{exam_id}-sec-c", "type": "recording", "title": "Section C: Recordings / Talks", "order_num": 3},
    ]
    for sec in sections:
        cursor.execute("""
            INSERT INTO sections (id, exam_id, type, title, order_num)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET title=excluded.title;
        """, (sec["id"], exam_id, sec["type"], sec["title"], sec["order_num"]))

    cursor.execute("DELETE FROM sentences WHERE exam_id = ?", (exam_id,))
    cursor.execute("DELETE FROM questions WHERE exam_id = ?", (exam_id,))
    cursor.execute("DELETE FROM subparts WHERE exam_id = ?", (exam_id,))

    for sp in subparts_data:
        sp_id = sp["id"]
        sec_id = sp["section_id"]
        cursor.execute("""
            INSERT INTO subparts (id, section_id, exam_id, type, title, order_num, start_time, end_time,
                                  questions_json, topic_zh, question_range, sentence_count, duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            sp_id, sec_id, exam_id, sp["type"], sp["title"], sp["order_num"],
            sp["start_time"], sp["end_time"], json.dumps(sp.get("questions_json", [])),
            sp.get("topic_zh", ""), sp.get("question_range", ""),
            len(sp["sentences"]), round(sp["end_time"] - sp["start_time"], 1)
        ))

        for idx, s in enumerate(sp["sentences"], 1):
            sent_id = f"{sp_id}-s{idx:03d}"
            cursor.execute("""
                INSERT INTO sentences (id, exam_id, section_id, subpart_id, order_num, speaker,
                                       start_time, end_time, english, chinese, words_json, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0.95);
            """, (
                sent_id, exam_id, sec_id, sp_id, idx, s.get("speaker"),
                s["start_time"], s["end_time"], s["english"], s.get("chinese", ""),
                json.dumps(s.get("words", []))
            ))

    for q in questions_data:
        q_num = q["num"]
        if 1 <= q_num <= 4:
            subpart_id = f"{exam_id}-conv-1"
        elif 5 <= q_num <= 8:
            subpart_id = f"{exam_id}-conv-2"
        elif 9 <= q_num <= 11:
            subpart_id = f"{exam_id}-pass-1"
        elif 12 <= q_num <= 15:
            subpart_id = f"{exam_id}-pass-2"
        elif 16 <= q_num <= 18:
            subpart_id = f"{exam_id}-rec-1"
        elif 19 <= q_num <= 21:
            subpart_id = f"{exam_id}-rec-2"
        else:
            subpart_id = f"{exam_id}-rec-3"

        opts = q.get("options", ["", "", "", ""])
        q_id = f"{exam_id}-q{q_num:02d}"
        cursor.execute("""
            INSERT INTO questions (id, exam_id, subpart_id, question_num, prompt,
                                   option_a, option_b, option_c, option_d, correct_answer, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            q_id, exam_id, subpart_id, q_num, q.get("prompt", f"Question {q_num}"),
            opts[0] if len(opts) > 0 else "",
            opts[1] if len(opts) > 1 else "",
            opts[2] if len(opts) > 2 else "",
            opts[3] if len(opts) > 3 else "",
            q.get("answer", ""), q.get("explanation", "")
        ))

    conn.commit()
    conn.close()

def process_exam_set(exam_meta: Dict[str, Any], whisper_model: WhisperModel) -> Dict[str, Any]:
    """Process a single exam set end-to-end."""
    exam_id = exam_meta["exam_id"]
    print(f"\n=======================================================")
    print(f"Processing: {exam_meta['title']} ({exam_id})")
    print(f"Audio file: {exam_meta['audio_file']}")

    # 1. Transcribe audio
    segs = transcribe_audio_whisper(exam_id, exam_meta["audio_path"], whisper_model)

    # 2. Extract Questions from docx or exam PDF
    docx_p = exam_meta.get("docx_path")
    pdf_p = exam_meta.get("exam_pdf_path")
    questions = []
    if docx_p and docx_p.exists():
        questions = extract_docx_questions(docx_p)
        print(f"Extracted {len(questions)} questions from Word docx: {docx_p.name}")
    elif pdf_p and pdf_p.exists():
        questions = extract_pdf_questions(pdf_p)
        print(f"Extracted {len(questions)} questions from PDF: {pdf_p.name}")

    # 3. Detect 7 subparts
    sub_specs = segment_subparts_from_whisper(segs)

    # 4. Build subparts and sentences
    subparts_data = []
    total_sentences = 0
    for idx, spec in enumerate(sub_specs, 1):
        sp_id = f"{exam_id}-{spec['id_suffix']}"
        sec_id = f"{exam_id}-{spec['sec_suffix']}"
        sentences = build_sentences_from_segments(spec["segments"])
        total_sentences += len(sentences)

        subparts_data.append({
            "id": sp_id,
            "section_id": sec_id,
            "order_num": idx,
            "type": spec["type"],
            "title": f"{spec['title_en']}",
            "topic_zh": spec["title_en"],
            "question_range": spec["q_range"],
            "start_time": spec["start"],
            "end_time": spec["end"],
            "sentences": sentences
        })
        print(f"  Subpart {idx}: {spec['title_en']:15s} [{spec['q_range']}] {spec['start']:6.1f}s - {spec['end']:6.1f}s ({len(sentences)} sentences)")

    # 5. Insert to DB
    insert_exam_to_db(exam_meta, subparts_data, questions)
    print(f"Successfully imported {exam_id} to DB: {len(subparts_data)} subparts, {total_sentences} sentences, {len(questions)} questions.")

    return {
        "status": "done",
        "subparts": len(subparts_data),
        "sentences": total_sentences,
        "questions": len(questions)
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Batch process CET-6 exams")
    parser.add_argument("--years", type=str, help="Comma separated years to process, e.g. 2024,2025,2026")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of exams to process")
    parser.add_argument("--force", action="store_true", help="Force re-processing")
    args = parser.parse_args()

    exams = discover_all_exams()
    print(f"Discovered {len(exams)} total exam sets in repository.")

    if args.years:
        year_list = [int(y.strip()) for y in args.years.split(",")]
        exams = [e for e in exams if e["year"] in year_list]
        print(f"Filtered to {len(exams)} exams matching years {year_list}")

    if args.limit > 0:
        exams = exams[:args.limit]
        print(f"Limited to first {len(exams)} exams")

    checkpoint = load_checkpoint()

    todo = []
    for e in exams:
        eid = e["exam_id"]
        if eid == "2020-07-set1" and not args.force:
            continue
        if not args.force and eid in checkpoint and checkpoint[eid].get("status") == "done":
            print(f"Skipping already completed: {eid}")
        else:
            todo.append(e)

    print(f"\nExams to process: {len(todo)}")
    if not todo:
        print("All requested exams are already completed!")
        exit(0)

    print("Loading faster-whisper base.en model (int8, 8 threads)...")
    whisper_model = WhisperModel("base.en", device="cpu", compute_type="int8", cpu_threads=8)

    for i, e in enumerate(todo, 1):
        eid = e["exam_id"]
        print(f"\n[{i}/{len(todo)}] Starting {eid}...")
        try:
            res = process_exam_set(e, whisper_model)
            checkpoint[eid] = res
            save_checkpoint(checkpoint)
        except Exception as exc:
            print(f"ERROR processing {eid}: {exc}")
            import traceback
            traceback.print_exc()

    print("\nBatch processing session complete!")
