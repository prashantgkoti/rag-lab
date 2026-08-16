from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
from src.rag.embeddings import LocalEmbeddingModel

texts = [
    "The borrower must post collateral to secure the securities loan.",
    "Margin requirements protect the lender against counterparty risk.",
    "The weather in Mumbai is hot and humid in August.",
    "Borrowing cost raises due to recall failures? "
]

labels = ["Collateral", "Margin/Risk", "Weather", "Recall"]

model = LocalEmbeddingModel()
vectors = model.embed(texts)

def cosine_sim(a: list[float], b: list[float]) -> float:
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


print("Cosine similarity (1.0 = identical meaning, 0 = unrelated, -1 = opposite):\n")
for i in range(len(texts)):
    for j in range(i + 1, len(texts)):
        sim = cosine_sim(vectors[i], vectors[j])
        print(f"  {labels[i]:<16} vs {labels[j]:<16}: {sim:.4f}")