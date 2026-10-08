import json
import re
import sqlite3
import subprocess
import unicodedata
from pathlib import Path
import docx

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = Path("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2020年07月CET6题+解+音频")
AUDIO_FILE = RAW_DIR / "202007-CET6 听力.mp3"
DOCX_FILE = RAW_DIR / "2020年07月六级真题（全1套）.docx"
PDF_FILE = RAW_DIR / "2020.07英语六级考试全1套解析.pdf"
DB_PATH = BASE_DIR / "data" / "sixsense.db"
WHISPER_PATH = BASE_DIR / "data" / "derived" / "exams" / "2020-07-set1" / "whisper_full.json"

def norm_word(w: str) -> str:
    return re.sub(r"[^\w']+", "", w.lower())

def load_whisper_words():
    with open(WHISPER_PATH, "r", encoding="utf-8") as f:
        segs = json.load(f)
    words = []
    for s in segs:
        for w in s["words"]:
            nw = norm_word(w["word"])
            if nw:
                words.append({
                    "word": w["word"].strip(),
                    "norm": nw,
                    "start": round(w["start"], 2),
                    "end": round(w["end"], 2)
                })
    return words

SUBPART_CONFIGS = [
    {
        "id": "2020-07-set1-conv-1",
        "subpart_code": "conv-1",
        "section_id": "2020-07-set1-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 1 · 科技推动体育进步",
        "topic_zh": "科技推动体育进步",
        "question_range": "Q1 ~ Q4",
        "start_trigger": ["tonight", "we", "have", "a", "very", "special", "guest"],
        "end_trigger": ["considered", "carefully", "on", "a", "case", "by", "case", "basis"]
    },
    {
        "id": "2020-07-set1-conv-2",
        "subpart_code": "conv-2",
        "section_id": "2020-07-set1-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 2 · 外贸生意",
        "topic_zh": "外贸生意",
        "question_range": "Q5 ~ Q8",
        "start_trigger": ["worked", "in", "international", "trade", "all", "my", "life"],
        "end_trigger": ["mostly", "because", "it", "enjoys", "lower", "customs", "duties"]
    },
    {
        "id": "2020-07-set1-pass-1",
        "subpart_code": "pass-1",
        "section_id": "2020-07-set1-sec-b",
        "section_title": "Section B: Listening Passages",
        "type": "passage",
        "title": "Passage 1 · 职场幽默",
        "topic_zh": "职场幽默",
        "question_range": "Q9 ~ Q11",
        "start_trigger": ["too", "many", "people", "view", "their", "jobs"],
        "end_trigger": ["thats", "one", "for", "the", "quote", "board"]
    },
    {
        "id": "2020-07-set1-pass-2",
        "subpart_code": "pass-2",
        "section_id": "2020-07-set1-sec-b",
        "section_title": "Section B: Listening Passages",
        "type": "passage",
        "title": "Passage 2 · 肥胖基因",
        "topic_zh": "肥胖基因",
        "question_range": "Q12 ~ Q15",
        "start_trigger": ["public", "interest", "was", "aroused", "by", "the", "latest", "discovery"],
        "end_trigger": ["can", "itself", "contribute", "to", "obesity"]
    },
    {
        "id": "2020-07-set1-rec-1",
        "subpart_code": "rec-1",
        "section_id": "2020-07-set1-sec-c",
        "section_title": "Section C: Recorded Lectures/Talks",
        "type": "recording",
        "title": "Recording 1 · 友谊的魅力及威胁",
        "topic_zh": "友谊的魅力及威胁",
        "question_range": "Q16 ~ Q18",
        "start_trigger": ["qualities", "of", "a", "relationship", "such", "as", "openness"],
        "end_trigger": ["a", "good", "friendship", "is", "hard", "to", "find"]
    },
    {
        "id": "2020-07-set1-rec-2",
        "subpart_code": "rec-2",
        "section_id": "2020-07-set1-sec-c",
        "section_title": "Section C: Recorded Lectures/Talks",
        "type": "recording",
        "title": "Recording 2 · 规模最大的恐龙化石埋藏地",
        "topic_zh": "规模最大的恐龙化石埋藏地",
        "question_range": "Q19 ~ Q21",
        "start_trigger": ["the", "partial", "skeletons", "of", "more", "than", "20", "dinosaurs"],
        "end_trigger": ["decaying", "bodies", "of", "buffalo", "that", "had", "died", "during", "spring", "floods"]
    },
    {
        "id": "2020-07-set1-rec-3",
        "subpart_code": "rec-3",
        "section_id": "2020-07-set1-sec-c",
        "section_title": "Section C: Recorded Lectures/Talks",
        "type": "recording",
        "title": "Recording 3 · 独立自主文化使美国人孤独终老",
        "topic_zh": "独立自主文化使美国人孤独终老",
        "question_range": "Q22 ~ Q25",
        "start_trigger": ["would", "like", "particularly", "to", "talk", "about", "the", "need"],
        "end_trigger": ["why", "their", "grandparents", "say", "the", "things", "they", "do"]
    }
]

def extract_docx_questions():
    doc = docx.Document(DOCX_FILE)
    in_listening = False
    q_blocks = {}
    curr_q = None

    for p in doc.paragraphs:
        txt = p.text.strip()
        if 'Part II' in txt and 'Listening' in txt:
            in_listening = True
            continue
        if 'Part III' in txt:
            in_listening = False
            break
        if not in_listening or not txt:
            continue
            
        m = re.match(r'^(\d+)\.\s*(.*)', txt)
        if m:
            curr_q = int(m.group(1))
            q_blocks[curr_q] = m.group(2)
        elif curr_q is not None:
            q_blocks[curr_q] += ' ' + txt

    questions = {}
    for q in range(1, 26):
        raw = q_blocks.get(q, '')
        clean = re.sub(r'(Section [A-C]|Directions.*?heard\.|Questions \d+ to \d+.*?heard\.)', '', raw, flags=re.DOTALL)
        opts = {}
        matches = list(re.finditer(r'([A-D])\)\s*', clean))
        for i, m in enumerate(matches):
            letter = m.group(1)
            start = m.end()
            end = matches[i+1].start() if i + 1 < len(matches) else len(clean)
            opt_text = clean[start:end].strip()
            opts[letter] = opt_text
        questions[q] = opts
    return questions

def extract_pdf_solutions():
    res = subprocess.run(['pdftotext', '-layout', str(PDF_FILE), '-'], capture_output=True, text=True)
    pdf_text = unicodedata.normalize('NFKC', res.stdout)
    
    prompts = {
        1: "What do we learn about Anna Sanchez?",
        2: "What is the woman's book mainly about?",
        3: "What has changed in the past thousands of years?",
        4: "What is the man's concern about the use of technology in sports competitions?",
        5: "What does the woman think is required to be successful in international trade?",
        6: "What does the woman say is special about her way of doing business?",
        7: "What does the woman have in both Italy and China?",
        8: "What does the woman say makes furniture marginally more profitable?",
        9: "What does the passage say about humor in the workplace?",
        10: "What does the study by Howard Polio show?",
        11: "What can Kodak's employees do in the humor room?",
        12: "What does the speaker say has aroused public interest?",
        13: "What do we learn about the changed gene?",
        14: "What does University of Vermont psychologist Esther Rothblum say?",
        15: "What accounts for Americans' obesity according to a survey by the Center for Disease Control?",
        16: "What quality do men value most concerning friendship according to a questionnaire response?",
        17: "What do women refer to when speaking of close friendships?",
        18: "What may threaten a friendship for both men and women?",
        19: "Where can many of the best dinosaur specimens be seen today?",
        20: "What occurs to many people when they see the massive bones in the pit wall?",
        21: "What does the speaker suggest about the large number of dinosaur bones in the pit?",
        22: "What ideal influences American aging style?",
        23: "What does the speaker say about old people in the United States?",
        24: "What is astonishing to the young mothers interviewed by the speaker?",
        25: "What does the speaker say older people try their best to do?"
    }

    answers = {
        1: "A", 2: "D", 3: "B", 4: "C",
        5: "B", 6: "D", 7: "A", 8: "C",
        9: "A", 10: "D", 11: "B",
        12: "A", 13: "D", 14: "C", 15: "B",
        16: "A", 17: "D", 18: "C",
        19: "D", 20: "B", 21: "A",
        22: "B", 23: "D", 24: "B", 25: "B"
    }

    explanations = {}
    for m in re.finditer(r'【答案精析】\s*([A-D])[\s\.、]*(.*?)(?=\n\s*(?:【|\d+\s*[\.、]|四、|$))', pdf_text, re.DOTALL):
        ans = m.group(1)
        expl = m.group(2).strip()
        expl = re.sub(r'\s+', ' ', expl)
        pre = pdf_text[max(0, m.start()-600):m.start()]
        q_matches = list(re.finditer(r'(\d+)\s*[\.、]', pre))
        if q_matches:
            q_num = int(q_matches[-1].group(1))
            if 1 <= q_num <= 25 and q_num not in explanations:
                explanations[q_num] = expl[:300]

    return prompts, answers, explanations

def build_full_clean_dataset():
    whisper_words = load_whisper_words()
    total_w = len(whisper_words)
    docx_questions = extract_docx_questions()
    prompts, answers, explanations = extract_pdf_solutions()

    subpart_q_map = {
        "conv-1": [1, 2, 3, 4],
        "conv-2": [5, 6, 7, 8],
        "pass-1": [9, 10, 11],
        "pass-2": [12, 13, 14, 15],
        "rec-1": [16, 17, 18],
        "rec-2": [19, 20, 21],
        "rec-3": [22, 23, 24, 25]
    }

    res = subprocess.run(['pdftotext', '-layout', str(PDF_FILE), '-'], capture_output=True, text=True)
    raw_pdf = unicodedata.normalize('NFKC', res.stdout)
    clean_pdf = '\n'.join([l for l in raw_pdf.split('\n') if not ('淘宝店铺' in l or '光速考研' in l or re.search(r'第\s*\d+\s*/\s*\d+\s*页', l))])

    pdf_subparts = [
        ('conv-1', r'Conversation One\s+科技推动体育进步'),
        ('conv-2', r'Conversation Two\s+外贸生意'),
        ('pass-1', r'Passage One\s+职场幽默'),
        ('pass-2', r'Passage Two\s+肥胖基因'),
        ('rec-1', r'Recording One\s+友谊的魅力及威胁'),
        ('rec-2', r'Recording Two\s+规模最大的恐龙化石埋藏地'),
        ('rec-3', r'Recording Three\s+独立自主文化使美国人孤独终老')
    ]

    offsets = []
    for sid, pat in pdf_subparts:
        m = re.search(pat, clean_pdf)
        if m: offsets.append((m.start(), sid))
    offsets.sort(key=lambda x: x[0])
    reading_pos = clean_pdf.find('Part III Reading Comprehension')
    if reading_pos == -1: reading_pos = len(clean_pdf)

    subpart_chunks = {}
    for i, (st, sid) in enumerate(offsets):
        en = offsets[i+1][0] if i+1 < len(offsets) else reading_pos
        subpart_chunks[sid] = clean_pdf[st:en]

    word_cursor = 0
    all_clean_subparts = []
    all_clean_questions = []

    for cfg in SUBPART_CONFIGS:
        sid = cfg["subpart_code"]
        chunk = subpart_chunks[sid]
        
        st_tokens = cfg["start_trigger"]
        end_tokens = cfg["end_trigger"]

        sp_start_idx = None
        for i in range(word_cursor, total_w - len(st_tokens)):
            if all(whisper_words[i + k]["norm"] == st_tokens[k] for k in range(len(st_tokens))):
                sp_start_idx = i
                break
        if sp_start_idx is None:
            sp_start_idx = word_cursor

        sp_end_idx = None
        for i in range(sp_start_idx, total_w - len(end_tokens)):
            if all(whisper_words[i + k]["norm"] == end_tokens[k] for k in range(len(end_tokens))):
                sp_end_idx = i + len(end_tokens) - 1
                break
        if sp_end_idx is None:
            sp_end_idx = min(sp_start_idx + 400, total_w - 1)

        subpart_words = whisper_words[sp_start_idx:sp_end_idx + 1]
        word_cursor = sp_end_idx + 1

        print(f"\nSubpart {sid} ({cfg['title']}): words={len(subpart_words)}, time: {subpart_words[0]['start']}s -> {subpart_words[-1]['end']}s")

        trans_m = re.search(r'四[、\s]*全文\s*翻译', chunk)
        zh_sentences = []
        if trans_m:
            trans_chunk = chunk[trans_m.start():]
            trans_lines = [l.strip() for l in trans_chunk.split('\n') if l.strip() and '全文翻译' not in l and not l.startswith('Section') and not l.startswith('Part')]
            full_zh = ' '.join(trans_lines)
            full_zh = re.sub(r'(男|女)\s*[;∶:：]\s*', '', full_zh)
            raw_zh = re.split(r'([。！？；]+)', full_zh)
            for j in range(0, len(raw_zh), 2):
                s = raw_zh[j] + (raw_zh[j+1] if j+1 < len(raw_zh) else '')
                s = s.strip()
                if len(s) > 1 and not s.startswith('第') and not s.startswith('淘宝'):
                    zh_sentences.append(s)

        pos_rec = chunk.find('二、录音分析')
        cut_candidates = [chunk.find(k) for k in ['【问题分析】', '【问题精解】', '三、试题精解'] if chunk.find(k) != -1]
        pos_end = min(cut_candidates) if cut_candidates else len(chunk)
        rec_chunk = chunk[pos_rec:pos_end] if pos_rec != -1 else ''

        clean_lines = []
        in_text = False
        cur_speaker = ""
        for line in rec_chunk.split('\n'):
            l = line.strip()
            if not l or l.startswith('二、'):
                continue
            m_spk = re.match(r'^(\d+|[lI])\s*[-–—]\s*([MW]):\s*(.*)', l)
            is_para = bool(re.match(r'^(I|II|III|IV|V|VI|VII)\b', l))
            
            if m_spk:
                in_text = True
                cur_speaker = m_spk.group(2)
                l = m_spk.group(3)
            elif is_para:
                in_text = True
                cur_speaker = ""
                l = re.sub(r'^(I|II|III|IV|V|VI|VII)\b\s*', '', l)
            elif re.search(r'[\u4e00-\u9fff]', l):
                in_text = False

            if in_text and not re.search(r'[\u4e00-\u9fff]', l):
                l = re.sub(r'\s*\[\s*\d+\s*\]\s*', ' ', l)
                l = re.sub(r'\s*[回圆□]\s*', ' ', l)
                l = re.sub(r'^L([A-Z])', r'\1', l)
                if '..' in l or l.startswith('Q') or l.startswith('【'):
                    continue
                if l.strip():
                    clean_lines.append((cur_speaker, l.strip()))

        full_en = ' '.join([line for _, line in clean_lines])

        for abbr in ["Mrs.", "Mr.", "Dr.", "Prof.", "Ms.", "vs.", "U.S.", "e.g.", "i.e."]:
            full_en = full_en.replace(abbr, abbr.replace(".", "@DOT@"))

        split_en = re.split(r'([.!?]+["\']?\s+)', full_en)
        en_sentences = []
        k = 0
        while k < len(split_en):
            s = split_en[k]
            if k + 1 < len(split_en):
                s += split_en[k+1]
                k += 2
            else:
                k += 1
            s = s.replace("@DOT@", ".").strip()
            s = re.sub(r'^(\d+|[lI])\s*[-–—]\s*[MW]:\s*', '', s)
            if len(s) > 4:
                en_sentences.append(s)

        print(f"  Extracted {len(en_sentences)} EN sentences, {len(zh_sentences)} ZH sentences.")

        sub_cursor = 0
        aligned_sentences = []
        num_en = len(en_sentences)
        num_zh = len(zh_sentences)

        for s_idx, en_text in enumerate(en_sentences):
            tokens = [norm_word(w) for w in en_text.split() if norm_word(w)]
            if not tokens:
                continue

            start_tok_idx = None
            window = min(80, len(subpart_words) - sub_cursor)
            for off in range(window):
                cur = sub_cursor + off
                if subpart_words[cur]["norm"] == tokens[0]:
                    if len(tokens) > 1 and cur + 1 < len(subpart_words):
                        if subpart_words[cur+1]["norm"] == tokens[1]:
                            start_tok_idx = cur
                            break
                    else:
                        start_tok_idx = cur
                        break

            if start_tok_idx is not None:
                start_time = subpart_words[start_tok_idx]["start"]
                last_tok = tokens[-1]
                end_tok_idx = min(start_tok_idx + len(tokens), len(subpart_words) - 1)
                for off in range(max(0, len(tokens) - 5), min(len(tokens) + 12, len(subpart_words) - start_tok_idx)):
                    cur = start_tok_idx + off
                    if cur < len(subpart_words) and subpart_words[cur]["norm"] == last_tok:
                        end_tok_idx = cur
                        break
                end_time = max(subpart_words[end_tok_idx]["end"], start_time + 0.8)
                sub_cursor = end_tok_idx + 1
            else:
                cur_time = subpart_words[min(sub_cursor, len(subpart_words)-1)]["start"]
                start_time = cur_time
                end_time = cur_time + max(1.5, len(tokens) * 0.35)

            zh_idx = int(s_idx * num_zh / max(num_en, 1))
            zh_idx = min(zh_idx, num_zh - 1)
            zh_text = zh_sentences[zh_idx] if zh_sentences else ""

            aligned_sentences.append({
                "id": f"{cfg['id']}-s{s_idx+1:03d}",
                "order_num": s_idx + 1,
                "speaker": "M" if "conv" in sid and s_idx % 2 == 0 else "W" if "conv" in sid else "",
                "start_time": round(start_time, 2),
                "end_time": round(end_time, 2),
                "english": en_text,
                "chinese": zh_text,
                "confidence": 0.98 if start_tok_idx is not None else 0.85
            })

        duration = round(aligned_sentences[-1]["end_time"] - aligned_sentences[0]["start_time"], 1) if aligned_sentences else 0.0

        all_clean_subparts.append({
            "id": cfg["id"],
            "subpart_code": sid,
            "section_id": cfg["section_id"],
            "type": cfg["type"],
            "title": cfg["title"],
            "topic_zh": cfg["topic_zh"],
            "question_range": cfg["question_range"],
            "order_num": len(all_clean_subparts) + 1,
            "start_time": aligned_sentences[0]["start_time"] if aligned_sentences else 0.0,
            "end_time": aligned_sentences[-1]["end_time"] if aligned_sentences else 0.0,
            "duration": duration,
            "sentence_count": len(aligned_sentences),
            "sentences": aligned_sentences
        })

        for q_num in subpart_q_map[sid]:
            opts = docx_questions.get(q_num, {})
            all_clean_questions.append({
                "id": f"2020-07-q{q_num:02d}",
                "exam_id": "2020-07-set1",
                "subpart_id": cfg["id"],
                "question_num": q_num,
                "prompt": prompts.get(q_num, f"Question {q_num}"),
                "option_a": opts.get("A", ""),
                "option_b": opts.get("B", ""),
                "option_c": opts.get("C", ""),
                "option_d": opts.get("D", ""),
                "correct_answer": answers.get(q_num, "A"),
                "explanation": explanations.get(q_num, "")
            })

    derived_dir = BASE_DIR / "data" / "derived" / "exams" / "2020-07-set1"
    derived_dir.mkdir(parents=True, exist_ok=True)

    with open(derived_dir / "alignment.json", "w", encoding="utf-8") as f:
        json.dump({
            "exam_id": "2020-07-set1",
            "title": "2020年07月大学英语六级考试真题（全国单套卷）",
            "audio_file": "202007-CET6 听力.mp3",
            "audio_duration": 1611.15,
            "subparts": all_clean_subparts
        }, f, ensure_ascii=False, indent=2)

    with open(derived_dir / "questions.json", "w", encoding="utf-8") as f:
        json.dump(all_clean_questions, f, ensure_ascii=False, indent=2)

    print(f"\nSaved {len(all_clean_subparts)} subparts and {len(all_clean_questions)} questions to derived files.")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS questions")
    cur.execute("""
        CREATE TABLE questions (
            id TEXT PRIMARY KEY,
            exam_id TEXT NOT NULL,
            subpart_id TEXT NOT NULL,
            question_num INTEGER NOT NULL,
            prompt TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            explanation TEXT
        )
    """)

    cur.execute("PRAGMA table_info(subparts)")
    cols = [r[1] for r in cur.fetchall()]
    if "topic_zh" not in cols:
        cur.execute("ALTER TABLE subparts ADD COLUMN topic_zh TEXT DEFAULT ''")
    if "question_range" not in cols:
        cur.execute("ALTER TABLE subparts ADD COLUMN question_range TEXT DEFAULT ''")
    if "sentence_count" not in cols:
        cur.execute("ALTER TABLE subparts ADD COLUMN sentence_count INTEGER DEFAULT 0")
    if "duration" not in cols:
        cur.execute("ALTER TABLE subparts ADD COLUMN duration REAL DEFAULT 0.0")

    cur.execute("DELETE FROM subparts WHERE id LIKE '2020-07%'")
    for sp in all_clean_subparts:
        cur.execute("""
            INSERT INTO subparts (id, section_id, type, title, topic_zh, question_range, order_num, start_time, end_time, sentence_count, duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sp["id"], sp["section_id"], sp["type"], sp["title"], sp["topic_zh"], sp["question_range"],
            sp["order_num"], sp["start_time"], sp["end_time"], sp["sentence_count"], sp["duration"]
        ))

    cur.execute("DELETE FROM sentences WHERE exam_id = '2020-07-set1'")
    total_s = 0
    for sp in all_clean_subparts:
        for s in sp["sentences"]:
            cur.execute("""
                INSERT INTO sentences (id, exam_id, section_id, subpart_id, order_num, speaker, start_time, end_time, english, chinese, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                s["id"], "2020-07-set1", sp["section_id"], sp["id"], s["order_num"],
                s["speaker"], s["start_time"], s["end_time"], s["english"], s["chinese"], s["confidence"]
            ))
            total_s += 1

    for q in all_clean_questions:
        cur.execute("""
            INSERT INTO questions (id, exam_id, subpart_id, question_num, prompt, option_a, option_b, option_c, option_d, correct_answer, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            q["id"], q["exam_id"], q["subpart_id"], q["question_num"], q["prompt"],
            q["option_a"], q["option_b"], q["option_c"], q["option_d"], q["correct_answer"], q["explanation"]
        ))

    conn.commit()
    conn.close()

    print(f"Database successfully updated: {len(all_clean_subparts)} subparts, {total_s} sentences, {len(all_clean_questions)} questions.")

if __name__ == "__main__":
    build_full_clean_dataset()
