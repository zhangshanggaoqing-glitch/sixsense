import os
import sys
import json
from collections import defaultdict
from pathlib import Path

SOURCE_DIR = Path("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频")

def audit():
    if not SOURCE_DIR.exists():
        print(f"Error: {SOURCE_DIR} does not exist")
        return

    ext_counter = defaultdict(int)
    total_size = 0
    top_dirs = sorted([d for d in SOURCE_DIR.iterdir() if d.is_dir()])
    
    report = {
        "source_dir": str(SOURCE_DIR),
        "top_level_directories": [],
        "extension_counts": {},
        "per_directory_details": []
    }

    for top_d in top_dirs:
        report["top_level_directories"].append(top_d.name)
        dir_info = {
            "name": top_d.name,
            "audio_files": [],
            "document_files": [],
            "other_files": [],
            "has_mp3": False,
            "has_pdf": False,
            "has_doc": False,
            "has_txt": False,
            "keywords_found": defaultdict(list)
        }

        for root, dirs, files in os.walk(top_d):
            for f in files:
                full_path = Path(root) / f
                rel_file_path = os.path.relpath(full_path, SOURCE_DIR)
                ext = full_path.suffix.lower()
                ext_counter[ext] += 1
                try:
                    size = full_path.stat().st_size
                except Exception:
                    size = 0
                total_size += size

                if ext in ['.mp3', '.m4a', '.wav', '.flac', '.aac', '.wma']:
                    dir_info["has_mp3"] = True
                    dir_info["audio_files"].append({
                        "rel_path": rel_file_path,
                        "name": f,
                        "size_mb": round(size / (1024*1024), 2),
                        "ext": ext
                    })
                elif ext in ['.pdf', '.doc', '.docx', '.txt']:
                    if ext == '.pdf': dir_info["has_pdf"] = True
                    if ext in ['.doc', '.docx']: dir_info["has_doc"] = True
                    if ext == '.txt': dir_info["has_txt"] = True
                    dir_info["document_files"].append({
                        "rel_path": rel_file_path,
                        "name": f,
                        "size_kb": round(size / 1024, 2),
                        "ext": ext
                    })
                else:
                    dir_info["other_files"].append({
                        "rel_path": rel_file_path,
                        "name": f,
                        "ext": ext
                    })

                lower_f = f.lower()
                keywords = ["听力", "音频", "原文", "文本", "解析", "答案", "真题", "翻译", "set", "第1套", "第2套", "第3套", "第一套", "第二套", "第三套"]
                for kw in keywords:
                    if kw in lower_f or kw in f:
                        dir_info["keywords_found"][kw].append(f)

        dir_info["keywords_found"] = dict(dir_info["keywords_found"])
        report["per_directory_details"].append(dir_info)

    report["extension_counts"] = dict(sorted(ext_counter.items(), key=lambda x: -x[1]))
    report["total_size_gb"] = round(total_size / (1024**3), 3)

    out_file = Path("/home/stone/桌面/石头听力/audit_summary.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"Audited {len(top_dirs)} directories.")
    print(f"Total size: {report['total_size_gb']} GB")
    print("Extension counts:")
    for ext, count in report["extension_counts"].items():
        print(f"  {ext or '(no ext)'}: {count}")

if __name__ == "__main__":
    audit()
