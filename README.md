# 📈 Securities Lending RAG

A Retrieval-Augmented Generation (RAG) system built from scratch — no LangChain, no LlamaIndex — grounded in real securities lending regulatory and industry documents (SEBI, ISLA, FSB). Built as a hands-on learning project in LLMs, RAG, and agentic AI, and as a portfolio piece demonstrating engineering practices applied to GenAI work.

**[Live demo screenshot below](#demo)** · Built by [Prashant](https://github.com/prashantgkoti)

---

## Why this project

Most RAG tutorials retrieve from Wikipedia or arXiv. This one retrieves from real regulatory and industry documents on securities lending — SEBI circulars, ISLA guides, FSB reports — a domain from my own background in capital markets and post-trade operations. The goal was to understand every stage of a RAG pipeline well enough to build it by hand, then ground it in a domain where the answers actually matter.

Every core component — chunking, embedding interface, retrieval, generation — is implemented from first principles rather than imported from a framework, specifically so I understand *why* each piece works, not just *that* it works.

## Demo

A working Streamlit app answers questions grounded in the corpus, with inline citations and expandable source passages for verification.

*Example: "Why is securities lending needed?"*
> Based on the provided sources, securities lending is needed for the following reasons: **Provides Liquidity and Increases Market Efficiency** — it provides essential liquidity to equity, bond, and money markets [2], [4]. **Enables Selling Securities Not Owned** — it allows participants to sell securities they do not own [3], [4]. **Facilitates Financing** — it serves as a method of financing through lending securities against cash [3], [4]...

Every claim is cited to a numbered source; sources are shown below the answer with similarity scores and full text, so the answer can be verified against the original document.

## Architecture

```
Raw PDFs (SEBI, ISLA, FSB)
      │
      ├─► OCR fallback for scanned PDFs (Tesseract + Poppler)
      │
      ▼
Recursive chunking (paragraph → sentence → word, hand-built)
      │
      ▼
Embeddings (sentence-transformers, model-agnostic interface)
      │
      ▼
Qdrant Cloud (vector storage, cosine similarity)
      │
      ▼
Retrieval (top-k semantic search)
      │
      ▼
Generation (Gemini 3.6 Flash, grounded + cited prompt)
      │
      ▼
Streamlit UI
```

## What's implemented

- **Corpus pipeline** — 9 public documents (SEBI, ISLA, FSB); `scripts/inspect_corpus.py` validates every file, detects scanned PDFs with no text layer, and OCRs them automatically into matching `.txt` files.
- **Recursive chunking** (`src/rag/chunking.py`) — hand-built, not a library call. Tries paragraph breaks first, then sentences, then words, falling back to a hard cut only as a last resort — so chunks never split mid-word or mid-sentence unless truly necessary.
- **Model-agnostic embeddings** (`src/rag/embeddings.py`) — a `Protocol`-based interface (`EmbeddingModel`) so the local `sentence-transformers` model and (future) OpenAI embeddings are interchangeable without touching any calling code.
- **Vector storage** — Qdrant Cloud, 384-dim vectors, cosine similarity. Batched upload to handle free-tier network timeouts gracefully.
- **Retrieval** (`scripts/query_corpus.py`) — semantic search via the same embedding model used for indexing, returning ranked chunks with source and similarity score.
- **Generation** (`src/rag/generation.py`) — Gemini 3.6 Flash, prompted to answer *only* from retrieved sources and cite them inline, with prompt construction separated from the API call so the LLM provider can be swapped independently.
- **Streamlit demo app** (`app/streamlit_app.py`) — a working Q&A interface: question box, formatted grounded answer, expandable cited sources.

## Corpus

9 public documents from SEBI, ISLA, and the FSB — see [`data/sources.md`](data/sources.md) for the full list and provenance. PDFs aren't committed to the repo (large, third-party documents); the sources doc lets anyone reconstruct the corpus.

## Setup

```bash
uv venv
.venv\Scripts\activate      # Windows
uv pip install -r requirements.txt
```

OCR requires [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) and [Poppler](https://github.com/oschwartz10612/poppler-windows/releases) on your system PATH. Qdrant Cloud and Gemini API credentials go in a `.env` file (never committed — see `.gitignore`).

```bash
python scripts/inspect_corpus.py     # validate + OCR the corpus
python scripts/embed_corpus.py       # chunk + embed all documents
python scripts/upload_to_qdrant.py   # upload to Qdrant Cloud
streamlit run app/streamlit_app.py   # launch the demo
```

## Status & roadmap

- [x] Corpus collection, validation, OCR pipeline
- [x] Hand-built recursive chunking
- [x] Model-agnostic embedding interface
- [x] Vector storage (Qdrant Cloud)
- [x] Retrieval + generation with citations
- [x] Streamlit demo app
- [ ] Compare chunking strategies and embedding models with real metrics
- [ ] Reranking and hybrid search
- [ ] Evaluation harness — gold Q&A set, retrieval + answer-quality metrics
- [ ] Agentic RAG capstone

## Tech stack

Python · sentence-transformers · Qdrant Cloud · Google Gemini API · Streamlit · Tesseract/Poppler (OCR) · uv
