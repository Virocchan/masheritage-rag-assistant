# Week 1 Project Scope — MASHeritage
Version: 1.0

| Field | Content |
|---|---|
| **Project Name** | **MASHeritage: Bilingual Malaysian Heritage Q&A Assistant** |
| **Domain** | Cultural Heritage & Tourism AI / Multilingual Retrieval-Augmented Generation (RAG) |
| **Problem Statement** | Authoritative information regarding Malaysia's UNESCO World Heritage sites is fragmented across international, federal, and state documentation in English and Bahasa Malaysia. Visitors, students, and guides lack a unified, trustworthy conversational assistant capable of answering questions accurately across both languages with verifiable citations. |
| **Evidence of the Problem** | **Evidence 1**: Influx of international and local heritage visitors (42.2 million arrivals in 2025, an 11.2% year-on-year increase) paired with recent heritage inscriptions (FRIM Selangor Forest Park inscribed as Malaysia's 6th World Heritage property in July 2025) underscores the growing demand for accessible, up-to-date heritage knowledge.<br>*Source / citation*: [The Vibes Tourism Industry Report (2025)](https://www.thevibes.com/articles/news/124424/govt-intensifies-tourism-drive-with-focus-on-china-india-and-japan-as-visitor-numbers-rise); Tourism Malaysia Official Statistics.<br><br>**Evidence 2**: Official public heritage records are divided across English-first UNESCO documentation and Malay-first statutory portals (Jabatan Warisan Negara), creating an information silo where monolingual searches fail to retrieve vital cross-lingual context.<br>*Source / citation*: [UNESCO World Heritage Centre Malaysia Documentation](https://whc.unesco.org/en/statesparties/my/documents); [Portal Rasmi Jabatan Warisan Negara](https://www.heritage.gov.my). |
| **Initial Related Work (at least 3)** | **Study / solution 1**: *BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation*<br>*Source / citation*: Chen et al., 2024 (arXiv:2402.03216)<br>*Key limitation*: Evaluated primarily on broad generic benchmarks; lacks fine-grained validation on domain-specific Bahasa Malaysia heritage terminology and cultural morphological variants.<br><br>**Study / solution 2**: *The Faux Polyglot: Diagnosing Cross-Lingual Biases and Vulnerabilities in Multilingual RAG*<br>*Source / citation*: Sharma et al., 2025 (arXiv:2501.08253)<br>*Key limitation*: Focuses on diagnosing cross-lingual generative drift on synthetic datasets; does not provide an implemented, grounded domain retrieval pipeline with verified citation tracking.<br><br>**Study / solution 3**: *Museum of London Clio 1.0 (Museum Conversational Grounded Assistant)*<br>*Source / citation*: London Museum Digital Heritage Initiative (2024)<br>*Key limitation*: Operates exclusively in a monolingual English environment; does not address cross-lingual queries or dual-language official statutory records. |
| **Engineering Gap / Limitation** | What practical or technical limitation remains unresolved?<br>**Gap / Limitation**: Existing solutions lack a bilingual (English / Bahasa Malaysia) domain-specific RAG architecture capable of performing cross-lingual retrieval (e.g. querying in Malay against English UNESCO records), enforcing verifiable section-level citations, and reliably abstaining when evidence is absent. |
| **Initial Project Objectives (2–3)** | **O1**: To design and build a bilingual RAG pipeline that answers English and Malay queries using official public heritage sources, with every factual claim grounded and cited by document title and section.<br>**O2**: To evaluate retrieval recall and answer correctness across an 80–100 bilingual test suite, comparing sparse (BM25), dense (multilingual embedding), and hybrid retrieval to ensure the English-Malay accuracy gap is within 10 percentage points.<br>**O3**: To implement safety and abstention guardrails that prevent hallucinations and achieve at least 85% correct refusals on out-of-scope or ungrounded queries. |
| **Target Users** | 1. **Tourists (domestic and international)** seeking verified historical facts, criteria, and official cultural background.<br>2. **History, heritage, and architecture students** researching Malaysian UNESCO properties.<br>3. **Tour guides and museum educators** requiring consistent, bilingual reference material. |
| **Data Sources (at least 2)** | **Source 1**: UNESCO World Heritage Centre — URL: `https://whc.unesco.org/en/statesparties/my/documents`<br>**Source 2**: Jabatan Warisan Negara (Department of National Heritage Malaysia) — URL: `https://www.heritage.gov.my`<br>**Source 3**: Ministry of Tourism, Arts and Culture (MOTAC) Malaysia — URL: `https://www.motac.gov.my` |
| **Similar to EduAdvisor** | Both applications are document-grounded informational Q&A assistants that enforce strict source citations, implement scope boundaries to refuse out-of-scope queries, and require structured evaluation of retrieval and generation correctness. |
| **Different from EduAdvisor** | EduAdvisor is a monolingual English university advisory assistant focused on course catalogues and prerequisites. MASHeritage addresses bilingual English / Bahasa Malaysia cross-lingual retrieval over asymmetric cultural texts, specialized historical vocabulary, and dual-language statutory governance. |
| **Responsible AI Risks (at least 2)** | **Risk 1 (Fairness / Language Bias)**: Disparity in retrieval recall or generation quality between English and Malay queries due to asymmetric document volumes and vocabulary tokenization differences.<br>**Risk 2 (Transparency & Grounding / Hallucination)**: Inventing historical events, altering gazetted dates, or misattributing cultural significance without supporting evidence from official heritage sources.<br>**Risk 3 (Scope & Safety)**: Providing commercial travel recommendations, booking advice, or speculative legal/archaeological interpretations outside the approved public documentation. |

---

### Step C3 — GitHub Repository Setup Checklist

- [x] Repository initialized with standard naming (`ai-engineering-masheritage` / `masheritage-rag-assistant`)
- [x] Directory structure configured:
  ```
  ├── docs/
  ├── data/
  ├── src/
  ├── notebooks/
  ├── evaluation/
  └── prompts/
  ```
- [x] `.gitignore` configured to ensure API keys, credentials, and non-redistributable binary files are never committed.
- [x] Non-empty `.gitkeep` markers added where directories are staged.
