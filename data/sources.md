# Corpus sources — securities lending knowledge base

Public documents making up the RAG knowledge base for this project.
Files live in `data/raw/` (gitignored — not committed, since they're
large and not ours to redistribute). Some are scanned PDFs with no
text layer; `scripts/inspect_corpus.py` detects those automatically
and OCRs them into a matching `.txt` file alongside the original.

All documents are published by regulators or industry bodies and are
publicly available. Used here for a personal, non-commercial learning
project. Attribution remains with the original publisher.

## India — SEBI & exchanges

- **SEBI SL.pdf** — SEBI securities lending framework/circular. *(Scanned — OCR'd to `SEBI_SL.txt`.)*
- **AutomatedSL.pdf** — Automated securities lending mechanics.

## Industry — ISLA

- **ISLA.pdf** (`isla_working_example`) — Worked example of a securities loan, including CREST/DBV collateral settlement.
- **isla_sl_basics.pdf** — ISLA's securities lending fundamentals/basics guide.
- **SLBH.pdf** — Securities Lending & Borrowing Handbook-style reference. *(Scanned — OCR'd to `SLBH.txt`.)*
- **SL Transactions.pdf** — Detailed transaction-level mechanics (125 pages).

## Financing & standing facilities

- **Securities Lending and Corporate Financing.pdf** — SL in the context of corporate financing.
- **...Securities-Lending-and-Related-Standing-Facilities.pdf** — Central-bank-style working paper on SL and standing facilities.

## Broad reference

- **slm_fullpublication.pdf** — Large (62-page) full publication on securities lending markets. *(Scanned — OCR'd to `slm_fullpublication.txt`.)*

---

**To reproduce this corpus:** these were downloaded manually from
regulator/industry sites. See individual filenames above for what
to search for. `scripts/inspect_corpus.py` validates and OCRs
whatever's placed in `data/raw/`, regardless of source.
