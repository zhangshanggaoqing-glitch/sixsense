import json
from pathlib import Path

with open("/home/stone/桌面/石头听力/audit_summary.json", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total Top Directories: {len(data['per_directory_details'])}")
print("-" * 60)

for d in data["per_directory_details"]:
    name = d["name"]
    audios = [a["name"] for a in d["audio_files"]]
    docs = [doc["name"] for doc in d["document_files"]]
    other = [o["name"] for o in d["other_files"]]
    
    print(f"DIR: {name}")
    print(f"  Audios ({len(audios)}):")
    for a in audios:
        print(f"    - {a}")
    print(f"  Docs ({len(docs)}):")
    for doc in docs:
        print(f"    - {doc}")
    if other:
        print(f"  Other ({len(other)}):")
        for o in other:
            print(f"    - {o}")
    print()
