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

