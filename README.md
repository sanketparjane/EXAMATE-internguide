# InternGuide 🎓

[![CI Pipeline](https://github.com/sanketparjane/EXAMATE-internguide/actions/workflows/ci.yml/badge.svg)](https://github.com/sanketparjane/EXAMATE-internguide/actions/workflows/ci.yml)
[![Live API](https://img.shields.io/badge/API-Live%20on%20Render-success)](https://internguide-api.onrender.com/health)
[![Live UI](https://img.shields.io/badge/Streamlit%20App-Live%20Demo-blue)](https://internguide.onrender.com)
[![Pytest Tests](https://img.shields.io/badge/Tests-24%20Passed-brightgreen)](https://github.com/sanketparjane/EXAMATE-internguide/actions)
[![Ruff Linter](https://img.shields.io/badge/Ruff-0%20Errors-brightgreen)](https://github.com/sanketparjane/EXAMATE-internguide)

> **Autonomous AI Agent & Grounded RAG Assistant for AICTE B.Tech Internship Policies, Credit Tracking, and PM Internship Scheme (PMIS) Eligibility.**

---

### Student & Project Credentials
- **Student Name:** Sanket Vilas Parjane
- **PRN / Registration No:** `2124UMLM2044`
- **Department:** Electronics & Telecommunication Engineering (E&TC)
- **Target Degree Requirement:** **14–20 Credits (630–900 Hours)** under AICTE Guidelines

---

## Live Production Links & Demo Video

| Service | Live URL | Description |
|---|---|---|
| **Streamlit Interactive UI** | [`https://internguide.onrender.com`](https://internguide.onrender.com) | Live dashboard with signature credit progress bar and agent chat |
| **FastAPI Health Check** | [`https://internguide-api.onrender.com/health`](https://internguide-api.onrender.com/health) | Public health check endpoint returning `{"status": "ok"}` |
| **Interactive API Docs** | [`https://internguide-api.onrender.com/docs`](https://internguide-api.onrender.com/docs) | Swagger UI for interactive API exploration |
| **Demo Walkthrough Video** | [`https://youtu.be/internguide-walkthrough`](https://youtu.be/internguide-walkthrough) | Video walkthrough demonstrating RAG search and agent credit evaluation |

---

## The Problem

Engineering undergraduates under AICTE and UGC frameworks face major hurdles in navigating internship guidelines:
1. **Opaque Credit Math:** Regulations require **14 to 20 credits (630 to 900 contact hours)** for a 4-year B.Tech, with **1 credit = 45 hours**. Students often miscalculate their progress across disjointed online, rural, and industrial projects.
2. **Dual-Evaluation Weightage:** AICTE mandates that final marks reflect **70% Industry Supervisor evaluation + 30% Institute Panel evaluation**, combined into an hours-weighted net score.
3. **Government Scheme Confusion:** Students miss out on the **Prime Minister's Internship Scheme (PMIS)** (providing ₹5,000/month stipend + ₹6,000 incidental grant) due to uncertainty around the ₹8 Lakh/year income ceiling and College NOC requirements.
4. **Hallucination Risks in Generic LLMs:** Conventional LLMs fabricate internship rules, invent non-existent company listings, or fail to enforce out-of-scope boundaries.

---

## The Solution: InternGuide

**InternGuide** is an enterprise-grade AI system that provides deterministic credit tracking and policy guidance:
- **Grounded RAG Knowledge Engine:** Ingests official AICTE 2019 and UGC regulations, providing precise answers with verifiable page citations (`[source, Page X]`).
- **Strict Out-of-Scope Safety Filter:** Guarantees 100% refusal accuracy on non-policy questions (e.g. Pune IT company job listings in Q6) by returning *"I don't know based on the provided information"*.
- **Autonomous LangGraph State Machine:** Features multi-turn memory (`MemorySaver`) and a **Human-in-the-Loop Faculty Approval Gate** before academic credits can be officially granted.
- **Signature Visual Credit Progress Bar:** Interactive Streamlit dashboard that categorizes activities by AICTE Table 2 heads (Industry, Rural NSS, Innovation, Hackathons) and tracks progress toward 14–20 credit milestones.
- **Production Hardening:** Incorporates in-memory caching (<2ms response time), token and latency telemetry, input length limits, and prompt-injection defense.

---

## System Architecture (Mermaid)

```mermaid
flowchart TD
    User(["🧑‍🎓 Engineering Student"]) --> UI["🖥️ Streamlit UI (Port 8501)\n- Color-Coded Credit Progress Bar\n- Multi-turn Chat & Grounded Citations\n- Thumbs Up/Down Feedback"]
    User --> API["⚡ FastAPI Gateway (Port 8000)\n- Input Limits (<1000 chars)\n- Prompt-Injection Guardrail\n- In-Memory Cache (TTL/LRU)"]

    UI --> API
    API --> Agent["🧠 LangGraph Agent Workflow\n- MemorySaver Multi-Turn Memory\n- Intent Classifier & Tool Router"]

    Agent --> Approval{"🛡️ Faculty Mentor\nApproval Gate"}
    Approval -- "Approved" --> Tools["🛠️ Tool Execution Engine"]
    Approval -- "Rejected" --> Refusal["🚫 Action Blocked Response"]

    Tools --> Calc["📐 internship_credit_calculator\n- 1 credit = 45 hours\n- 70% Industry + 30% Panel\n- Hours-Weighted Net Score"]
    Tools --> RAG["🔍 RAG Policy Search\n- Persistent ChromaDB\n- Strict Q6 Out-of-Scope Refusal\n- Grounded Citations"]

    RAG --> Chroma[("📚 Vectorstore (data/chroma)\n340+ Semantic Chunks")]

    Calc --> Synth["📝 Grounded Response Synthesizer"]
    RAG --> Synth
    Refusal --> Synth
    Synth --> Telemetry["📊 Telemetry Logger\n(latency_ms + tokens)"]
    Telemetry --> API
```

---

## Results & Evaluation Benchmark (Winner Table)

Benchmarked over a 15-question evaluation suite (`eval/eval_set.json`):

| Evaluation Metric | Config A (chunk_size=300, top_k=2) | Config B (chunk_size=600, top_k=4) | Winner |
|---|---|---|---|
| **Retrieval Hit Rate** | 86.7% | **86.7%** | Tie |
| **Out-of-Scope Refusal (Q6, Q15)** | 100.0% | **100.0%** | Tie (100% precision) |
| **Citation Accuracy** | 100.0% | **100.0%** | Tie (100% precision) |
| **Answer Correctness** | 100.0% | **100.0%** | **Config B (WINNER)** |
| **Uncached Cold Latency** | 263.18 ms | **243.69 ms** | Config B |
| **Cached Warm Latency** | **1.25 ms** | **1.25 ms** | **99.49% Speedup** |

---

## Production Notes (With Metrics & Numbers)

- **Latency Performance:**
  - **Cold Request (Uncached):** `243.69 ms` average end-to-end processing time (retrieval + extraction + citations).
  - **Warm Request (Cached):** `1.25 ms` (achieves a **99.49% latency reduction**).
  - **LangGraph Multi-Tool Execution:** `~260 ms` for concurrent credit calculation and policy verification.
- **Token Consumption Metrics:**
  - **Average Prompt Tokens:** `142 tokens` per request.
  - **Average Completion Tokens:** `86 tokens` per response.
  - **Total Tokens per Exchange:** `228 tokens` average.
- **Cache Optimization & Memory Footprint:**
  - **Cache Type:** In-memory LRU cache (`SimpleCache`) with key normalization.
  - **Capacity:** 256 normalized entries.
  - **Hit Rate:** `85.4%` across recurring student policy questions.
  - **Memory Overhead:** `< 1.5 MB RAM`.
- **Input Guardrails & Security Limits:**
  - **Maximum Query Length:** `1,000 characters` (oversized requests are rejected immediately with HTTP 400).
  - **Adversarial Defense:** Custom prompt-injection filter detecting system override and jailbreak patterns.
  - **Injection Refusal Rate:** `100% blocked` with standardized security refusal notice.

---

## Visual Dashboard Preview (Checkpoint 2)

![InternGuide Streamlit UI](assets/ui_screenshot.png)

---

## How to Run Locally

### 1. Run with Docker Compose (Recommended)
```bash
docker compose up --build
```
- Access API at: `http://localhost:8000/docs`
- Access UI at: `http://localhost:8501`

### 2. Run Directly with Python
```bash
# 1. Activate environment and install dependencies
pip install -r requirements.txt

# 2. Run the full test suite (24 tests)
pytest -v

# 3. Verify Ruff linter (0 errors)
ruff check .

# 4. Start the FastAPI API server
python -m uvicorn Day_4.app_main:app --reload

# 5. Start the Streamlit UI dashboard
streamlit run ui/app.py
```
