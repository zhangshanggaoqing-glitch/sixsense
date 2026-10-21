import json
import re
import time
import urllib.parse
import urllib.request
from typing import Optional, List
from fastapi import APIRouter, Query, Response, HTTPException
from backend.app.database import get_connection

router = APIRouter(prefix="/api/dict", tags=["Dictionary"])

CACHE_TTL_SECONDS = 30 * 86400  # 30 days cache for dictionary lookups

def query_youdao(word: str) -> Optional[dict]:
    clean = re.sub(r"[^\w'-]+", "", word.strip()).lower()
    if not clean:
        return None

    url = f"https://dict.youdao.com/jsonapi?q={urllib.parse.quote(clean)}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            if res.status != 200:
                return None
            data = json.loads(res.read().decode("utf-8"))
    except Exception as e:
        print(f"Youdao query error for {word}: {e}")
        return None

    result = {
        "word": clean,
        "lemma": clean,
        "phonetic_uk": "",
        "phonetic_us": "",
        "audio_uk": f"/api/dict/voice?word={clean}&type=1",
        "audio_us": f"/api/dict/voice?word={clean}&type=2",
        "audio_uk_direct": f"https://dict.youdao.com/dictvoice?audio={urllib.parse.quote(clean)}&type=1",
        "audio_us_direct": f"https://dict.youdao.com/dictvoice?audio={urllib.parse.quote(clean)}&type=2",
        "definitions": [],
        "tags": [],
        "examples": []
    }

    # 1. English-Chinese (ec)
    ec = data.get("ec", {})
    ec_words = ec.get("word", [])
    if ec_words:
        w_info = ec_words[0]
        result["phonetic_uk"] = w_info.get("ukphone", "") or ""
        result["phonetic_us"] = w_info.get("usphone", "") or ""

        # Tags
        tags = ec.get("exam_type", [])
        if tags:
            result["tags"] = tags

        # Definitions
        for tr in w_info.get("trs", []):
            l_entry = tr.get("tr", [{}])[0].get("l", {})
            i_list = l_entry.get("i", [])
            for item in i_list:
                if isinstance(item, str) and item.strip():
                    m = re.match(r"^([a-zA-Z]+\.)\s*(.*)$", item.strip())
                    if m:
                        result["definitions"].append({"pos": m.group(1), "meaning": m.group(2)})
                    else:
                        result["definitions"].append({"pos": "", "meaning": item.strip()})

    # 2. Simple fallback
    if not result["definitions"] and "simple" in data:
        for s in data.get("simple", {}).get("word", []):
            for tr in s.get("trs", []):
                for tr_sub in tr.get("tr", []):
                    text = tr_sub.get("l", {}).get("i", [""])[0]
                    if text:
                        m = re.match(r"^([a-zA-Z]+\.)\s*(.*)$", text.strip())
                        if m:
                            result["definitions"].append({"pos": m.group(1), "meaning": m.group(2)})
                        else:
                            result["definitions"].append({"pos": "", "meaning": text.strip()})

    # 3. Bilingual context examples (top 2)
    blng = data.get("blng_sents_part", {}).get("sentence-pair", [])
    for pair in blng[:2]:
        en = pair.get("sentence-eng", "")
        zh = pair.get("sentence-translation", "")
        if en and zh:
            clean_en = re.sub(r"</?[a-zA-Z0-9]+[^>]*>", "", en)
            result["examples"].append({"en": clean_en, "zh": zh})

    if not result["definitions"]:
        return None

    return result


def query_free_dict_fallback(word: str) -> Optional[dict]:
    clean = re.sub(r"[^\w'-]+", "", word.strip()).lower()
    if not clean:
        return None

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.parse.quote(clean)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=4) as res:
            if res.status != 200:
                return None
            data = json.loads(res.read().decode("utf-8"))
            if not isinstance(data, list) or len(data) == 0:
                return None
            entry = data[0]
            phonetics = entry.get("phonetics", [])
            text_phone = entry.get("phonetic", "")
            uk_phone = next((p.get("text", "") for p in phonetics if "uk" in p.get("audio", "").lower() and p.get("text")), text_phone)
            us_phone = next((p.get("text", "") for p in phonetics if "us" in p.get("audio", "").lower() and p.get("text")), text_phone)

            defs = []
            for m in entry.get("meanings", []):
                pos = m.get("partOfSpeech", "")
                for d in m.get("definitions", [])[:2]:
                    defs.append({"pos": f"{pos}.", "meaning": d.get("definition", "")})

            return {
                "word": clean,
                "lemma": clean,
                "phonetic_uk": uk_phone.strip("/"),
                "phonetic_us": us_phone.strip("/"),
                "audio_uk": f"/api/dict/voice?word={clean}&type=1",
                "audio_us": f"/api/dict/voice?word={clean}&type=2",
                "audio_uk_direct": f"https://dict.youdao.com/dictvoice?audio={urllib.parse.quote(clean)}&type=1",
                "audio_us_direct": f"https://dict.youdao.com/dictvoice?audio={urllib.parse.quote(clean)}&type=2",
                "definitions": defs[:3],
                "tags": ["FreeDict"],
                "examples": []
            }
    except Exception:
        return None


@router.get("/lookup")
def lookup_word(word: str = Query(..., description="English word to look up")):
    clean = re.sub(r"[^\w'-]+", "", word.strip()).lower()
    if not clean:
        raise HTTPException(status_code=400, detail="Word cannot be empty")

    now = time.time()
    conn = get_connection()
    cursor = conn.cursor()

    # Check cache first
    cursor.execute("SELECT data_json, updated_at FROM dictionary_cache WHERE word = ?", (clean,))
    row = cursor.fetchone()
    if row:
        data_json, updated_at = row["data_json"], row["updated_at"]
        if now - updated_at < CACHE_TTL_SECONDS:
            conn.close()
            try:
                return json.loads(data_json)
            except Exception:
                pass

    # Fetch from Youdao
    result = query_youdao(clean)

    # Fallback to Free Dictionary API
    if not result:
        result = query_free_dict_fallback(clean)

    # Ultimate fallback if completely offline or missing
    if not result:
        result = {
            "word": clean,
            "lemma": clean,
            "phonetic_uk": clean,
            "phonetic_us": clean,
            "audio_uk": f"/api/dict/voice?word={clean}&type=1",
            "audio_us": f"/api/dict/voice?word={clean}&type=2",
            "audio_uk_direct": f"https://dict.youdao.com/dictvoice?audio={urllib.parse.quote(clean)}&type=1",
            "audio_us_direct": f"https://dict.youdao.com/dictvoice?audio={urllib.parse.quote(clean)}&type=2",
            "definitions": [{"pos": "", "meaning": "CET-6 核心听力词汇"}],
            "tags": ["CET6"],
            "examples": []
        }

    # Save to cache
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO dictionary_cache (word, data_json, updated_at)
            VALUES (?, ?, ?);
        """, (clean, json.dumps(result, ensure_ascii=False), now))
        conn.commit()
    except Exception as e:
        print(f"Failed to cache word {clean}: {e}")
    finally:
        conn.close()

    return result


@router.get("/voice")
def stream_word_voice(
    word: str = Query(..., description="Word to pronounce"),
    type: int = Query(2, description="1 for UK, 2 for US")
):
    clean = re.sub(r"[^\w'-]+", "", word.strip()).lower()
    if not clean:
        raise HTTPException(status_code=400, detail="Word is required")

    voice_type = 1 if type == 1 else 2
    url = f"https://dict.youdao.com/dictvoice?audio={urllib.parse.quote(clean)}&type={voice_type}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            audio_bytes = res.read()
            return Response(
                content=audio_bytes,
                media_type="audio/mpeg",
                headers={
                    "Cache-Control": "public, max-age=604800, immutable",
                    "Accept-Ranges": "bytes",
                    "Content-Disposition": f'inline; filename="{clean}_{"uk" if voice_type == 1 else "us"}.mp3"'
                }
            )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch pronunciation voice: {e}")
