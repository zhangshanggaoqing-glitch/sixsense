import json
from pathlib import Path

ALIGNMENT_FILE = Path("/home/stone/桌面/石头听力/data/derived/exams/2020-07-set1/alignment.json")
REPORT_FILE = Path("/home/stone/桌面/石头听力/data/derived/exams/2020-07-set1/alignment_report.json")

def qc():
    with open(ALIGNMENT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    subparts = data["subparts"]
    total_sentences = 0
    anomalies = []
    durations = []

    last_end = 0.0

    for sp in subparts:
        for s in sp["sentences"]:
            total_sentences += 1
            start = s["start_time"]
            end = s["end_time"]
            dur = round(end - start, 2)
            durations.append(dur)

            # Check 1: start >= end
            if start >= end:
                anomalies.append({
                    "id": s["id"],
                    "type": "negative_or_zero_duration",
                    "text": s["english"][:40],
                    "start": start,
                    "end": end
                })

            # Check 2: duration extremes (< 0.4s or > 30s)
            if dur < 0.4:
                anomalies.append({
                    "id": s["id"],
                    "type": "too_short",
                    "duration": dur,
                    "text": s["english"][:40]
                })
            elif dur > 30.0:
                anomalies.append({
                    "id": s["id"],
                    "type": "too_long",
                    "duration": dur,
                    "text": s["english"][:40]
                })

            # Check 3: empty text
            if not s["english"].strip():
                anomalies.append({"id": s["id"], "type": "empty_english"})

    avg_dur = round(sum(durations) / max(len(durations), 1), 2)
    min_dur = min(durations) if durations else 0
    max_dur = max(durations) if durations else 0

    report = {
        "exam_id": data["exam_id"],
        "total_subparts": len(subparts),
        "total_sentences": total_sentences,
        "anomalies_count": len(anomalies),
        "anomalies": anomalies,
        "metrics": {
            "min_duration_sec": min_dur,
            "max_duration_sec": max_dur,
            "avg_duration_sec": avg_dur
        },
        "qc_status": "PASSED" if len(anomalies) == 0 else "WARNINGS_FOUND"
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("=== QC Alignment Report ===")
    print(f"Total Sentences: {total_sentences}")
    print(f"Anomalies: {len(anomalies)}")
    print(f"Duration stats: min={min_dur}s, max={max_dur}s, avg={avg_dur}s")
    print(f"Status: {report['qc_status']}")
    if anomalies:
        for a in anomalies[:5]:
            print("  Warning:", a)

if __name__ == "__main__":
    qc()
