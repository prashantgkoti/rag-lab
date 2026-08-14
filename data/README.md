# rag-lab

A from-scratch build of a Retrieval-Augmented Generation (RAG) system,
grounded in a securities lending / capital markets knowledge base.

Built as a hands-on learning project to develop practical depth in
LLMs, RAG, and (later) agentic AI — and as a portfolio piece
demonstrating engineering practices applied to GenAI work.

## Why securities lending?

Most RAG tutorials use generic corpora (Wikipedia, arXiv). This one
uses real regulatory and industry documents — SEBI, ISLA, FSB — on
securities lending, a domain from my own background in capital
markets / post-trade operations. The goal: show RAG applied to a
real, technically demanding domain, not just a toy dataset.

## Status

🚧 Early stage — building in public, module by module.

- [x] Project scaffolding, Git/GitHub workflow
- [x] Corpus collection — 9 public documents (SEBI, ISLA, FSB, and
      related sources) — see `data/sources.md`
- [x] Corpus validation & OCR pipeline (`scripts/inspect_corpus.py`) —
      detects scanned PDFs with no text layer and OCRs them automatically
- [ ] Chunking strategies
- [ ] Embedding & vector storage (Qdrant)
- [ ] Retrieval (dense / hybrid / reranking)
- [ ] Generation with citations
- [ ] Evaluation harness (retrieval + answer quality metrics)
- [ ] Agentic RAG capstone

## Repo structure

```
rag-lab/
├── data/
│   ├── raw/            # source PDFs (gitignored — see data/sources.md)
│   └── sources.md      # where every document came from
├── scripts/
│   └── inspect_corpus.py   # validates corpus, OCRs scanned PDFs
├── requirements.txt
└── .gitignore
```

## Setup

```bash
uv venv
.venv\Scripts\activate      # Windows
uv pip install -r requirements.txt
```

OCR requires two external tools on your system PATH: [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
and [Poppler](https://github.com/oschwartz10612/poppler-windows/releases).

## Corpus

See [`data/sources.md`](data/sources.md) for the full list of documents
and where they came from. PDFs aren't committed to the repo (they're
large, third-party documents) — the sources doc lets anyone
reconstruct the corpus themselves.

## Running it

```bash
python scripts/inspect_corpus.py
```

Scans `data/raw/`, reports page/character counts per document, flags
any PDF with no extractable text, and OCRs those automatically into
a matching `.txt` file.
