# Corpus sources — securities lending knowledge base

These public documents make up the RAG knowledge base for this project.
The PDFs themselves are **not** committed to the repo (see `.gitignore`);
run `python scripts/download_corpus.py` to fetch them into `data/raw/`.

All documents are published by regulators or industry bodies and are
publicly available. They are used here for a personal, non-commercial
learning project. Attribution remains with the original publisher — check
each source's terms before any redistribution or commercial use.

---

## India — SEBI & exchanges

- **sebi_slb_faqs.pdf** — FAQ on the Securities Lending & Borrowing (SLB)
  scheme: tenure, margins, T+1 settlement, tax treatment. *(Cleanest starter
  document — plain Q&A, chunks well.)*
  https://ncfe.org.in/wp-content/uploads/2023/12/FAQs-for-Securities-lending-and-borrowing-SLB-scheme.pdf

- **sebi_slb_scheme.pdf** — The SLB scheme framework: role of the approved
  intermediary, lender, and borrower; title vs. beneficial-interest rules.
  https://www.sebi.gov.in/sebi_data/commondocs/cirsmd15a4_p.pdf

- **sebi_shortselling_slb_discussion.pdf** — Discussion paper on short
  selling and SLB; the market-design rationale.
  https://www.sebi.gov.in/sebi_data/commondocs/rep40_p.pdf

- **bse_slb_framework.pdf** — Broad operational framework for SLB:
  agreements, risk management, settlement.
  https://www.bseindia.com/downloads1/SEBICircular.pdf

## Industry — ISLA

- **isla_working_example.pdf** — Worked example of a securities loan
  including collateral settlement in the UK CREST system (Delivery by Value).
  https://www.esma.europa.eu/sites/default/files/ISLA_1.pdf

- ISLA Securities Lending & Borrowing Hub — *web pages*, useful later for
  the glossary and FAQ (scrape as a separate ingestion source):
  https://www.islaemea.org/sl-hub/

## Global regulator — FSB

- **fsb_market_overview.pdf** — Market overview and financial-stability
  issues in securities lending and repo; participants, margins/haircuts,
  collateral eligibility across jurisdictions.
  https://www.fsb.org/wp-content/uploads/r_120427.pdf

- **fsb_shadow_banking_recommendations.pdf** — Policy recommendations,
  including the haircuts framework for non-centrally-cleared SFTs.
  https://www.fsb.org/uploads/r_130829b.pdf
