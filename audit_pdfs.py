import os
import subprocess
from pathlib import Path

root = Path("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频")

results = []

for pdf_path in sorted(root.rglob("*.pdf")):
    # Check if it is a 解析 (explanation) or 真题 (exam paper)
    is_analysis = "解析" in pdf_path.name or "详解" in pdf_path.name or "答案" in pdf_path.name
    # Extract text sample using pdftotext
    try:
        proc = subprocess.run(
            ["pdftotext", "-f", "1", "-l", "5", str(pdf_path), "-"],
            capture_output=True,
            text=True,
            timeout=10
        )
        text = proc.stdout.strip()
        has_text = len(text) > 100
        sample = text[:150].replace('\n', ' ') if has_text else ""
    except Exception as e:
        has_text = False
        sample = f"Error: {e}"

    results.append({
        "path": str(pdf_path.relative_to(root)),
        "name": pdf_path.name,
        "is_analysis": is_analysis,
        "has_text": has_text,
        "text_len_p1_5": len(text) if 'text' in locals() else 0,
        "sample": sample
    })

print(f"Total PDFs examined: {len(results)}")
analysis_pdfs = [r for r in results if r["is_analysis"]]
textable_analysis = [r for r in analysis_pdfs if r["has_text"]]
scanned_analysis = [r for r in analysis_pdfs if not r["has_text"]]

print(f"Analysis PDFs total: {len(analysis_pdfs)}")
print(f"  With extractable text: {len(textable_analysis)}")
print(f"  Scanned / No text: {len(scanned_analysis)}")

print("\n--- Sample of Analysis PDFs with extractable text ---")
for r in textable_analysis[:10]:
    print(f"[{r['text_len_p1_5']} chars] {r['path']}")
    print(f"   Sample: {r['sample'][:100]}")

print("\n--- Sample of Analysis PDFs WITHOUT text (scanned) ---")
for r in scanned_analysis[:10]:
    print(f"[{r['text_len_p1_5']} chars] {r['path']}")
