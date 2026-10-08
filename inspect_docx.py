import os
from pathlib import Path
import docx

def test_docx(p):
    try:
        doc = docx.Document(p)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return len(paragraphs), paragraphs[:10]
    except Exception as e:
        return 0, [f"Error: {e}"]

# Check a recent year with docx, e.g., 2023年12月 or 2024年06月
sample_dirs = [
    "/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2024年06月CET6题+解+音频",
    "/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2023年12月CET6题+解+音频",
    "/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2022年12月CET6题+解+音频"
]

for sd in sample_dirs:
    p = Path(sd)
    print(f"Directory: {p.name}")
    docx_files = list(p.glob("*.docx"))
    for df in docx_files:
        n_p, preview = test_docx(df)
        print(f"  DOCX: {df.name} (Paragraphs: {n_p})")
        for line in preview[:4]:
            print(f"    {line[:100]}")
    pdf_files = list(p.glob("*.pdf"))
    for pf in pdf_files:
        print(f"  PDF: {pf.name} (Size: {round(pf.stat().st_size/1024, 1)} KB)")
    print()
