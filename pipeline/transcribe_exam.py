#!/usr/bin/env python3
import sys
import json
import time
from pathlib import Path
from faster_whisper import WhisperModel

BASE_DIR = Path(__file__).resolve().parent.parent
DERIVED_DIR = BASE_DIR / "data" / "derived" / "exams"

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 transcribe_exam.py <exam_id> <audio_path>")
        sys.exit(1)

    exam_id = sys.argv[1]
    audio_path = Path(sys.argv[2])
    out_dir = DERIVED_DIR / exam_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "whisper_full.json"

    if out_file.exists():
        print(f"[{exam_id}] whisper_full.json already exists: {out_file}")
        return

    print(f"[{exam_id}] Loading Whisper model base.en (CPU 8 threads)...")
    t0 = time.time()
    model = WhisperModel("base.en", device="cpu", compute_type="int8", cpu_threads=8)

    print(f"[{exam_id}] Transcribing {audio_path.name}...")
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

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    elapsed = round(time.time() - t0, 1)
    print(f"[{exam_id}] Transcription complete! Saved {len(data)} segments in {elapsed}s to {out_file}")

if __name__ == "__main__":
    main()
