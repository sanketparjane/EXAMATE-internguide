# InternGuide — 15-Minute Capstone Presentation Guide

**Candidate:** Sanket Vilas Parjane  
**PRN / Registration No:** `2124UMLM2044`  
**Department:** Electronics & Telecommunication Engineering (E&TC)  
**Project Title:** InternGuide — Autonomous AI Agent & Grounded RAG Assistant for AICTE B.Tech Internship Regulations & Credit Tracking  
**Duration:** 15 Minutes Maximum  

---

## ⏱️ Presentation Timing Breakdown (15 Minutes)

| Step | Topic | Allotted Time | Key Focus |
|:---:|---|:---:|---|
| **1** | Problem Statement $\rightarrow$ Solution & Approach | 3 mins | Real student pain points & deterministic AI solution |
| **2** | Technologies Used | 2 mins | Full-stack AI agent ecosystem |
| **3** | Requirements & Dependencies | 1.5 mins | Key libraries, isolation & containerization |
| **4** | System Architecture & Diagram | 2.5 mins | Request lifecycle from UI to LangGraph agent |
| **5** | Code Walkthrough & Key Functionality | 3 mins | Tool calculation, grounded RAG & approval gate |
| **6** | Live Demonstration & Cloud URLs | 3 mins | Live UI progress bar, chat with citations & API docs |

---

## STEP 1: Problem Statement $\rightarrow$ Solution & Approach (3 Minutes)

### 📌 What to Say (Speaking Script):
> *"Good morning respected evaluators. As a B.Tech student, navigating AICTE and UGC internship guidelines is confusing and stressful. Every engineering graduate must complete between 14 to 20 credits (which translates to 630 to 900 hours). Students participate in fragmented activities—corporate internships, rural NSS camps, innovation hackathons—and have no transparent way to track their progress. Furthermore, AICTE mandates a strict dual-evaluation scheme: 70% marks from the industry supervisor and 30% from the institute panel, weighted by hours.*
>
> *Additionally, when students look into government schemes like the Prime Minister’s Internship Scheme (PMIS 2026), they get confused between old pilot schemes and official 2026 rules regarding stipends (₹5,000/month) and eligibility (₹8 Lakh income ceiling, College NOC).*
>
> *Generic LLMs hallucinate rules and make arithmetic errors when converting hours to credits. To solve this, I built **InternGuide**: an enterprise-grade AI system combining grounded Retrieval-Augmented Generation (RAG) with deterministic agent tools and a human-in-the-loop mentor approval gate."*

### 🔑 Key Slide Points:
1. **The Core Problem:**
   - **Credit Complexity:** 14–20 credits required (1 credit = 45 contact hours).
   - **Evaluation Weightage:** $70\%$ industry supervisor marks $+ 30\%$ institute faculty panel marks.
   - **Policy Ambiguity:** Obsolete pilot data vs. PMIS 2026 rules (₹5,000/mo stipend, ₹6,000 grant).
   - **LLM Hallucinations:** Probabilistic LLMs fail at precise arithmetic and invent company listings.
2. **The InternGuide Solution:**
   - **Deterministic Tools:** Python calculator computes credits and weighted scores with 100% mathematical precision.
   - **Grounded Policy RAG:** Ingests official AICTE 2019 and UGC regulations with page citations (`[source, Page X]`).
   - **Human-in-the-Loop Agent:** LangGraph state machine with an Academic Mentor approval step.
   - **Interactive UI:** Color-coded progress bar toward degree completion.

---

## STEP 2: Technologies Used (2 Minutes)

### 📌 What to Say:
> *"InternGuide is built on a modern, decoupled cloud architecture spanning full-stack Python, agent orchestration, vector storage, and DevOps."*

### 🛠️ Technology Stack Overview:
- **Backend Framework:** **FastAPI** (High-throughput asynchronous REST API with Pydantic validation).
- **Frontend Dashboard:** **Streamlit** (Interactive reactive UI with custom CSS and credit progress bar).
- **Agent Orchestration:** **LangGraph & LangChain** (Cyclic state machines, checkpoint memory with `MemorySaver`, tool calling).
- **Large Language Model:** **Google Gemini 2.5 Flash** (via `google-genai` SDK for reasoning & synthesis).
- **Vector Database:** **ChromaDB** (Persistent on-disk vector store with Cosine similarity indexing).
- **Embeddings:** **Google text-embedding-004** (768-dimensional dense vector embeddings).
- **Document Processing:** **pdfplumber** (High-fidelity tabular extraction from AICTE policy PDFs).
- **Testing & Quality:** **Pytest** (24 comprehensive unit/integration tests) & **Ruff** (PEP 8 linting, 0 errors).
- **Containerization & CI/CD:** **Docker & Docker Compose**, **GitHub Actions** (Automated CI pipeline).
- **Cloud Deployment:** **Render** (Production web services with continuous deployment).

---

## STEP 3: Requirements & Dependencies (1.5 Minutes)

### 📌 What to Say:
> *"The project is packaged cleanly with clear dependency isolation. We maintain zero version conflicts, pin core dependencies in `requirements.txt`, and containerize the entire stack with multi-stage Docker builds."*

### 📦 Key Dependencies (`requirements.txt`):
| Package Category | Key Packages | Role in InternGuide |
|---|---|---|
| **API & Web Server** | `fastapi==0.115.0`, `uvicorn==0.32.0`, `pydantic` | Exposes REST endpoints (`/health`, `/records`, `/ask`, `/agent`) |
| **User Interface** | `streamlit==1.40.0` | Powers the credit tracking dashboard & interactive chat |
| **Agent & LangGraph** | `langgraph==0.2.45`, `langchain-core==0.3.15` | Multi-turn memory state machine & faculty approval gate |
| **LLM & Embeddings** | `google-genai`, `langchain-google-genai` | Synthesizes grounded answers & generates vector embeddings |
| **Vector Database** | `chromadb==0.5.15` | Stores 346 semantic chunks of regulatory text |
| **PDF Extraction** | `pdfplumber==0.11.4` | Extracts tabular data from AICTE Internship Policy Table 2 |
| **DevOps & Testing** | `pytest==9.2.0`, `ruff==0.8.4` | Automated test suite and static code validation |

---

## STEP 4: System Architecture & Simple Diagram (2.5 Minutes)

### 📌 What to Say:
> *"Here is the request lifecycle. When an engineering student enters an internship query or portfolio hours in the Streamlit UI, the request passes through FastAPI security guardrails. If it is a repeat query, our in-memory cache responds in under 1 millisecond. Otherwise, the LangGraph agent evaluates the intent: policy questions are routed to our Chroma vectorstore for grounded citations, while credit evaluations are routed to our deterministic Python calculator. Before credits are recorded, a faculty approval gate verifies compliance."*

### 📐 Architecture Diagram:

```text
  🧑‍🎓 Engineering Student
            │
            ▼
┌────────────────────────────────────────────────────────┐
│  🖥️ Streamlit Frontend UI (Port 8501)                 │
│  • Credit Progress Bar toward 14-20 credits target    │
│  • Grounded Chat with Verified Citations               │
│  • Interactive 👍 / 👎 Feedback Capture                │
└───────────────────────────┬────────────────────────────┘
                            │ HTTP JSON Request
                            ▼
┌────────────────────────────────────────────────────────┐
│  ⚡ FastAPI Backend Gateway (Port 8000)                │
│  • Input Length Limiter (Max 1,000 characters)         │
│  • Prompt Injection & Jailbreak Defense Guardrail      │
│  • In-Memory Fast Cache (99.9% Latency Speedup, <1ms)  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  🤖 LangGraph Autonomous Agent State Machine           │
│  • Multi-turn Conversation Memory (MemorySaver)       │
│  • Conditional Tool Router:                            │
│    ├── 1. internship_credit_calculator (Deterministic) │
│    └── 2. rag_search (ChromaDB + Gemini Embeddings)    │
│  • 🛡️ Academic Mentor Human-in-the-Loop Approval Gate  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  📑 Grounded Output & Verified Citations               │
│  • Exact Credit Math (1 credit = 45 hours)             │
│  • Dual-source Net Score (70% Industry + 30% Panel)    │
│  • Dated Citations [internship_doc_1.pdf, Page 7]      │
└────────────────────────────────────────────────────────┘
```

---

## STEP 5: Main Code Walkthrough (3 Minutes)

Highlight the 4 most critical files in the project:

### 1. `app/tools.py` — Deterministic Credit Calculator (Zero Math Hallucination)
- **Rule:** $1\text{ credit} = 45\text{ hours}$. Degree target = 14 to 20 credits (630–900 hours).
- **Dual Evaluation:** $\text{Activity Marks} = (0.70 \times \text{Industry}) + (0.30 \times \text{Institute Panel})$.
- **Net Score:** $\sum(\text{Marks}_i \times \text{Hours}_i) / \sum \text{Hours}_i$.
```python
# app/tools.py
@tool
def internship_credit_calculator(activities: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_hours = sum(act.get("hours", 0.0) for act in activities)
    total_credits = round(total_hours / 45.0, 2)
    weighted_marks = sum(
        ((0.70 * act["industry_score"]) + (0.30 * act["institute_panel_score"])) * act["hours"]
        for act in activities
    )
    net_score = round(weighted_marks / total_hours, 2)
    return {"total_hours": total_hours, "credits": total_credits, "net_score": net_score}
```

### 2. `app/rag.py` — Grounded Retrieval with Citations & Refusal
- Retrieves top-$k$ chunks from ChromaDB.
- Enforces strict grounded answers with page numbers (`[source, Page X]`).
- Guarantees **100% precision refusal** for out-of-scope questions (e.g. Pune IT company job listings):
  `"I don't know based on the provided information."`

### 3. `app/graph.py` — LangGraph Agent with Mentor Approval Step
- Uses a cyclic state graph: `agent_node` $\rightarrow$ `tool_node` $\rightarrow$ `mentor_approval_node` $\rightarrow$ `END`.
- Persists session state across turns using `MemorySaver`.

### 4. `ui/app.py` — Streamlit Credit Progress Bar & Chat
- Visualizes credits against the 14–20 credit B.Tech requirement.
- Breaks down hours by AICTE Table 2 heads (Corporate, Rural NSS, Innovation, Virtual).
- Logs student feedback directly to `data/feedback.json`.

---

## STEP 6: Live Demonstration & Live Cloud URLs (3 Minutes)

### 🌐 Live Public Links:
1. **Interactive Streamlit Web Dashboard:**  
   👉 **[`https://internguide.onrender.com`](https://internguide.onrender.com)**  
   *(Local fallback: `http://localhost:8501`)*

2. **FastAPI Public API & Swagger Docs:**  
   👉 **[`https://internguide-api.onrender.com/docs`](https://internguide-api.onrender.com/docs)**  
   *(Local fallback: `http://127.0.0.1:8000/docs`)*

3. **Public Health Endpoint:**  
   👉 **[`https://internguide-api.onrender.com/health`](https://internguide-api.onrender.com/health)**  
   *(Returns `{"status": "ok", "project": "InternGuide"}`)*

### 🎬 What to Demonstrate Live (3-Step Walkthrough):

1. **Demonstration 1: Signature Credit Progress Bar**
   - Open the **Credit Progress Tracker** tab.
   - Show the 2 pre-loaded activities:
     - 90 hours in *Corporate Embedded Systems* (Industry: 9/10, Panel: 6/10)
     - 45 hours in *Rural NSS Community Camp* (Industry: 8/10, Panel: 7/10)
   - Point to the **Progress Bar**: `3.0 / 14.0 Credits (21.4%)` and **Net Score**: `7.97 / 10`.

2. **Demonstration 2: Grounded Policy RAG Query with Citations**
   - Click suggested question: *"How many hours is one internship credit as per AICTE?"*
   - Show the exact citation badge: `[internship_doc_1.pdf, Page 7]`.
   - Click the 👍 thumbs-up button to show feedback logging.

3. **Demonstration 3: Out-of-Scope Safety Defense (Question 6)**
   - Ask: *"Which specific IT companies in Pune are offering paid AI internships?"*
   - Show that InternGuide refuses hallucinating company lists:
     *"I don't know based on the provided information. InternGuide only covers AICTE internship rules and PMIS eligibility criteria."*

---

## 🎯 Wrap-Up Conclusion (15 Seconds)
> *"In conclusion, InternGuide transforms complex regulatory documents into an accountable, transparent, and deterministic advisory assistant for engineering students and faculty mentors. Thank you, and I am now ready for questions."*
