from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pypdf import PdfReader
from src.rag.chunking import chunk_document

print("sys.path[0]:", sys.path[0])
print("Exists?", (Path(sys.path[0]) / "src").exists())
print("Looking for src at:", Path(__file__).resolve().parent.parent / "src" / "rag")

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

def main() -> None:
    target_pdf_path = RAW_DIR / "AutomatedSL.pdf"
    reader = PdfReader(target_pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    chunks = chunk_document(text, source=target_pdf_path.name, max_chars=800)
    print(f"{target_pdf_path.name}: {len(text)} chars -> {len(chunks)} chunks\n")
    
    for c in chunks[:5]:
        print(f"[chunk {c.chunk_index}] ({len(c.text)} chars)")
        print(f"  {c.text[:150]!r}...\n")

if __name__ == "__main__":
    main()        
