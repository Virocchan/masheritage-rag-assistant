# Week 3 Data Inventory — MASHeritage

**Selected pathway:** Pathway A — Document / Text (Unstructured Heritage Corpus)  
**Project Application:** Bilingual (English/Bahasa Malaysia) Malaysian Heritage Q&A RAG Assistant  
**Traceability Mapping:**
- **FR1 (Heritage Q&A):** Authoritative descriptions of Malaysia's 6 inscribed UNESCO World Heritage properties.
- **FR2 (Cross-Lingual Retrieval):** Bilingual corpus spanning official English (UNESCO, JWN English) and Bahasa Malaysia (JWN Malay register & policy, MOTAC).
- **FR3 & RAI3 (Source Citations & Grounding):** Granular provenance tracking (Source ID, Canonical URL, SHA-256 fingerprint, publisher).
- **FR5 (Heritage Terminology):** National Heritage Act (Akta 645) terminology and Malay heritage classifications (*warisan kebangsaan*, *tapak warisan*, *kriteria OUV*).
- **NFR4 (Reproducible Source Updates):** Deterministic, automated scraping and preprocessing pipeline executing in < 15 minutes.
- **RAI1 (English/Malay Parity):** Stratified multilingual evaluation and explicit tracking of language distribution.

---

## 1. Corpus Inventory Table (Step A4 Standard)

| Source ID | Filename / URL | Type and purpose | Version / date / owner | Access / rights | Inspection evidence |
|---|---|---|---|---|---|
| `UNESCO_MY` | `https://whc.unesco.org/en/statesparties/my/`<br>`data/raw/sources/UNESCO_MY.txt` | Unstructured HTML/TXT;<br>National heritage overview & property index | 2026-11 (Latest web);<br>UNESCO World Heritage Centre | Public portal;<br>Attribution required | 1,875 chars, 254 words. Valid UTF-8. Confirms 6 inscribed Malaysian properties. SHA-256: `e48a7e2458...` |
| `UNESCO_1223` | `https://whc.unesco.org/en/list/1223/`<br>`data/raw/sources/UNESCO_1223.txt` | Unstructured HTML/TXT;<br>OUV criteria, history, conservation of Melaka & George Town | Inscribed 2008;<br>UNESCO WHC | CC-BY-SA IGO 3.0;<br>Public reuse | 8,844 chars, 1,308 words. Rich narrative sections on Straits trading history, architecture, Criteria (ii)(iii)(iv). SHA-256: `cf748edad7...` |
| `UNESCO_1012` | `https://whc.unesco.org/en/list/1012/`<br>`data/raw/sources/UNESCO_1012.txt` | Unstructured HTML/TXT;<br>Natural heritage, biodiversity, geology of Kinabalu Park | Inscribed 2000;<br>UNESCO WHC | CC-BY-SA IGO 3.0;<br>Public reuse | 11,719 chars, 1,735 words. Ecological descriptions, altitudinal zones, Criteria (ix)(x). SHA-256: `adcd7ed29c...` |
| `UNESCO_1013` | `https://whc.unesco.org/en/list/1013/`<br>`data/raw/sources/UNESCO_1013.txt` | Unstructured HTML/TXT;<br>Karst topography, cave systems, biodiversity of Gunung Mulu | Inscribed 2000;<br>UNESCO WHC | CC-BY-SA IGO 3.0;<br>Public reuse | 17,218 chars, 2,683 words. Detailed cave passage stats, pinnacle formations, Criteria (vii)(viii)(ix)(x). SHA-256: `8bca13139f...` |
| `UNESCO_1396` | `https://whc.unesco.org/en/list/1396/`<br>`data/raw/sources/UNESCO_1396.txt` | Unstructured HTML/TXT;<br>Archaeological heritage, Perak Man, palaeolithic culture of Lenggong Valley | Inscribed 2012;<br>UNESCO WHC | CC-BY-SA IGO 3.0;<br>Public reuse | 8,769 chars, 1,329 words. Prehistoric stone tool workshops, hominid remains, Criteria (iii)(iv). SHA-256: `fee72afc32...` |
| `UNESCO_1014` | `https://whc.unesco.org/en/list/1014/`<br>`data/raw/sources/UNESCO_1014.txt` | Unstructured HTML/TXT;<br>Rainforest archaeological sequence, burial caves of Niah Caves Complex | Inscribed 2024;<br>UNESCO WHC | CC-BY-SA IGO 3.0;<br>Public reuse | 8,243 chars, 1,209 words. 50,000-year human occupation evidence, cave paintings, Criteria (iii)(v). SHA-256: `acf5ff13c6...` |
| `UNESCO_1734` | `https://whc.unesco.org/en/list/1734/`<br>`data/raw/sources/UNESCO_1734.txt` | Unstructured HTML/TXT;<br>Man-made tropical rainforest, forestry conservation of FRIM Forest Park Selangor | Inscribed July 2025;<br>UNESCO WHC | CC-BY-SA IGO 3.0;<br>Public reuse | 10,394 chars, 1,486 words. 6th World Heritage Site; reafforestation history, research arboreta, Criteria (v). SHA-256: `114ea7702f...` |
| `JWN_REGISTER_MS` | `https://www.heritage.gov.my/ms/tapak-warisan`<br>`data/raw/sources/JWN_REGISTER_MS.txt` | Unstructured HTML/TXT;<br>Official national gazette portal, state sites, Malay heritage terms | 2026-11;<br>Jabatan Warisan Negara | Official portal;<br>Public view; check reuse terms | 524 chars, 66 words. Bahasa Malaysia register text. Valid UTF-8. Covers national gazetted sites. SHA-256: `03a02d5f91...` |
| `JWN_REGISTER_EN` | `https://www.heritage.gov.my/en/tapak-warisan`<br>`data/raw/sources/JWN_REGISTER_EN.txt` | Unstructured HTML/TXT;<br>English portal version of National Heritage Register | 2026-11;<br>Jabatan Warisan Negara | Official portal;<br>Public view; check reuse terms | 519 chars, 66 words. English portal parallel to Malay register. SHA-256: `a4dfade67f...` |
| `JWN_ACT_MS` | `https://www.heritage.gov.my/ms/info-jwn/dasar-perundangan.html`<br>`data/raw/sources/JWN_ACT_MS.txt` | Unstructured HTML/TXT;<br>National Heritage Act 2005 (Akta 645) policy and legal definitions | Act 645 (2005);<br>Jabatan Warisan Negara | Official legislation / policy;<br>Public guidance | 459 chars, 60 words. Malay legal definitions for cultural, natural, and intangible heritage. SHA-256: `825a11a03e...` |
| `JWN_ACT_EN` | `https://www.heritage.gov.my/en/jwn-info/policy-and-legislation.html`<br>`data/raw/sources/JWN_ACT_EN.txt` | Unstructured HTML/TXT;<br>National Heritage Act policy in English | Act 645 (2005);<br>Jabatan Warisan Negara | Official legislation / policy;<br>Public guidance | 436 chars, 57 words. English legal terminology and administration structures under Act 645. SHA-256: `5ff22d1b20...` |
| `MOTAC_CULTURE_STATS` | `https://www.motac.gov.my/.../Buku-Data-Sektor-Kebudayaan-2022-2024.pdf` | Structured/Unstructured PDF;<br>Supplementary statistical report on cultural sites & funding | 2024 Edition;<br>MOTAC Malaysia | Public government PDF;<br>Educational use | Supplementary PDF file for future expansion; tracked in registry but skipped by HTML text scraper. |

---

## 2. In-Depth Inspection Observations (Step A3 Evidence)

### Inspection Record 1: English Representative Artefact (`UNESCO_1223.txt`)
- **Origin & Format:** Clean UTF-8 text extracted from UNESCO World Heritage Centre property page.
- **Size & Metrics:** 8,844 characters, 1,308 words across 18 paragraphs.
- **Structural Properties:** Contains clear semantic headings (`Outstanding Universal Value`, `Brief synthesis`, `Criterion (ii)`, `Integrity`, `Authenticity`, `Management and protection requirements`).
- **Domain Content:** Covers the 500-year trading history between East and West, multicultural residential quarters, Baba Nyonya architecture, and specific gazetted conservation buffer zones in Melaka and George Town.
- **Observed Constraints:** High density of multi-sentence paragraphs exceeding 1,000 characters; requires chunking to fit RAG embedding context windows without truncating mid-sentence.

### Inspection Record 2: Bahasa Malaysia Representative Artefact (`JWN_REGISTER_MS.txt`)
- **Origin & Format:** UTF-8 text scraped from Jabatan Warisan Negara official portal.
- **Size & Metrics:** 524 characters, 66 words.
- **Structural Properties:** Short declarative text introducing the National Heritage Register (*Daftar Warisan Kebangsaan*) under the National Heritage Act 2005 (*Akta Warisan Kebangsaan 2005 [Akta 645]*).
- **Domain Content:** Establishes legal authority and definitions for gazetted cultural and natural sites in Malaysia.
- **Observed Constraints:** Significantly shorter than UNESCO descriptive texts; represents portal introduction rather than full paginated site tables. Highlights the necessity of paragraph-aware boundary handling so short entries remain coherent single chunks without arbitrary padding.

---

## 3. Storage Hierarchy & Lineage Separation

| Storage Stage | Directory Location | Committed to Git? | Contents & Policy |
|---|---|---|---|
| **Raw Layer** | `data/raw/sources/*.txt` | Yes (Controlled) | Unmodified text dumps from HTTP scraper. Cryptographically fingerprinted with SHA-256 in `data/raw/source_manifest.json`. |
| **Processed Layer (Part B)** | `data/processed/*.txt`<br>`data/processed/prepared_text.jsonl` | Yes | Normalized text files (`*_clean.txt`) and chunked JSONL export (`prepared_text.jsonl`) with metadata. |
| **Part B Manifest** | `data/week3_manifest.json` | Yes | Lineage audit record detailing input-to-output SHA-256 transformations, timestamps, and parameters. |
| **Pipeline V1 (Part C)** | `data/pipeline_v1/documents/` | Yes | Repeatable pipeline outputs: `prepared_text.jsonl` (215 chunks) and `pipeline_manifest.json`. |

---

## 4. Responsible AI & Corpus Quality Reflection

1. **Language Asymmetry (RAI1):** UNESCO's documentation is English-first and contains extensive historical, environmental, and geological descriptions (77,062 total characters across 7 files). Jabatan Warisan Negara (JWN) provides authoritative Malay administrative terminology, but the texts are concise (1,938 total characters across 4 files). The corpus is therefore **not a sentence-aligned parallel corpus**. In Topic 4, retrieval parity will be evaluated using cross-lingual queries (Malay query to English document) rather than assuming equal corpus volume.
2. **Licensing & Redistribution Rights:** UNESCO texts are distributed under CC-BY-SA IGO 3.0. JWN and MOTAC materials are public government documents; however, raw scraped HTML contains dynamic UI elements. Scraping extracts strictly the informational text blocks, preserving source URLs for mandatory attribution.
3. **Purity of Ingestion:** No machine translation was applied during ingestion. Malay sources retain authentic morphological terminology (*perbadanan*, *pemuliharaan*, *tapak warisan*, *gazet*) to support genuine cross-lingual retrieval benchmarks.
