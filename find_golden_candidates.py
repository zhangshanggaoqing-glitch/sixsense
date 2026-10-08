import os
import subprocess
from pathlib import Path
import json

root = Path("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频")

sessions = {}

for p in root.rglob("*"):
    if not p.is_file():
        continue
    rel = p.relative_to(root)
    parts = rel.parts
    top_dir = parts[0]
    
    session_key = None
    if "1990" in top_dir and len(parts) > 1 and "CET6" in parts[1]:
        session_key = parts[1].replace("CET6题+解+音频", "").strip()
    elif "CET6" in top_dir:
        session_key = top_dir.replace("CET6题+解+音频", "").replace("【新】", "").strip()
    
    if not session_key:
        continue
    
    if session_key not in sessions:
        sessions[session_key] = {
            "audios": [],
            "papers": [],
            "explanations": [],
            "hints": []
        }
    
    ext = p.suffix.lower()
    name = p.name
    str_p = str(p)
    
    if ext in [".mp3", ".wav", ".m4a"]:
        sessions[session_key]["audios"].append(str(p))
    elif any(k in name for k in ["解析", "详解", "答案"]) or "03、" in str_p or "03" in str_p:
        sessions[session_key]["explanations"].append(str(p))
    elif ext == ".txt":
        sessions[session_key]["hints"].append(str(p))
    else:
        sessions[session_key]["papers"].append(str(p))

analysis_report = []

for skey in sorted(sessions.keys()):
    sdata = sessions[skey]
    audios = [Path(a).name for a in sdata["audios"]]
    expls = sdata["explanations"]
    
    expl_summary = []
    for ep in expls:
        ep_path = Path(ep)
        if ep_path.suffix.lower() == ".pdf":
            try:
                proc = subprocess.run(["pdftotext", str(ep_path), "-"], capture_output=True, text=True, timeout=10)
                txt = proc.stdout
                char_count = len(txt)
                has_transcript = any(k in txt for k in ["Conversation One", "Conversation 1", "Section A", "听力原文"])
                has_translation = any(k in txt for k in ["参考译文", "听力译文", "原文翻译", "【参考译文】"])
                expl_summary.append({
                    "name": ep_path.name,
                    "char_count": char_count,
                    "has_transcript": has_transcript,
                    "has_translation": has_translation,
                    "snippet": txt[max(0, txt.find("Section A")):max(0, txt.find("Section A"))+150].replace('\n', ' ') if "Section A" in txt else ""
                })
            except Exception as e:
                expl_summary.append({"name": ep_path.name, "error": str(e)})

    analysis_report.append({
        "session": skey,
        "audio_count": len(audios),
        "audios": audios,
        "paper_count": len(sdata["papers"]),
        "explanation_count": len(expls),
        "explanations": expl_summary
    })

print("-" * 70)
for r in analysis_report:
    print(f"Session: {r['session']}")
    print(f"  Audios ({r['audio_count']}): {r['audios']}")
    print(f"  Explanations ({r['explanation_count']}):")
    for ex in r["explanations"]:
        has_t = ex.get("has_transcript", False)
        has_tr = ex.get("has_translation", False)
        chars = ex.get("char_count", 0)
        print(f"    - {ex['name']}: {chars} chars | Transcript: {has_t} | Translation: {has_tr}")
        if ex.get("snippet"):
            print(f"      Snippet: {ex['snippet'][:100]}")
    print()

with open("/home/stone/桌面/石头听力/session_summary.json", "w", encoding="utf-8") as f:
    json.dump(analysis_report, f, ensure_ascii=False, indent=2)
