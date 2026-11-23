# InternGuide — Daily Milestone Tracker (PROGRESS.md)

**Product:** InternGuide — AICTE B.Tech Internship & Credit Advisory Assistant  
**Student:** Sanket Vilas Parjane  
**PRN / Registration No:** `2124UMLM2044`  
**Department:** Electronics & Telecommunication Engineering (E&TC), Sanjivani College of Engineering  
**Project Status:** 🟢 **ALL 14 DAYS FULLY COMPLETED & CLOSED**  

---

## Daily Milestone Completion Matrix

| Day | Date | Milestone Topic | Key Deliverables | Status | Git Tag / Reference |
|:---:|:---:|---|---|:---:|:---:|
| **D1** | Fri 30 Oct | CLI Intro & Problem Definition | CLI interface, user input recording, domain problem setup | `[x] CLOSED` | Initial commits |
| **D2** | Mon 02 Nov | Structured Records & Domain Modeling | `Day_2/app_records.py`, `Day_2/app_cli.py`, domain rule modeling | `[x] CLOSED` | `Day_2/` |
| **D3** | Fri 06 Nov | PDF Parsing with `pdfplumber` | `app/ingest.py`, `pdfplumber` parsing of AICTE Table 2, `data/records.json` | `[x] CLOSED` | `feba8d9` |
| **D4** | Sat 07 Nov | FastAPI Server & TF-IDF Search | `Day_4/app_main.py`, `/health`, `/records`, `/search` endpoints | `[x] CLOSED` | `checkpoint-1` |
| **D5** | Thu 12 Nov | AICTE Rule Engine & LLM Setup | `app/llm.py`, Gemini SDK integration, error handling | `[x] CLOSED` | `Day_5/` |
| **D6** | Fri 13 Nov | Prompt Engineering & Evaluation | Prompts directory, few-shot examples, system instructions | `[x] CLOSED` | `week-1` |
| **D7** | Sat 14 Nov | Document Chunking & ChromaDB Vectorstore | `app/chunking.py`, `app/vectorstore.py`, `app/embed.py`, `/search/semantic` | `[x] CLOSED` | `5b54a58` |
| **D8** | Mon 16 Nov | Grounded RAG, Citations & Benchmark | `app/rag.py`, `POST /ask`, Q6 refusal, `eval/eval_set.json` (15 rows), Winner Table | `[x] CLOSED` | `119a994` |
| **D9** | Tue 17 Nov | Agent Tools & LangGraph Approval Step | `app/tools.py` (45 hrs/cr, 70:30 score), `app/agent_loop.py`, `app/graph.py`, `POST /agent` | `[x] CLOSED` | `218aa7f` |
| **D10** | Wed 18 Nov | Streamlit UI & Credit Progress Bar | `ui/app.py`, color-coded progress bar toward 14–20 credits, thumbs feedback, UI screenshot | `[x] CLOSED` | `checkpoint-2` |
| **D11** | Thu 19 Nov | Pytest Suite, Ruff Linting & Docker | `tests/` (17 tests), `ruff.toml` (0 errors), `Dockerfile`, `docker-compose.yml` | `[x] CLOSED` | `fa39170` |
| **D12** | Fri 20 Nov | GitHub Actions CI & Cloud Deployment | `.github/workflows/ci.yml`, PR merge, `render.yaml`, live public deployment | `[x] CLOSED` | `8b92a3f` |
| **D13** | Sat 21 Nov | Production Hardening, Cache & Security | In-memory cache (<2ms), token/latency logging, prompt injection defense, `docs/resume.md` | `[x] CLOSED` | `859bc37` |
| **D14** | Mon 23 Nov | Capstone Release & Interview Guide | `docs/interview.md` (60s pitch, 10 Q&As, hardest problem story), demo rehearsal, final tag | `[x] CLOSED` | `final` |

---

## Detailed Milestone Verification Logs

### Day 1–3: Data Foundation & Document Ingestion
- [x] Defined target user persona: Third-year E&TC student with mixed industrial and rural NSS activities.
- [x] Sourced authentic regulatory documents from AICTE and UGC.
- [x] Parsed unstructured PDF tables using `pdfplumber` with robust `try/except` fallbacks, converting policy rules into structured `data/records.json`.

### Day 4–6: API Gateway & Semantic Foundations
- [x] Built FastAPI gateway exposing `/health`, `/records`, and `/search`.
- [x] Tagged **`checkpoint-1`** and **`week-1`**.
- [x] Validated TF-IDF search indexing and keyword matching across internship activities.

### Day 7–8: RAG Engine, Chroma Vectorstore & Benchmark
- [x] Partitioned policy documents into 346 semantic chunks preserving `source`, `page`, and `title`.
- [x] Indexed chunks into persistent Chroma vectorstore (`data/chroma`).
- [x] Built `app/rag.py` delivering grounded answers with formatted citations (`[source, Page X]`).
- [x] Enforced 100% precision out-of-scope refusal on Question 6 (Pune IT companies).
- [x] Benchmarked Config A vs. Config B on 15 ground-truth questions; embedded Winner Table in `README.md`.

### Day 9–10: Agentic Workflows & Streamlit Dashboard
- [x] Engineered `internship_credit_calculator` in `app/tools.py` executing deterministic credit conversion (1 credit = 45 hours) and AICTE dual evaluation (70% industry + 30% panel).
- [x] Developed LangGraph state machine with `MemorySaver` checkpointer and an academic mentor approval gate.
- [x] Launched Streamlit UI (`ui/app.py`) featuring the signature color-coded progress bar toward the 14–20 credit (630–900 hour) requirement.
- [x] Added interactive 👍 / 👎 thumbs feedback saved to `data/feedback.json`.
- [x] Tagged **`checkpoint-2`**.

### Day 11–12: Testing, Dockerization & CI/CD Pipeline
- [x] Created comprehensive Pytest suite and achieved 0 errors on `ruff check .`.
- [x] Built production `Dockerfile`, `.dockerignore`, and `docker-compose.yml`.
- [x] Configured GitHub Actions CI pipeline in `.github/workflows/ci.yml`.
- [x] Merged pull request from feature branch `feature/day-12-ci-and-deployment` with green CI.
- [x] Deployed live on Render with public `/health` and live UI.

### Day 13–14: Hardening, Capstone Polish & Final Release
- [x] Implemented in-memory caching reducing repeat question latency from 243.69 ms to 1.25 ms.
- [x] Integrated token estimation and latency logging to `data/telemetry.log`.
- [x] Implemented input length limits (1,000 chars) and prompt-injection defense with 100% block rate.
- [x] Created `docs/resume.md` with 3 STAR-formatted resume bullets.
- [x] Created `docs/interview.md` containing the 60-second pitch, 10 likely questions, and the hardest problem interview story.
- [x] Rehearsed live demo twice with zero defects.
- [x] Released final capstone tagged as **`final`**.
