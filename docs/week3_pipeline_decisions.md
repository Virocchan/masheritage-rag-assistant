# Pipeline Architecture Decisions & Traceability — MASHeritage (Week 3)

## 1. Requirements Traceability

This V1 Data Engineering pipeline directly implements the data foundation designed in Topic 2:

| Requirement ID | Requirement Summary | Pipeline Response & Implementation |
|---|---|---|
| **FR1** | Bilingual Heritage Q&A | Ingests official documentation for all 6 Malaysian World Heritage properties in English, supplemented with Jabatan Warisan Negara (JWN) Malay documentation. |
| **FR2** | Cross-Lingual Retrieval | Preserves authentic Malay cultural terminology without machine translation; chunks both languages into a shared schema with language tags (`EN`, `MS`). |
| **FR3 & RAI3** | Grounding & Verifiable Citations | Every prepared chunk in `prepared_text.jsonl` contains `record_id`, `source_id`, `source_url`, `publisher`, `site`, `language`, and `source_sha256`. |
| **FR5** | Cultural & Heritage Terminology | Ingests National Heritage Act 2005 (Akta 645) policy pages containing legal definitions of cultural, natural, and archaeological heritage. |
| **NFR4** | Maintainability & Update Speed | Automated batch pipeline executes in < 30 seconds (< 15-minute threshold) to ingest, clean, chunk, validate, and hash updated sources. |
| **RAI1** | Fairness & Language Parity | Tracks language metadata per chunk to enable stratified cross-lingual evaluation in Topic 4 without masking corpus volume differences. |

---

## 2. Selected Sources and Justification

- **UNESCO World Heritage Centre (whc.unesco.org):** 7 authoritative English documents covering Malaysia's World Heritage profile and all 6 inscribed properties (Melaka & George Town, Kinabalu Park, Gunung Mulu, Lenggong Valley, Niah Caves Complex, FRIM Forest Park Selangor). Provides definitive Statements of Outstanding Universal Value (OUV) and legal criteria.
- **Jabatan Warisan Negara (heritage.gov.my):** 4 bilingual (Malay/English) documents providing official national heritage classifications, gazette status, and statutory definitions under Akta 645.
- **MOTAC Cultural Statistics Report:** Identified as supplementary PDF documentation for statistical inquiries.

---

## 3. Part B Transformation Comparison & Evidence

In Part B, two document chunking strategies were evaluated on `UNESCO_1223.txt` (Melaka and George Town, 8,844 characters):

| Metric / Dimension | Strategy 1: Fixed-Character Chunking | Strategy 2: Paragraph-Aware Chunking (Selected) |
|---|---|---|
| **Window Size** | 500 characters strict | Max 500 characters, paragraph-aligned |
| **Total Chunks Produced** | 18 chunks | 24 chunks |
| **Boundary Integrity** | Chunks severed arbitrarily in the middle of sentences and proper nouns (e.g., cutting off historical dates and Malay site names). | Chunks respect natural paragraph breaks and section headings (`Outstanding Universal Value`, `Criterion (ii)`). |
| **Sub-splitting Behavior** | Linear sliding window | Paragraphs < 500 chars remain atomic; paragraphs > 500 chars are sub-chunked cleanly. |
| **Semantic Coherence** | Low (fragmented context causes hallucination or incomplete answers in RAG). | High (each chunk contains a coherent thematic statement or historical argument). |

### Comparison Sample:
- **Fixed Chunk 0:**  
  `Melaka and George Town, historic cities of the Straits of Malacca have developed over 500 years of trading and cultural exchanges between East and West in the Straits of Malacca. The influences of Asia and Europe have endowed the towns with a specific multicul...` *(Truncates mid-sentence)*
- **Paragraph-Aware Chunk 0:**  
  `Melaka and George Town, historic cities of the Straits of Malacca have developed over 500 years of trading and cultural exchanges between East and West in the Straits of Malacca.` *(Clean, self-contained concept)*

### Chosen Configuration:
- **Method:** `paragraph-aware-char-500` (Max chunk size: 500 characters, respecting `\n\n` boundaries).
- **Accepted Limitations:** Character-length splitting approximates but does not strictly match token counts for embedding models. True semantic chunking or recursive token chunking (e.g., with TikToken / HuggingFace tokenizer) will be evaluated in Topic 5.

---

## 4. Architectural & System Design Decisions

### 4.1 ETL vs. ELT Architecture
- **Decision:** **ETL (Extract, Transform, Load)** was selected over ELT.
- **Rationale:** For a domain-specific heritage RAG application with strict citation requirements (FR3/RAI3), raw web scrape noise (scripts, styling, boilerplate, ads) must be removed and partitioned into validated, deduplicated JSONL chunks *prior* to indexing. Storing uncleaned text directly in vector stores (ELT) wastes embedding API costs, degrades retrieval precision, and leaks web artifacts into user responses.

### 4.2 Batch vs. Streaming Rationale
- **Decision:** **Batch Processing** was selected.
- **Rationale:** Malaysian heritage declarations, UNESCO inscriptions, and national gazette updates occur on monthly, annual, or decennial cycles (e.g., FRIM inscribed July 2025; Niah Caves inscribed July 2024). There is no high-velocity real-time data stream. A deterministic batch pipeline running periodically (or on source release) ensures reproducibility, lower operational cost, and full cryptographic validation.

### 4.3 Storage and Lineage Schema
- **Raw Layer:** `data/raw/sources/` (Contains immutable source text dumps with SHA-256 fingerprints in `data/raw/source_manifest.json`).
- **Processed Layer:** `data/processed/prepared_text.jsonl` (Part B intermediate processed dataset).
- **V1 Pipeline Layer:** `data/pipeline_v1/documents/` containing:
  - `prepared_text.jsonl`: 215 structured JSON records with full provenance metadata.
  - `pipeline_manifest.json`: Execution run metadata, configuration parameters, and input-to-output SHA-256 mappings.

---

## 5. Stage Contracts & Failure Handling Table

| Stage | Contract / Evidence Required | Failure Response & Recovery Mechanism |
|---|---|---|
| **Ingest** | Target official URLs respond with HTTP 200; valid TLS certificates; sources listed in `sources.csv`. | **Network Timeout / SSL Mismatch:** Retry with exponential backoff; enforce canonical host domains (`www.heritage.gov.my`); log failures to `source_manifest.json`; **fail-stop** if successful sources < 2. |
| **Inspect** | Raw source files exist, are valid UTF-8, and exceed minimum length threshold (> 250 characters). | **Empty / Corrupted Body:** Raise `ValueError`; skip blank/JS-only documents; report defect in inspection logs rather than poisoning pipeline. |
| **Prepare** | Whitespace normalized; paragraph-aware chunker produces non-empty string chunks ≤ 500 chars. | **Transformation Failure:** Halt processing for that record; log unparseable encoding; ensure no partial or malformed chunks reach the output. |
| **Validate** | `prepared_text.jsonl` exists, size > 0 bytes; every record contains required non-empty keys (`record_id`, `text`, `source_url`, `source_sha256`); zero duplicate IDs. | **Missing / Incomplete Fields:** Trigger assertion failure (`AssertionError`); refuse to generate pipeline manifest until schema validation passes 100%. |
| **Record Lineage** | Output JSONL and manifest reference exact source files with bit-for-bit verifiable SHA-256 checksums. | **Lineage Mismatch:** Invalidate build; log provenance error; abort pipeline. |

---

## 6. Repeatability & Provenance Verification (Part C Verification)

Repeatability was validated by executing the integrated pipeline twice under identical inputs and configurations.
- **Source Fingerprint Invariance:** SHA-256 digests of all 11 source documents remained bit-identical across runs.
- **Output Fingerprint Invariance:** SHA-256 digest of `data/pipeline_v1/documents/prepared_text.jsonl` remained identical (`b480c5d5e2...`).
- **Mapping Verification:** Source-to-output mapping verified 100% stable.
- **Result:** **PASS — Repeatability smoke checks passed successfully.**
