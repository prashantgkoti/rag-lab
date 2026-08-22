from __future__ import annotations

import os 
from google import genai

def build_prompt(question: str, chunks: list[dict]) -> str:
    """Assemble a grounded prompt: the question, plus numbered source passages."""
    context_blocks = []
    for i, chunk in enumerate(chunks, start=1):
        context_blocks.append(f"[{i}] (source: {chunk['source']})\n{chunk['text']}")
    context = "\n\n".join(context_blocks)

    return f"""Answer the question using ONLY the numbered sources below. \
If the sources don't contain enough information, say so — do not use outside knowledge.
Cite sources inline using their number, like [1].

SOURCES:
{context}

QUESTION: {question}

ANSWER:"""


def generate_answer(question: str, chunks: list[dict]) -> str:
    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )
    prompt = build_prompt(question, chunks)

    response = client.models.generate_content(
        model = "gemini-3.6-flash",
        contents = prompt,
    )
    return response.text