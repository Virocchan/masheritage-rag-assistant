# Project Scope: MASHeritage

## Description
A bilingual (English/Malay) RAG assistant for Malaysian heritage sites, answering from official public documents with citations.

## Target Users and Use Cases
| User | Use case |
|---|---|
| Tourists | Background on a site before or during a visit |
| Students | Find and compare information across documents |
| Guides/museum staff | Consistent bilingual answers to common questions |

## Selected Sites (5-8, fix by Week 2)
1. Melaka and George Town
2. Lenggong Valley
3. Gunung Mulu National Park
4. Kinabalu Park
5. Niah Caves (check UNESCO's current Malaysia list)

## In Scope
- Q&A with citations, English and Malay
- Cross-lingual retrieval
- Metadata filters (site, state, type, language, source)
- Comparison of 2-3 sites
- "Not found in documents" responses
- Streamlit/Gradio UI with language toggle

## Out of Scope
- Itineraries, booking, live info
- Resolving disputed historical claims
- Image recognition/generation
- Unrelated chat

## Evaluation Targets
Recall@5 >= 0.80; correctness >= 80%; faithfulness >= 90%; citation accuracy >= 90%; abstention >= 85%; language consistency >= 95%; median latency < 5 s.
