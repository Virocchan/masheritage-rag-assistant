# Requirements Specification — MASHeritage
Version: 1.0

## Section 0 — Project Framing & Application Scope Checkpoint

| Framing element | What you must confirm |
|---|---|
| Problem + evidence | Information about Malaysia's World Heritage sites is fragmented across UNESCO, government, and museum documents in English and Malay. International visitor arrivals reached 42.2 million in 2025 (an 11.2% increase), and FRIM Selangor Forest Park became Malaysia's 6th World Heritage site in July 2025. Visitors and students lack a unified, trustworthy bilingual assistant.<br><br>*Sources*: [The Vibes Tourism Report (2025)](https://www.thevibes.com/articles/news/124424/govt-intensifies-tourism-drive-with-focus-on-china-india-and-japan-as-visitor-numbers-rise); [UNESCO World Heritage Malaysia](https://whc.unesco.org/en/statesparties/my/documents). |
| Existing Approaches | 1. *BGE M3-Embedding*: Multilingual dense/sparse retrieval supporting 100+ languages (Chen et al., 2024), but untested on specialized Malay heritage terms.<br>2. *Faux Polyglot Study*: Diagnosed systemic cross-language retrieval and generation bias favoring query language (Sharma et al., 2025), evaluated on synthetic data without a deployed assistant.<br>3. *London Museum Clio 1.0*: Single-language (English) museum RAG chatbot that reduces hallucinations via grounding, lacking cross-lingual support. |
| Project / Engineering Gap | Existing solutions lack a bilingual English/Malay heritage RAG pipeline evaluated explicitly per language (including cross-lingual cases like Malay questions to English documents) with robust abstention controls when evidence is absent. |
| Objective O1 | To build a RAG pipeline that answers English and Malay heritage questions from 3+ public sources, with each answer citing its document and section. |
| Objective O2 | To evaluate retrieval and answers per language on an 80-100 question bilingual test set, comparing BM25, multilingual dense and hybrid retrieval (target Recall@5 of at least 0.80, with the Malay-to-English gap within 10 points). |
| Objective O3 (if relevant) | To add guardrails so the system abstains when evidence is missing (target at least 85% correct refusals) and keeps at least 90% of claims supported by cited text. |
| Intended Users | Tourists (local and international), history and heritage students, tour guides, and museum staff who need consistent bilingual answers. |
| Supported Tasks | Answering factual questions about Malaysian World Heritage sites, cross-lingual retrieval (querying in Malay, retrieving English documents), providing section-level source citations, and defining cultural terms. |
| Information / Knowledge Domain | Official public documentation from UNESCO World Heritage Centre, Ministry of Tourism, Arts and Culture (MOTAC) Malaysia, and Portal Rasmi Jabatan Warisan Negara. |
| Operating Context | Web-based conversational chatbot interface accessed by desktop and mobile users requiring responsive bilingual interactions. |
| Important Constraints | Reliance on public web documentation structure; handling bilingual semantic nuances between English and Bahasa Malaysia; managing API latency and inference costs. |
| Explicit Out-of-Scope Tasks | The system shall not book tickets, arrange tours, provide travel agency recommendations, or decide heritage protection policies or funding. |
| Evaluation Focus | Determining retrieval accuracy, cross-lingual performance parity between English and Malay, citation faithfulness, and abstention correctness on out-of-scope or unsupported queries. |

---

## Section 1 — Functional Requirements Specification

| # | Requirement — The system SHALL | Scope Boundary — SHALL NOT (where relevant) |
|---|---|---|
| FR1 | Answer user queries regarding Malaysian World Heritage sites, history, criteria, and official documents in either English or Bahasa Malaysia. | Invent historical dates, site criteria, or administrative details unsupported by source documents. |
| FR2 | Perform cross-lingual retrieval, allowing users to query in Malay and retrieve relevant English source texts (and vice versa) to synthesize a response. | Silently drop or ignore documents written exclusively in the non-query language during hybrid search retrieval. |
| FR3 | Include precise document titles, sections, or URL references for every factual claim presented in an answer. | Present uncited or general parametric model knowledge as official approved heritage facts. |
| FR4 | Decline queries falling outside Malaysian World Heritage sites or the approved knowledge base and provide a polite redirect message. | Provide travel booking advice, itinerary planning, commercial recommendations, or legal/financial guidance. |
| FR5 | Provide a bilingual glossary definition or clarification when specialized cultural or heritage terms are requested. | - |

---

## Section 2 — Non-Functional Requirements Specification

| # | Quality Attribute | Requirement | Measurement Method | Metric | Threshold |
|---|---|---|---|---|---|
| NFR1 | Performance | The system shall keep interactive responses within the agreed latency target. | Measure end-to-end latency on a defined test workload of 50 bilingual queries. | p90 latency | < 4,000 ms |
| NFR2 | Correctness | Answers shall be factually consistent with approved source documents. | Score a curated evaluation set of 80 bilingual items using a defined rubric. | Correct response rate (%) | ≥ 80% |
| NFR3 | Cost | Inference cost shall remain within the project budget. | Record model and embedding API usage over the evaluation workload. | Cost per 100 queries | < US$0.40 per 100 queries |
| NFR4 | Maintainability | Approved source updates shall be incorporated without rebuilding unrelated components. | Run a controlled document-update and indexing test on new markdown/PDF files. | Update time | < 15 min |

---

## Section 3 — Responsible AI Requirements Specification

| # | Responsible AI Risk | Requirement | Measurement Method | Metric | Threshold |
|---|---|---|---|---|---|
| RAI1 | Fairness / Language Bias | System performance shall not differ beyond the agreed tolerance across English and Malay user groups. | Evaluate a stratified test set and compare correctness rates across English and Malay language queries. | Absolute correctness-rate gap between languages | ≤ 10 percentage points |
| RAI2 | Safety / Scope | The system shall refuse out-of-scope queries and redirect users appropriately. | Run a defined safety/scope test set containing at least 20 out-of-scope queries. | Refusal-and-redirect success rate | ≥ 85% |
| RAI3 | Transparency / Grounding | The system shall provide a verifiable source reference for document-grounded answers and indicate when sufficient supporting evidence cannot be found. | Evaluate document-grounded responses for citation presence and whether the cited source supports the answer. | Citation presence rate; citation-source match rate | 100% citation presence; ≥ 90% citation-source match |

---

### Reflection: Topic 2 Part A
*Which Responsible AI requirement in your project will be the most difficult to measure or enforce technically? Why?*
> **Reflection Answer**: RAI1 (Fairness / Language Bias across English and Malay queries) will be the most difficult to enforce technically due to lexical and morphosyntactic divergences between English and Bahasa Malaysia. BM25 and sparse retrieval models often struggle with Malay suffix variations (e.g., *perbadanan*, *berperbadanan*) and historical loanwords, leading to asymmetric retrieval performance even with advanced multilingual embedding models.
