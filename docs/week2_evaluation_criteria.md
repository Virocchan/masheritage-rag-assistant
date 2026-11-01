# Evaluation Criteria Table — MASHeritage

| Objective / Requirement ID | Evaluation Criterion | Capability Bucket | Measurement Method | Metric | Threshold | User / Business Outcome |
|---|---|---|---|---|---|---|
| O2 / NFR2 / RAI1 | Bilingual Retrieval & Answer Accuracy | Domain-specific capability | Evaluate a defined set of 100 supported bilingual heritage queries (50 EN, 50 MS) using a rubric. | Correct response rate (split by language) | ≥ 80% overall; Malay-English gap ≤ 10% | Users receive sufficiently reliable historical and cultural facts regardless of language choice. |
| O1 / FR3 / RAI3 | Source Citation and Support | Instruction-following capability | Inspect document-grounded responses for citation presence and verify whether cited sources support the answer. | Citation presence rate; citation-source match rate | 100% presence; ≥ 90% match | Users can verify historical and cultural information against official state and UNESCO sources. |
| O3 / FR4 / RAI2 | Out-of-Scope Refusal | Instruction-following capability | Test the system with a defined safety/scope query set containing at least 20 out-of-scope prompts. | Refusal-and-redirect success rate | ≥ 85% | Reduces inappropriate advice outside the intended Malaysian heritage domain. |
| O2 / NFR1 | Response Latency | Cost and latency | Measure end-to-end response time across the defined 50-query evaluation workload. | p90 latency | < 4.0 s | Users receive sufficiently responsive interaction without disruptive delays. |

---

### Reflection: Topic 2 Part B
*Which evaluation criterion is most important for determining whether your AI application will be useful to its intended users? Why?*
> **Reflection Answer**: The **Bilingual Retrieval & Answer Accuracy** criterion linked with O2, NFR2, and RAI1 is the most important. Because MASHeritage's core value proposition is bridging English and Malay heritage data for tourists and students, failing to maintain parity or factual correctness across both languages directly invalidates the system's trustworthiness.
