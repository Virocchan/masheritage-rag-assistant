# Week 3 Pipeline Diagram

The following Mermaid diagram visualises the full V1 data‑engineering pipeline for the Topic 3 lab, including source ingestion, raw storage, inspection, preparation, validation, lineage, and repeatability smoke‑test.

```mermaid
flowchart TD
    subgraph S1["1. SOURCE & INGESTION"]
        A["Official Sources<br/>• UNESCO World Heritage (EN)<br/>• JWN National Register & Act (MS/EN)<br/>• MOTAC Cultural Data (MS)"]
        B["Ingestion Engine<br/>src/ingestion/fetch_sources.py<br/>HTTP GET + BeautifulSoup + SSL Validation"]
        A --> B
        F1{{"⚠️ Failure Point 1:<br/>Host SSL Mismatch / 404 / Rate Limit"}}
        B -.- F1
        R1["Recovery / Response:<br/>• Enforce exact domain (www.heritage.gov.my)<br/>• Retry with backoff; log to source_manifest.json<br/>• Fail‑stop if valid sources < 2"]
        F1 -.- R1
    end

    subgraph S2["2. RAW STORAGE & INSPECTION"]
        B --> C["Raw Layer (data/raw/sources/)<br/>11 UTF‑8 TXT files + SHA‑256 Checksums<br/>source_manifest.json"]
        C --> D["Inspection & Quality Checks (Step A4)<br/>• Minimum character threshold (>250 chars)<br/>• Representative sampling: UNESCO (EN) vs JWN (MS)<br/>• Encoding and readability verification"]
        F2{{"⚠️ Failure Point 2:<br/>Empty Page / JS‑Rendered Blank Body"}}
        D -.- F2
        R2["Recovery / Response:<br/>• Length assertion check (len > 250)<br/>• Flag source in manifest, skip empty chunking<br/>• Halt pipeline if corpus is corrupted"]
        F2 -.- R2
    end

    subgraph S3["3. PREPARATION & TRANSFORMATION"]
        D --> E["Text Normalization & Cleaning<br/>• Normalise whitespace & newlines<br/>• Strip navigation/boilerplate<br/>• Output: data/processed/<id>_clean.txt"]
        E --> F["Paragraph‑Aware Chunking (Pathway A)<br/>• Max chunk size: 500 chars<br/>• Preserves paragraph/section boundaries<br/>• Injects provenance: URL, ID, SHA‑256, site"]
    end

    subgraph S4["4. VALIDATION, LINEAGE & REPEATABILITY"]
        F --> G["Validation Gate (Part B3 & C1)<br/>• Assert prepared_text.jsonl exists & non‑empty<br/>• Unique deterministic Record IDs<br/>• URL & Metadata completeness"]
        G --> H["Lineage & Artifact Storage (B4 & C1)<br/>• data/processed/prepared_text.jsonl<br/>• data/week3_manifest.json<br/>• data/pipeline_v1/documents/pipeline_manifest.json"]
        H --> I["Repeatability Smoke Verification (Cell 9)<br/>Assert source & output SHA‑256 fingerprints match across reruns"]
    end

    classDef stage fill:#f0f9ff,stroke:#0284c7,stroke-width:2px,color:#0f172a;
    classDef fail  fill:#fef2f2,stroke:#ef4444,stroke-width:2px,stroke-dasharray:5 5,color:#991b1b;
    classDef resp  fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#166534;
    class F1,F2 fail;
    class R1,R2 resp;
```

*When viewed in Antigravity or any Mermaid‑compatible renderer, this diagram will appear as a richly‑styled flowchart.*