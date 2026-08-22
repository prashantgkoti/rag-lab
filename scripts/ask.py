from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.query_corpus import search
from src.rag.generation import generate_answer


def ask(question: str, top_k: int = 5) -> None:
    print(f"Question: {question}\n")

    hits = search(question, top_k=top_k)
    chunks = [
        {"source": hit.payload["source"], "text": hit.payload["text"]}
        for hit in hits
    ]

    print(f"Retrieved {len(chunks)} chunks. Generating answer...\n")
    answer = generate_answer(question, chunks)

    print("ANSWER:")
    print(answer)

    print("\nSOURCES USED:")
    for i, hit in enumerate(hits, start=1):
        print(f"  [{i}] {hit.payload['source']} (chunk {hit.payload['chunk_index']}, score {hit.score:.4f})")


if __name__ == "__main__":
    question = "What margin is required from the borrower in securities lending?"
    ask(question)