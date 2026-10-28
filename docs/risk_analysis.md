# Risk Analysis: MASHeritage

| Risk | Impact | Control |
|---|---|---|
| Hallucinated dates/names/facts | Misinformation about heritage | Answer only from retrieved text; show snippets; abstain on low confidence |
| Translation distortion of cultural terms | Misrepresenting communities | Keep original terms; glossary in `data/glossary.csv`; spot check Malay output |
| Contested or sensitive history | Taking sides, offence | Attribute claims to sources; no opinions; refuse to adjudicate |
| Outdated information | Wrong details | Store document and access dates; show "last updated"; link to official site |
| Language bias (EN favoured over MS) | Poorer service for Malay users | Report metrics per language; 50/50 test set |
| Copyright | Redistribution issues | Cite and link; store only text allowed by terms; keep raw PDFs out of repo |
| Prompt injection via scraped pages | Manipulated output | Treat documents as data; sanitize at ingestion; adversarial tests |
| Privacy | Leaked user data | No personal data collected; anonymize logs |
