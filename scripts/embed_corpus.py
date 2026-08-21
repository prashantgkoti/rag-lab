from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pypdf import PdfReader
from src.rag.chunking import chunk_document
from src.rag.embeddings import LocalEmbeddingModel

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

def load_text(path: Path) -> str:
    """Read a document's text: native PDF extraction, or its OCR'd .txt sibling."""
    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8")
    reader = PdfReader(path)
    return "".join(page.extract_text() or "" for page in reader.pages)

def main() -> None:
    # Only process each document once: prefer the .txt (OCR'd) version if it
    # exists, otherwise use the PDF directly. Skip PDFs that have a .txt sibling.
    pdfs = sorted(RAW_DIR.glob("*.pdf"))
    docs = []
    for pdf in pdfs:
        txt_sibling = pdf.with_suffix(".txt")
        docs.append(txt_sibling if txt_sibling.exists() else pdf)

    print(f"Found {len(docs)} documents to process\n")

    model = LocalEmbeddingModel()
    all_chunks = []
    for doc in docs:
        text = load_text(doc)
        chunks = chunk_document(text, source=doc.stem, max_chars=800)
        all_chunks.extend(chunks)
        print(f"  {doc.name:<45} {len(text):>7} chars -> {len(chunks):>3} chunks")

    print(f"\nTotal: {len(all_chunks)} chunks across {len(docs)} documents")

    print("\nEmbedding all chunks (this may take a minute)...")
    texts = [c.text for c in all_chunks]
    vectors = model.embed(texts)
    print(f"Done — {len(vectors)} vectors, {len(vectors[0])} dimensions each")


if __name__ == "__main__":
    main()