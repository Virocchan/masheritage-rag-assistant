# Weekly Log

## Week 1-2
- Chose project: MASHeritage
- Created repo structure and scope documents
- Outlined functional/non-functional requirements (FR1-FR5, NFR1-NFR4, RAI1-RAI3) and V1 architecture decisions.

## Week 3 (Data Engineering for AI)
- Ingested 11 official public documents (UNESCO World Heritage Centre & Jabatan Warisan Negara) covering all 6 inscribed Malaysian World Heritage properties in English, supplemented with Malay statutory and register documentation.
- Created `src/ingestion/fetch_sources.py` with polite delay, DOM cleanup, and cryptographic SHA-256 fingerprinting stored in `data/raw/source_manifest.json`.
- Completed inspection of representative English (`UNESCO_1223.txt`) and Malay (`JWN_REGISTER_MS.txt`) artefacts in `docs/week3_data_inventory.md`.
- Evaluated fixed vs. paragraph-aware chunking on `UNESCO_1223.txt`; justified selection of paragraph-aware chunking (max 500 characters) to preserve semantic boundaries.
- Built and validated `data/processed/prepared_text.jsonl` (215 chunks) and recorded Part B lineage manifest `data/week3_manifest.json`.
- Built modular V1 pipeline utilities and implemented Pathway A document pipeline in `notebooks/week3_pipeline.ipynb` and `data/pipeline_v1/documents/`.
- Executed repeatability verification (Cell 9) asserting bit-identical fingerprints and mapping invariance across independent runs.
- Documented pipeline diagram (`docs/week3_pipeline_diagram.png`) with failure modes, and recorded architectural choices and stage contracts in `docs/week3_pipeline_decisions.md`.

## Week 4 (Data Quality and Responsible Data Practices)
- Loaded and cryptographically verified the Topic 3 prepared-data hand-off (`data/prepared_chunks.jsonl` and `data/chunks.pkl`, 215 chunks).
- Built chunk-quality inventory in `notebooks/week4_quality.ipynb` profiling missingness, character counts, whitespace noise, and web boilerplate.
- Enforced repeatable data contracts using **Pandera** (`pa.DataFrameSchema`), logging findings to `docs/week4_validation_failures.csv`.
- Executed exact SHA-256 hash deduplication, identifying 26 redundant boilerplate chunks (12.1%) and preserving provenance in `docs/week4_duplicate_review.csv`.
- Produced clean Topic 4 corpora: `data/prepared_chunks_clean.jsonl` and `data/chunks_clean.pkl` (189 unique chunks).
- Conducted representation and coverage analysis across sources, sites, and languages; generated `docs/week4_coverage_by_source.png`.
- Analyzed empirical Historical, Representation (98.4% EN vs 1.6% MS), and Measurement bias risks, tracing their propagation through RAG vector retrieval and generation.
- Formulated full audit report `docs/week4_data_quality_report.md` with explicit **GO WITH CONDITIONS** Quality Gate Decision.
