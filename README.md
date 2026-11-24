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

## Topic 4 Data Quality & Responsible Data Deliverables (Week 4)

In Week 4, the prepared corpus underwent comprehensive quality profiling, Pandera schema validation, exact deduplication, coverage and bias risk tracing, and governance review:

| Deliverable Artefact | Location in Repository | Description & Role |
|---|---|---|
| **Quality Notebook** | [`notebooks/week4_quality.ipynb`](notebooks/week4_quality.ipynb) | End-to-end executable notebook: hand-off verification, chunk profiling, Pandera schema rules, SHA-256 deduplication, and coverage analysis. |
| **Data Quality & Bias Report** | [`docs/week4_data_quality_report.md`](docs/week4_data_quality_report.md) | Formal 8-section audit report with Quality Scorecard, triage findings, bias propagation models, and **GO WITH CONDITIONS** gate decision. |
| **Reviewed Cleaned Corpus (JSONL)** | [`data/prepared_chunks_clean.jsonl`](data/prepared_chunks_clean.jsonl) | Auditable cleaned corpus (189 unique chunks) after removing 26 exact duplicate boilerplate chunks. **Feeds into Topic 7 Vectorstore.** |
| **Reviewed Cleaned Corpus (PKL)** | [`data/chunks_clean.pkl`](data/chunks_clean.pkl) | Notebook-compatible cleaned corpus (189 Document objects) retained for downstream course code. |
| **Validation Failures Log** | [`docs/week4_validation_failures.csv`](docs/week4_validation_failures.csv) | Machine-readable log of Pandera validation rule evaluations and triage decisions. |
| **Duplicate Review Audit** | [`docs/week4_duplicate_review.csv`](docs/week4_duplicate_review.csv) | Audit trail of all 26 detected duplicates, source provenance, and removal actions. |
| **Coverage Visualisation** | [`docs/week4_coverage_by_source.png`](docs/week4_coverage_by_source.png) | High-resolution distribution chart of prepared chunks across all 11 official source documents. |

## How to Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python src/ingestion/fetch_sources.py   # downloads pages listed in data/sources.csv
pytest                                  # runs smoke tests verifying Week 1-4 deliverables
```

## Roadmap
Weeks 1-2 scoping and data; 3-4 ingestion, pipeline & data quality; 5-6 model selection & prompt design; 7 vectorstore & first RAG; 8-9 hybrid retrieval & reranking; 10 guardrails; 11-12 UI; 13 final evaluation; 14 demo and `v1.0`.

## Disclaimer
MASHeritage reports what its source documents state and may be incomplete or outdated. Verify important details with the official source. It is not an official heritage authority service.
