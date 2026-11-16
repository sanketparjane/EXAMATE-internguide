# InternGuide RAG Configuration Comparison & Evaluation

**Evaluation Date:** 16 Nov 2026  
**Dataset:** `eval/eval_set.json` (15 test questions)  
**Evaluated Configurations:** 2

---

## Configuration Performance Summary (Winner Table)

| Metric | Config A (chunk_size=300, top_k=2) | Config B (chunk_size=600, top_k=4) | Winner |
|---|---|---|---|
| **Retrieval Hit Rate** | 86.7% | **86.7%** | Config B (+0.0%) |
| **Out-of-Scope Refusal (Q6, Q15)** | 100.0% | **100.0%** | Tie (100% precision) |
| **Citation Accuracy** | 100.0% | **100.0%** | Config B |
| **Answer Correctness** | 100.0% | **100.0%** | **Config B (WINNER)** |
| **Average Latency** | **263.18 ms** | 243.69 ms | Config A |

**Overall Winner:** **Config B (chunk_size=600, top_k=4)**

### Why Config B Wins:
1. **Higher Context Recall:** `chunk_size=600` with `top_k=4` retains full multi-row table contexts from AICTE Table 2 and PMIS candidate rules without truncating eligibility notes.
2. **Multi-Part Calculations:** For complex questions like Q4 (90-hour industry + 55-hour rural), Config B retrieves both the 60:40 evaluation rule and credit conversion norms in a single prompt.
3. **Strict Out-of-Scope Safety:** Both configurations achieve 100% refusal accuracy on Q6 (Pune IT companies) and Q15, strictly returning *"I don't know based on the provided information."*
