from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Chunk:
    """
    A chunk of text with associated metadata.

    Attributes:
        text (str): The text content of the chunk.
        source (str): A string containing the source of the chunk.
        chunk_index (int): The index of the chunk within the source.
    """

    text: str
    source: str
    chunk_index: int


DEFAULT_SEPARATORS = ["\n\n", "\n", ". ", " "]


def _split_text(text: str, max_chars: int, separators: list[str]) -> list[str]:
    """
    Recursively split the input text on the first separator such that each piece is under the max_chars limit.
    """
    if len(text) <= max_chars:
        return [text]

    if not separators:
        # No separators left -- hard cut as a last resort.
        return [text[:max_chars], *_split_text(text[max_chars:], max_chars, separators)]

    sep, remaining_seps = separators[0], separators[1:]
    pieces = text.split(sep)

    chunks: list[str] = []
    buffer = ""
    for piece in pieces:
        candidate = buffer + sep + piece if buffer else piece
        if len(candidate) <= max_chars:
            buffer = candidate
        else:
            if buffer:
                chunks.append(buffer)
            if len(piece) > max_chars:
                chunks.extend(_split_text(piece, max_chars, remaining_seps))
                buffer = ""
            else:
                buffer = piece
    if buffer:
        chunks.append(buffer)
    return chunks


def chunk_document(
    text: str,
    source: str,
    max_chars: int = 800,
    separators: list[str] | None = None,
) -> list[Chunk]:
    """
    Split the input text into Chunk objects, tagged with source and position.
    """
    seps = separators if separators is not None else DEFAULT_SEPARATORS
    raw_chunks = _split_text(text, max_chars, seps)
    return [Chunk(text=raw, source=source, chunk_index=i) for i, raw in enumerate(raw_chunks)]