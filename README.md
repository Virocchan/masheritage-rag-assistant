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

## Topic 3 Data Engineering Deliverables (Week 3)

In Week 3, the project transitioned from specifications to an executable, reproducible V1 Data Pipeline for **Pathway A (Document / Text)**:

| Deliverable Artefact | Location in Repository | Description & Role |
|---|---|---|
| **Runnable Notebook** | [`notebooks/week3_pipeline.ipynb`](notebooks/week3_pipeline.ipynb) | Google Colab executable pipeline: ingestion, inspection, chunking comparison, validation, and repeatability smoke tests. |
| **Data Inventory** | [`docs/week3_data_inventory.md`](docs/week3_data_inventory.md) | Comprehensive audit of 11 official sources, licenses, character counts, raw/prepared storage separation, and inspection evidence. |
| **Pipeline Diagram** | [`docs/week3_pipeline_diagram.png`](docs/week3_pipeline_diagram.png) | Visual workflow showing Ingest → Inspect → Prepare → Validate → Lineage with 2 annotated failure points and responses ([Source .mmd](docs/week3_pipeline_diagram.mmd)). |
| **Pipeline Decisions** | [`docs/week3_pipeline_decisions.md`](docs/week3_pipeline_decisions.md) | Engineering decisions (ETL vs ELT, batch rationale), chunking comparisons, stage contracts, and trade-offs. |
| **Part B Lineage Manifest** | [`data/week3_manifest.json`](data/week3_manifest.json) | Lineage manifest recording source-to-output SHA-256 transformations and chunk parameters. |
| **Part C Pipeline Artefacts** | [`data/pipeline_v1/documents/`](data/pipeline_v1/documents/) | Executable pipeline outputs (`prepared_text.jsonl` containing 215 chunks with citations, and `pipeline_manifest.json`). |

### How to Run the Week 3 Pipeline
1. **Google Colab:** Open `notebooks/week3_pipeline.ipynb` in Colab and execute cells top-to-bottom (zero cost, no API key required).
2. **Local Terminal:**
```bash
# 1. Fetch official source documents with SHA-256 validation
python src/ingestion/fetch_sources.py

# 2. Inspect outputs
cat data/raw/source_manifest.json
cat data/pipeline_v1/documents/pipeline_manifest.json
```

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
