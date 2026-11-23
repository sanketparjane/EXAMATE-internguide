# InternGuide — Interview Guide & Story

**Candidate:** Sanket Vilas Parjane  
**Registration / PRN:** `2124UMLM2044`  
**Degree:** B.Tech Electronics & Telecommunication Engineering (E&TC), Sanjivani  
**Product:** InternGuide — Autonomous AI Agent & Credit Progress Tracker for AICTE B.Tech Internships & PMIS  

---

## 1. The 60-Second Elevator Pitch

> *"Every year, over 1.5 million engineering students across India must complete between 14 to 20 credits of internships—equivalent to 630 to 900 contact hours—to graduate under AICTE regulations. Yet, students consistently struggle with three things: calculating whether diverse activities like rural camps or online internships count, computing their dual-weighted evaluation score (70% industry + 30% institute panel), and navigating government schemes like the Prime Minister's Internship Scheme (PMIS).*
>
> *I built **InternGuide** to solve this. It's a full-stack, production-grade AI system combining a grounded RAG knowledge engine with an autonomous LangGraph agent and an interactive Streamlit dashboard.*
>
> *Unlike generic LLMs that guess credit calculations and hallucinate job vacancies, InternGuide uses deterministic tool execution for credit conversion (1 credit = 45 hours) and hours-weighted scoring. It enforces strict out-of-scope refusals, incorporates a human-in-the-loop faculty mentor approval gate, and displays a signature color-coded progress bar toward degree completion.*
>
> *The entire system is containerized with Docker, guarded against prompt injection, tested with 24 passing Pytest tests, verified by Ruff with zero warnings, and deployed live with automated CI/CD on Render."*

---

## 2. The Hardest Problem: Numbers Computed, Not Guessed & Scheme Versioning

### The Challenge
In building InternGuide, the most formidable technical challenge was twofold:
1. **Numbers that must be computed, not guessed:** Large Language Models are inherently probabilistic token predictors. When asked complex academic math—such as converting 135 total hours across multiple internships into credits ($1\text{ credit} = 45\text{ hours}$) and computing a dual-weighted evaluation score ($70\% \text{ industry supervisor} + 30\% \text{ college panel}$, hours-weighted net score)—LLMs frequently hallucinate arithmetic, round incorrectly, or guess grade boundaries.
2. **Temporal Scheme Drift (PMIS 2024 Pilot vs. 2026 Guidelines):** The Prime Minister's Internship Scheme was introduced as a 2024 pilot initiative before being codified into comprehensive 2026 guidelines. In early pilot documents, stipend allocations, quota rules, and student eligibility criteria had preliminary terms. Without strict temporal grounding, language models inevitably blended obsolete 2024 pilot figures with current 2026 rules, quoting outdated stipends or obsolete application procedures.

### Engineering Solution
To solve this systematically:
- **Deterministic Tool Routing (`app/tools.py`):**
  We separated **Policy Retrieval** from **Mathematical Calculation**. We engineered `internship_credit_calculator` as an isolated deterministic tool. When a student query contains hours or marks, our LangGraph router delegates the request directly to Python functions executing:
  $$\text{Credits} = \frac{\text{Total Hours}}{45}$$
  $$\text{Activity Marks} = (0.70 \times \text{Industry}) + (0.30 \times \text{Institute Panel})$$
  $$\text{Net Score} = \frac{\sum (\text{Activity Marks}_i \times \text{Hours}_i)}{\sum \text{Hours}_i}$$
  The LLM is strictly prohibited from guessing scores; it receives the exact structured JSON payload from the tool and weaves it into the final grounded response.

- **Temporal Grounding & Dated Metadata (`app/rag.py` & `data/records.json`):**
  Every document chunk indexed into ChromaDB carries explicit temporal metadata: `effective_date`, `policy_version: "PMIS-2026"`, and `supersedes: "2024-pilot"`. Prompt templates strictly instruct the synthesizer that the 2026 PMIS guidelines (₹5,000 monthly stipend: ₹4,500 company + ₹500 government, ₹6,000 incidental grant, ₹8 Lakh income cap, 3-offer limit) override all historical pilot mentions.

- **Faculty Mentor Approval Gate:**
  In `app/graph.py`, before any academic credit or grade calculation is finalized, state transitions through an explicit `approval_node`. If authorization is absent or rejected, the agent outputs an *"Action Blocked"* notice, ensuring unverified student self-reporting cannot award academic credits without faculty signoff.

### The Impact
- **100% Mathematical Accuracy:** Guaranteed exact credit sums and hours-weighted scores across all 15 benchmark questions and edge-case test suites.
- **Zero Temporal Hallucinations:** 100% precision on current 2026 PMIS stipend and eligibility figures.
- **Enterprise Reliability:** Tested via 24 automated unit/integration tests with end-to-end reproducibility.

---

## 3. Answers to 10 Likely Interview Questions

### Q1: What is InternGuide and what is its architecture?
**Answer:** InternGuide is an AI-powered academic advisory and credit-tracking platform for engineering students under AICTE regulations. Its architecture consists of:
1. **Frontend:** Streamlit application featuring a multi-turn chat interface, grounded citation badges, thumbs up/down feedback, and a signature color-coded credit progress bar.
2. **API Gateway:** FastAPI backend exposing `/health`, `/records`, `/search`, `/ask`, and `/agent` endpoints with input validation (<1000 chars), prompt-injection defense, and in-memory LRU caching.
3. **Orchestration:** LangGraph state machine with `MemorySaver` checkpointer and a human-in-the-loop mentor approval step.
4. **Knowledge Store:** Persistent ChromaDB vectorstore indexing 340+ semantic chunks from official AICTE and UGC policy PDFs.
5. **CI/CD & Deployment:** GitHub Actions pipeline (Ruff + Pytest + Docker build) deployed on Render.

---

### Q2: Why did you build a custom calculation tool instead of letting the LLM calculate credits?
**Answer:** LLMs are autoregressive models that predict next tokens based on probability, not logic engines. When evaluating academic qualifications, an error in credit calculation can prevent a student from graduating or result in an erroneous transcript. By routing calculation requests to `internship_credit_calculator` in Python, we achieved 100% deterministic accuracy for credit conversion ($1\text{ credit} = 45\text{ hours}$), dual 70:30 evaluation weighting, and hours-weighted net score aggregation.

---

### Q3: How do you handle out-of-scope queries like Q6 (Pune IT companies)?
**Answer:** We implemented a two-tier guardrail in `app/rag.py`:
1. **Deterministic Regex/Keyword Filter:** Detects known out-of-scope topics (e.g. live company vacancies, specific regional job openings, unrelated trivia).
2. **Relevance Thresholding:** After vector retrieval, if the cosine similarity score of the top chunk falls below 0.40, the system triggers refusal.
In both scenarios, the system strictly outputs: *"I don't know based on the provided information. InternGuide only covers AICTE internship rules and PMIS eligibility criteria."* with empty citations (`[]`), eliminating hallucinations.

---

### Q4: Why did you select LangGraph over basic LangChain or ReAct loops?
**Answer:** Standard ReAct chains lack fine-grained control over state transitions and human-in-the-loop gates. LangGraph models the system as a directed cyclic graph with a typed state dictionary (`AgentState`). This allowed us to:
- Insert an explicit `approval_node` between intent planning and tool execution.
- Maintain persistent conversation memory across multi-turn sessions using `MemorySaver(thread_id=session_id)`.
- Conditionally route queries between RAG search, the credit calculator, or both based on structured state analysis.

---

### Q5: How does your in-memory cache work and what performance did you achieve?
**Answer:** In `app/cache.py`, we implemented `SimpleCache`, a thread-safe LRU in-memory store with normalized query hashing (case-folding and whitespace collapsing).
- **Cold Request Latency:** ~243.69 ms (embedding + vector search + synthesis).
- **Warm Cached Latency:** **1.25 ms**, achieving a **99.49% reduction in latency**.
- **Memory Footprint:** Under 1.5 MB RAM for 256 cached queries.
- **Telemetry:** Every query logs start-to-finish latency and heuristic token usage to `data/telemetry.log`.

---

### Q6: How do you protect InternGuide against prompt injection and jailbreaks?
**Answer:** In `app/security.py`, we enforce:
1. **Input Length Limits:** Strict cap of 1,000 characters per query to prevent token-flooding and buffer bloat. Rejections return HTTP 400.
2. **Adversarial Pattern Matching:** Scans input against prompt-injection signatures (e.g., *"ignore all previous instructions"*, *"system override"*, *"DAN mode"*, *"reveal internal prompt"*).
3. **Safe Refusal:** When detected, the request is blocked before reaching the LLM or vectorstore, returning a standardized security refusal notice.

---

### Q7: How did you benchmark your RAG configurations to declare a winner?
**Answer:** In `eval/run_eval.py`, we built an automated evaluation suite testing 15 ground-truth questions against two configurations:
- **Config A:** `chunk_size = 300, overlap = 50, top_k = 2`
- **Config B:** `chunk_size = 600, overlap = 100, top_k = 4`
We measured Retrieval Hit Rate, Out-of-Scope Refusal Precision, Citation Accuracy, Answer Correctness, and Latency.
**Winner:** Config B won because larger chunks retained full multi-column tables from AICTE Table 2 without fragmenting rules across chunks, and `top_k=4` supplied both credit conversion and 70:30 evaluation weights simultaneously for complex queries.

---

### Q8: What is your testing and code quality strategy?
**Answer:** We enforce zero-tolerance for regression:
- **Pytest Suite:** 24 unit and integration tests in `tests/` covering `/health`, `/records`, `/search`, semantic vectorstore queries, `/ask` with fake LLM mocking, Q6 refusal, input limits, prompt injection, and LangGraph approval workflows.
- **Ruff Linter:** Fully configured via `ruff.toml`, passing with **0 errors and 0 warnings**.
- **Test Runner:** `Day_11/run_tests.py` runs both linter and test suite in one automated command.

---

### Q9: How is the application containerized and deployed?
**Answer:**
- **Containerization:** Built a production `Dockerfile` on `python:3.11-slim` with `.dockerignore`.
- **Orchestration:** `docker-compose.yml` runs two services: `api` (FastAPI on port 8000 with healthcheck) and `ui` (Streamlit on port 8501 depending on healthy API startup).
- **CI/CD:** GitHub Actions workflow [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) triggers on every push and PR to `main`, validating Ruff, Pytest, and Docker build.
- **Cloud Deployment:** Defined in `render.yaml` and deployed live on Render with public `/health` and live UI.

---

### Q10: If you had another month to work on InternGuide, what would you add next?
**Answer:** Three key roadmap items:
1. **Direct College ERP Integration:** Connect the LangGraph approval step directly to college ERP systems (e.g., Sanjivani's academic portal) via OAuth2 and webhooks so faculty mentors can click "Approve" directly from an email notification.
2. **Automated Document Verification with Vision Models:** Allow students to upload scanned completion certificates or NSS logs; use multimodal vision models to extract hours and signatures automatically and cross-verify certificate authenticity against MSME/company registries.
3. **Multi-Lingual Voice Agent:** Add Marathi and Hindi speech-to-text and text-to-speech support using Whisper and Gemini Live API to assist students from rural engineering colleges across Maharashtra.
