from __future__ import annotations

from typing import Protocol

from sentence_transformers import SentenceTransformer

class EmbeddingModel(Protocol):
    """Anything that can turn a list of texts into a list of embedding vectors."""

    def embed(self, texts: list[str]) -> list[list[float]]:
        ...


class LocalEmbeddingModel:
    """Embeds text locally using a sentence-transformers model. Free, no API key, runs on CPU."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self._model = SentenceTransformer(model_name)

    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors = self._model.encode(texts)
        return vectors.tolist()