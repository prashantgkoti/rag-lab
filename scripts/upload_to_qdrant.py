from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
import uuid
from dotenv import load_dotenv
from pypdf import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from src.rag.chunking import chunk_document
from src.rag.embeddings import LocalEmbeddingModel

load_dotenv()

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
COLLECTION_NAME = "securities_lending"
VECTOR_SIZE = 384  # must match LocalEmbeddingModel's output

def load_text(path: Path) -> str:
    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8")
    reader = PdfReader(path)
    return "".join(page.extract_text() or "" for page in reader.pages)


def main() -> None:
    client = QdrantClient(
        url=os.environ["QDRANT_URL"],
        api_key=os.environ["QDRANT_API_KEY"],
        timeout=60,  # give slow cloud writes more room before giving up
    )

    # (Re)create the collection fresh each run, so re-runs don't duplicate data.
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )
    print(f"Collection '{COLLECTION_NAME}' ready.\n")

    pdfs = sorted(RAW_DIR.glob("*.pdf"))
    docs = [pdf.with_suffix(".txt") if pdf.with_suffix(".txt").exists() else pdf for pdf in pdfs]
 
    model = LocalEmbeddingModel()

    all_chunks = []

    for doc in docs:
        print (f"doc : {doc}, doc.stem: {doc.stem}")
        text = load_text(doc)
        chunks = chunk_document(text, source=doc.stem, max_chars=800)
        all_chunks.extend(chunks)
        print(f"  {doc.name:<45} {len(chunks):>3} chunks")

    print(f"\nTotal: {len(all_chunks)} chunks. Embedding...")
    texts = [c.text for c in all_chunks]
    vectors = model.embed(texts)

    print("Uploading to Qdrant...")
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={"text": chunk.text, "source": chunk.source, "chunk_index": chunk.chunk_index},
        )
        for chunk, vector in zip(all_chunks, vectors)
    ]
    batch_size = 50
    for i in range(0, len(points), batch_size):
        batch = points[i : i + batch_size]
        client.upsert(collection_name=COLLECTION_NAME, points=batch)
        print(f"Uploaded {min(i + batch_size, len(points))}/{len(points)}")

    print(f"Done. {len(points)} chunks uploaded to '{COLLECTION_NAME}'.")


if __name__ == "__main__":
    main()