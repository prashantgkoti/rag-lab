from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

from src.rag.embeddings import LocalEmbeddingModel

COLLECTION_NAME = "securities_lending"

load_dotenv()

def search(query: str, top_k:int = 5):
    client = QdrantClient(
        url = os.environ["QDRANT_URL"],
        api_key = os.environ["QDRANT_API_KEY"]
    )

    model = LocalEmbeddingModel()

    query_vector = model.embed([query])[0]

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
    )
    return results.points

def main() -> None:
    query = "What margin is required from the borrower in securities lending?"
    print(f"Query: {query}\n")

    hits = search(query) 

    for i, hit in enumerate(hits, start=1):
        print(f"[{i}] score={hit.score:.4f}  source={hit.payload['source']}  chunk={hit.payload['chunk_index']}")
        print(f"    {hit.payload['text'][:200]}...\n")


if __name__ == "__main__":
    main()