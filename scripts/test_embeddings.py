from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.rag.embeddings import LocalEmbeddingModel

texts = [
    "The borrower must post collateral to secure the securities loan.",
    "Margin requirements protect the lender against counterparty risk.",
    "The weather in Mumbai is hot and humid in August.",
]

model = LocalEmbeddingModel()
vectors = model.embed(texts)

print(f"Got {len(vectors)} vectors, each with {len(vectors[0])} dimensions\n")
for text, vec in zip(texts, vectors):
    print(f"'{text[:50]}...'")
    print(f"  first 5 numbers: {vec[:5]}\n")