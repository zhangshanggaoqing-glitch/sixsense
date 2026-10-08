import subprocess
import docx
from pathlib import Path

root = Path("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频")

print("Checking docx files for any listening transcripts...")
found_docx_transcripts = []
for doc_path in root.rglob("*.docx"):
    try:
        d = docx.Document(doc_path)
        full_text = "\n".join([p.text for p in d.paragraphs if p.text.strip()])
        # Check if conversation text or transcript exists
        if "Conversation One" in full_text or "Conversation 1" in full_text or "听力原文" in full_text:
            found_docx_transcripts.append((doc_path, len(full_text)))
    except Exception:
        pass

print(f"Found {len(found_docx_transcripts)} docx files containing Conversation/听力原文:")
for p, l in found_docx_transcripts:
    print(f"  {p.relative_to(root)} ({l} chars)")

print("\nChecking all PDFs for clean listening transcripts...")
pdf_scores = []
for p in root.rglob("*.pdf"):
    if "真题" in p.name and "解析" not in p.name and "详解" not in p.name:
        continue # skip question papers first
    try:
        res = subprocess.run(["pdftotext", str(p), "-"], capture_output=True, text=True, timeout=5)
        txt = res.stdout
        if "Conversation One" in txt or "Conversation 1" in txt or "听力原文" in txt or "Section A" in txt:
            # Measure word separation quality: count how many intact words exist
            # vs single spaced letters like "t o d a y"
            pos = max(txt.find("Conversation One"), txt.find("Conversation 1"), txt.find("Section A"))
            snippet = txt[pos:pos+300] if pos != -1 else ""
            pdf_scores.append((p.relative_to(root), len(txt), snippet))
    except Exception:
        pass

print(f"Found {len(pdf_scores)} PDFs with listening keywords:")
for path, length, snippet in pdf_scores[:15]:
    print(f"\n--- {path} (len: {length}) ---")
    print(snippet.replace('\n', ' ')[:180])
