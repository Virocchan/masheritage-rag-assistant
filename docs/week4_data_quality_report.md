# Data Quality, Bias, and Responsible Data Report — MASHeritage

**Project:** MASHeritage — Bilingual (English / Bahasa Malaysia) Malaysian World Heritage Assistant  
**Domain:** Unstructured Heritage Corpus (UNESCO World Heritage Inscriptions & Jabatan Warisan Negara Statutory Documents)  
**Lifecycle Stage:** Phase 1 (Data Engineering & Governance) — Topic 4 Quality Gate  
**Date:** November 2026  
**Author:** MASHeritage AI Engineering Team  

---

## 1. Data Quality Scorecard

The MASHeritage corpus consists of 215 prepared text chunks derived from 11 official public documents covering Malaysia's inscribed UNESCO World Heritage properties, national statutory heritage legislation, and heritage register portals. Quality was assessed against the five operational data-quality dimensions:

| Dimension | Rating (1–5 / N.V.) | Evidence | Action / Limitation |
|---|:---:|---|---|
| **Completeness** | **4 / 5** | All 11 targeted official sources were ingested. Zero chunks contain empty text (`missing_text = 0`). 100% of chunks retain valid source paths, publisher provenance, and HTTPS citation URLs. | **Limitation:** Isolated single-line headings (e.g. *"Integrity"*, 9 chars) and web navigation footers lack complete semantic context. Handled via threshold warnings and boilerplate triage. |
| **Consistency** | **5 / 5** | Unified JSONL and PKL schema across all chunks. Language tags (`EN`, `MS`), site names, and deterministic chunk IDs (`<source_id>-<index:04d>`) follow uniform formatting. | **Controlled:** 100% schema compliance verified by automated Pandera data contracts. |
| **Accuracy** | **5 / 5** | Sources directly originate from authoritative institutional publishers (UNESCO World Heritage Centre and Jabatan Warisan Negara). Factual criteria (e.g. Melaka Criteria ii, iii, iv) match official gazetted records. | **Controlled:** Exact URL attribution and SHA-256 source hashing guarantee verifiable ground truth. |
| **Timeliness** | **4 / 5** | Inscription documentation includes the newest 2024 inscription (*Niah National Park Caves Complex*) and the 2025 inscription (*FRIM Forest Park Selangor*). Statutory data reflects the current National Heritage Act 2005 (Act 645). | **Limitation:** Inscription narratives for older sites (e.g. *Kinabalu Park* and *Gunung Mulu*, inscribed 2000) reflect conditions at the time of nomination and lack recent 2024–2026 periodic conservation reports. |
| **Uniqueness** | **4 / 5** | 26 exact duplicate chunks (12.1% of raw corpus) detected and resolved via SHA-256 hash deduplication, reducing the corpus from 215 to 189 distinct chunks. | **Controlled:** Provenance preserved in `week4_duplicate_review.csv`. Exact duplicates consisted of repeated UNESCO license notices and identical executive summary paragraphs. |

---

## 2. Validation and Data-Defect Findings

Data contracts were declared and enforced using **Pandera** (`pa.DataFrameSchema`), evaluating structural integrity, completeness, and domain constraints:

### Rule Summary and Execution Results
1. **Text Completeness (`text.str.strip().str.len() > 0`):**
   - *Quality Concern:* Empty chunks provide zero information and degrade RAG embeddings.
   - *Result:* **0 failures (100% pass)**. All 215 chunks contain non-empty text.
2. **Provenance Metadata Completeness (`source.str.strip().str.len() > 0`):**
   - *Quality Concern:* Untraceable text chunks violate Responsible AI attribution (RAI1, RAI3) and risk hallucinated responses.
   - *Result:* **0 failures (100% pass)**. All chunks retain traceable source paths and canonical URLs.
3. **Minimum Semantic Length Threshold (`char_count >= 40`):**
   - *Quality Concern:* Fragments under 40 characters typically represent isolated structural headings or layout artifacts that lack sufficient semantic context for vector search.
   - *Result:* **2 failures flagged**:
     - Chunk 30 (`UNESCO_1012`): 9 characters (*"Integrity"*).
     - Chunk 82 (`UNESCO_1013`): 38 characters (*"Protection and management requirements"*).
   - *Triage Decision:* **Retain with Warning**. These are valid UNESCO criterion headings. Removing them risks losing section demarcation; in Phase 2, they will be merged with their subsequent descriptive paragraph.
4. **Encoding & Byte Corruption Check (`has_bad_char == False`):**
   - *Quality Concern:* Garbled text, null bytes (`\x00`), or unicode replacement characters (`\ufffd`) indicate PDF extraction or encoding pipeline failures.
   - *Result:* **0 failures (100% pass)**. Clean UTF-8 across all 11 documents.
5. **Domain Language & URL Validation:**
   - *Quality Concern:* Invalid language tags or insecure URLs break bilingual routing and web citation.
   - *Result:* **0 failures (100% pass)**. All language tags are officially `EN` or `MS`; all URLs start with `https://`.

All validation results have been logged to [`docs/week4_validation_failures.csv`](file:///Users/virocchan/MASHeritage/masheritage-rag-assistant/docs/week4_validation_failures.csv).

---

## 3. Duplicate and Anomaly Findings

### Exact Deduplication Audit
Using normalized SHA-256 fingerprinting (`re.sub(r'\s+', ' ', text.strip())`), exact duplicates were identified and triaged:
- **Corpus Size Before Deduplication:** 215 chunks
- **Exact Duplicates Detected:** 26 chunks (12.1%)
- **Cleaned Corpus Retained:** 189 unique chunks

### Root Cause Analysis of Duplicates
1. **Repeated UNESCO Licensing Notices (16 instances):**
   - Snippet: *"Description is available under license CC-BY-SA IGO 3.0"*
   - Occurrence: Appears in the footer of every UNESCO inscription webpage (`UNESCO_1012`, `1013`, `1014`, `1223`, `1396`, `1734`).
   - Action: Deduplicated to a single reference instance; source occurrences preserved in audit trail.
2. **Shared Section Subheadings (6 instances):**
   - Snippet: *"Integrity"*, *"Protection and management requirements"*.
   - Occurrence: Standard statutory UNESCO OUV template used across multiple natural and cultural properties.
   - Action: Retained unique representative instances with source mapping.
3. **Document-Internal Executive Summary Repetition (4 instances):**
   - Snippet: Introductory paragraph of `UNESCO_1013` (Gunung Mulu) repeated verbatim in the brief description and long narrative.
   - Action: Deduplicated; primary reference retained.

The complete audit trail is preserved in [`docs/week4_duplicate_review.csv`](file:///Users/virocchan/MASHeritage/masheritage-rag-assistant/docs/week4_duplicate_review.csv). Cleaned outputs are stored in `data/prepared_chunks_clean.jsonl` and `data/chunks_clean.pkl`.

---

## 4. Representation, Coverage, and Bias Assessment

### Coverage by Source and Heritage Site
The cleaned corpus of 189 chunks covers all 6 inscribed Malaysian World Heritage properties:

| Heritage Property | State / Location | Type | Inscribed Year | Chunks | Percent |
|---|---|---|:---:|---:|---:|
| **Gunung Mulu National Park** | Sarawak | Natural | 2000 | 43 | 22.8% |
| **Kinabalu Park** | Sabah | Natural | 2000 | 33 | 17.5% |
| **FRIM Forest Park Selangor** | Selangor | Cultural | 2025 | 31 | 16.4% |
| **Archaeological Heritage of Lenggong Valley** | Perak | Cultural | 2012 | 26 | 13.8% |
| **Niah National Park Caves Complex** | Sarawak | Mixed/Cultural | 2024 | 24 | 12.7% |
| **Melaka and George Town, Historic Cities** | Melaka & Penang | Cultural | 2008 | 22 | 11.6% |
| **National Overview & Statutory Registers** | Malaysia (Federal) | General | Current | 10 | 5.3% |
| **Total Cleaned Corpus** | — | — | — | **189** | **100.0%** |

```
Chunk Coverage Visualization:
Gunung Mulu        [████████████████████████] 43 chunks (22.8%)
Kinabalu Park      [██████████████████] 33 chunks (17.5%)
FRIM Forest Park   [█████████████████] 31 chunks (16.4%)
Lenggong Valley    [██████████████] 26 chunks (13.8%)
Niah Caves Complex [█████████████] 24 chunks (12.7%)
Melaka & George Town [████████████] 22 chunks (11.6%)
National/Statutory [█████] 10 chunks (5.3%)
```
*(High-resolution chart saved to [`docs/week4_coverage_by_source.png`](file:///Users/virocchan/MASHeritage/masheritage-rag-assistant/docs/week4_coverage_by_source.png))*

### Empirical Bias Risks & Propagation Pathway Analysis

```
Propagation Pathway Model:
Source / Pipeline Decision ──► Prepared Corpus ──► Vector Retrieval (Topic 7) ──► User-Facing Generation (Topic 8)
```

#### Risk 1: Representation Bias (Severe Language Imbalance)
- **Empirical Evidence:** The prepared corpus is **98.4% English** (186 chunks) and only **1.6% Bahasa Malaysia** (3 chunks: `JWN_REGISTER_MS`, `JWN_ACT_MS`).
- **Origin:** UNESCO World Heritage Centre publishes comprehensive technical monographs primarily in English and French. The Malaysian Department of National Heritage (JWN) web portal provides concise summaries and form downloads in Malay rather than complete digitized text.
- **Propagation Path:**
  1. *Prepared Corpus:* 186 English chunks vs. 3 Malay chunks.
  2. *Vector Retrieval:* Queries posed in Bahasa Malaysia (*"Apakah kriteria UNESCO untuk Taman Negara Kinabalu?"*) will encounter low semantic similarity against English embeddings if monolingual embeddings are used.
  3. *User Generation:* The LLM may hallucinate answers, refuse to answer in Malay, or generate English responses, violating requirement **FR5**.
- **Intervention:** Mandate cross-lingual bilingual dense retrieval (e.g. `multilingual-e5-base` or `BAAI/bge-m3`) and ingest the full legislative text of Akta Warisan Kebangsaan 2005 (Act 645) in Bahasa Malaysia.

#### Risk 2: Historical & Temporal Bias (Nomination Snapshot Disparity)
- **Empirical Evidence:** Inscription documentation dates span 25 years: *Kinabalu Park* and *Gunung Mulu* (inscribed 2000) vs. *Niah Caves* (2024) and *FRIM Forest Park* (2025).
- **Origin:** UNESCO inscription dossiers capture the property's state of conservation at the time of World Heritage Committee inscription.
- **Propagation Path:**
  1. *Prepared Corpus:* Inscription text for Kinabalu Park does not reflect post-2015 earthquake park management updates or modern Sabah Parks boundary zoning.
  2. *Vector Retrieval:* RAG retrieves 2000 nomination data as contemporary fact.
  3. *User Generation:* System answers contemporary management queries using historical 2000 baseline data without temporal caveats.
- **Intervention:** Inject inscription year metadata (`inscription_year: 2000`) into chunk context and enforce temporal grounding in the RAG system prompt.

#### Risk 3: Measurement Bias (DOM Extraction Proxy Asymmetry)
- **Empirical Evidence:** Natural sites (*Gunung Mulu*, 43 chunks) have approximately double the chunk volume of cultural urban sites (*Melaka and George Town*, 22 chunks), despite both having equal World Heritage status.
- **Origin:** Ecological and geological descriptions in UNESCO dossiers contain extensive species inventories and cave measurements that yield more paragraphs during extraction than architectural narratives.
- **Propagation Path:**
  1. *Prepared Corpus:* Dense cluster of Mulu/Kinabalu chunks in vector space.
  2. *Vector Retrieval:* Generic queries (*"What biodiversity is protected in Malaysia?"*) heavily skew toward Mulu, crowding out cultural biodiversity or FRIM forest data.
  3. *User Generation:* Unbalanced coverage presented to the end user.
- **Intervention:** Implement Maximal Marginal Relevance (MMR) retrieval with topical diversification and site-specific metadata filtering.

---

## 5. Privacy, Consent, Rights/Access, and Data Governance

| Governance Dimension | Audit Finding | Compliance Status | Operational Policy / Owner |
|---|---|:---:|---|
| **Data Ownership & Provenance** | 100% of chunks trace to official government and international bodies (UNESCO WHC and Jabatan Warisan Negara). | **Compliant** | Provenance maintained via `sources.csv` and cryptographic SHA-256 hashes. |
| **Intellectual Property & Licensing** | UNESCO documents are published under Creative Commons Attribution-ShareAlike 3.0 IGO (`CC-BY-SA 3.0 IGO`). JWN documents are open government public information. | **Compliant** | Mandatory citation notice: *"Information derived from official UNESCO World Heritage Centre and Jabatan Warisan Negara public records."* |
| **Personal Identifiable Information (PDPA)** | Zero private citizen data, student records, phone numbers, or residential addresses exist in the corpus. Contains only institutional contact email (`info@heritage.gov.my`). | **Compliant** | Fully compliant with the Malaysian Personal Data Protection Act 2010 (PDPA). |
| **Consent & Collection Basis** | All documents were published openly for public awareness, education, and statutory compliance. | **Compliant** | No individual consent required for public legislative and heritage documentation. |
| **Version & Retention Lifecycle** | Current snapshot reflects official state as of November 2026. | **Active Maintenance** | Quarterly automated re-ingestion scheduled to capture newly gazetted national heritage listings and UNESCO State of Conservation reports. |

---

## 6. Mitigation Plan and Residual Risk

| Identified Quality / Bias Risk | Empirical Evidence | Engineering Mitigation | Owner & Implementation Timing | Residual Risk & Post-Mitigation Impact |
|---|---|---|---|---|
| **Severe Language Imbalance** | 98.4% EN vs 1.6% MS chunks | 1. Mandate cross-lingual bilingual embedding models (`multilingual-e5-base`).<br>2. Ingest full-text Malay Act 645 legislation in Topic 5. | Data Engineering Team<br>(Phase 2 / Topic 5 & 7) | **Low–Medium:** Dense retrieval bridges semantic queries; technical statutory phrasing in Malay may still require exact BM25 keyword matching. |
| **Isolated Heading Chunks** | 2 chunks < 40 chars (*"Integrity"*) | Implement header-aware chunk merging in document pipeline preprocessor. | Pipeline Team<br>(Pre-Topic 7) | **Negligible:** Chunks will be conjoined to subsequent body text, eliminating low-information chunks. |
| **Temporal Staleness of 2000 Inscriptions** | 25-year-old nomination descriptions for Mulu and Kinabalu | Inject `[Inscription Date: YYYY]` into chunk metadata and system prompt instructions. | RAG Prompt Engineer<br>(Topic 7) | **Low:** Users are explicitly informed of the baseline vintage of historical nomination texts. |
| **Web Navigation Boilerplate** | Chunk 000 contains portal navigation links | Filter chunks triggering navigation link regex patterns (`HRMIS`, `Staff Directory`) from the clean vector index. | Data Cleaning Engineer<br>(Topic 4 / Completed) | **Zero:** Boilerplate chunks excluded from vectorstore indexing. |

---

## 7. Impact on Topic 2 Requirements / Evaluation Criteria

| Topic 2 Requirement | Potential Failure Mode if Left Unresolved | Topic 4 Engineering Safeguard | Residual Failure Risk |
|---|---|---|---|
| **FR1 (Heritage Q&A)** | System retrieves navigation footers or isolated headings instead of factual criteria. | Deduplication and minimum length validation rule (`char_count >= 40`). | **Low** |
| **FR2 (Legal & Statutory)** | Act 645 statutory definitions truncated mid-sentence by fixed-width slicing. | Topic 3 paragraph-aware chunking preserved; verified 100% intact text blocks. | **Low** |
| **FR5 (Bilingual Assistance)** | System fails to retrieve relevant content for queries in Bahasa Malaysia due to 98.4% English corpus skew. | Mandatory condition: cross-lingual dense embedding model (`multilingual-e5-base`) in Topic 7. | **Medium** (requires Topic 8 evaluation) |
| **NFR4 (Reproducibility)** | Non-deterministic chunk IDs or changing hashes cause inconsistent test runs. | SHA-256 deduplication and repeatable Pandera schema validation gates. | **Zero** |
| **RAI1 & RAI3 (Provenance & Attribution)** | Hallucinated facts or unsourced claims presented without official verification. | 100% of chunks carry verified HTTPS canonical URLs and cryptographic source hashes. | **Zero** |

---

## 8. Topic 4 Quality Gate Decision

```
================================================================================
FINAL QUALITY GATE DECISION: GO WITH CONDITIONS
================================================================================
```

### Decision Justification
The prepared corpus demonstrates high structural integrity, zero encoding defects, 100% verifiable institutional provenance, and effective elimination of 26 exact duplicate boilerplate chunks. The dataset is technically sound and ready to proceed to Phase 2 (Model Selection in Topic 5 and Vector Indexing in Topic 7).

### Mandatory Conditions for Phase 2:
1. **Cross-Lingual Embedding Requirement (Topic 7):**  
   Because the corpus currently exhibits a 98.4% English representation bias, the retrieval engine must employ a proven cross-lingual embedding model (e.g. `multilingual-e5-base` or `BGE-M3`) to ensure Bahasa Malaysia user queries successfully retrieve relevant English UNESCO documentation.
2. **Supplemental Malay Statutory Ingestion (Topic 5):**  
   The full text of *Akta Warisan Kebangsaan 2005 (Akta 645)* must be ingested to expand Bahasa Malaysia statutory coverage from 3 chunks to $\ge 40$ chunks.
3. **Mandatory Provenance Citation (Topic 7/8):**  
   The RAG generator prompt must cite the official source URL and publisher (`UNESCO World Heritage Centre` or `Jabatan Warisan Negara`) for every retrieved proposition to uphold Responsible AI commitments (RAI1, RAI3).

---
*Report approved by MASHeritage AI Engineering Team — Topic 4 Quality Gate Complete.*
