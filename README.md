# MASHeritage: Bilingual Malaysian Heritage Q&A Assistant

MASHeritage is a retrieval-augmented generation (RAG) assistant that answers questions about Malaysian heritage sites in **English and Malay**, using official public documents. Every answer cites its source document and page or section. It is informational only.

## Problem Statement
Information about heritage sites is scattered across UNESCO files, national heritage pages and museum websites, in two languages and different wording. Visitors and students cannot easily find or compare it.

## Users
- Tourists (local and international)
- History and heritage students
- Tour guides and museum staff

## Why AI
- Cross-lingual retrieval (Malay question, English document) that keyword search cannot do
- Synthesis and comparison across several documents
- Easy updates by re-indexing documents

## Data Sources
See [`data/SOURCES.md`](data/SOURCES.md). Minimum 3 public sources: UNESCO World Heritage Centre, Jabatan Warisan Negara / state heritage bodies, and museum or site operator pages.

## Scope
**In scope:** bilingual Q&A with citations, cross-lingual retrieval, metadata filters, comparison of 2-3 sites, "not found" responses, simple UI.
**Out of scope:** itinerary planning or booking, live info (hours, prices), settling disputed history, image recognition, unrelated chat.

## Architecture
```
Docs (EN/MS) -> Ingestion & cleaning -> Language detection -> Chunking + metadata
   -> Multilingual embeddings -> Vector store
Question -> Language detect -> Query rewrite -> Retrieve (+filters) -> (Rerank)
   -> LLM answer with citations -> Guardrails -> UI
```

## Risks and Controls
See [`docs/risk_analysis.md`](docs/risk_analysis.md).

## Evaluation Plan
80-100 Q&A pairs, 50% English and 50% Malay, including cross-lingual and unanswerable questions. Metrics: Recall@5, MRR, correctness, faithfulness, citation accuracy, abstention rate, language consistency, latency. Baselines: BM25 vs multilingual embeddings vs hybrid.

## How to Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python src/ingestion/fetch_sources.py   # downloads pages listed in data/sources.csv
pytest
```

## Roadmap
Weeks 1-2 scoping and data; 3-4 ingestion and BM25; 5-6 first RAG; 7 test set; 8-9 hybrid and rerank; 10 guardrails; 11-12 UI; 13 final evaluation; 14 demo and `v1.0`.

## Disclaimer
MASHeritage reports what its source documents state and may be incomplete or outdated. Verify important details with the official source. It is not an official heritage authority service.
