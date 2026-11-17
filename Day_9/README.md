# Day 9: Agent Tools, Hand-written Loop & LangGraph with Memory + Approval Step

## Overview
Day 9 advances InternGuide into an autonomous agent system featuring:
1. **Agent Tools (`app/tools.py` & `Day_9/app_tools.py`):**
   - `internship_credit_calculator`: Converts internship hours to credits (**1 credit = 45 hours**) and calculates AICTE evaluation scores:
     * **Per-activity marks:** $70\% \text{ industry} + 30\% \text{ institute panel}$
     * **Net score:** Hours-weighted average of activity marks across all completed internships.
   - `rag_search`: Semantic retrieval over AICTE and PMIS policy documents with citations.
2. **Hand-written Agent Loop (`app/agent_loop.py` & `Day_9/app_agent_loop.py`):**
   - Think-Act-Observe reasoning loop.
   - Dynamically determines intent (Calculation vs. Policy Search vs. Compound queries).
   - Coordinates tool calls and synthesizes unified responses.
3. **LangGraph Agent with Memory & Approval Step (`app/graph.py` & `Day_9/app_graph.py`):**
   - Rebuilt as a state machine using LangGraph (`StateGraph`).
   - **One Mandatory Approval Step:** Human-in-the-loop / Faculty Mentor authorization gate required before formal credit conversion and grade generation.
   - **Conversation Memory:** Persistent multi-turn memory using `MemorySaver` indexed by `session_id` (`thread_id`).
4. **FastAPI Agent Endpoint (`POST /agent`):**
   - Exposed in both `app/main.py` and `Day_4/app_main.py`.
   - Accepts prompt/query, optional activity list, session identifier, and approval flag.

---

## Deliverables Summary

| Component | Path | Description |
|---|---|---|
| **Agent Tools** | [`app/tools.py`](../app/tools.py) / [`Day_9/app_tools.py`](./app_tools.py) | Implements `internship_credit_calculator` (45 hrs/credit, 70:30 ratio) and `rag_search`. |
| **Hand-written Agent Loop** | [`app/agent_loop.py`](../app/agent_loop.py) / [`Day_9/app_agent_loop.py`](./app_agent_loop.py) | Custom loop orchestrating RAG search and credit calculator. |
| **LangGraph Agent** | [`app/graph.py`](../app/graph.py) / [`Day_9/app_graph.py`](./app_graph.py) | StateGraph with memory checkpointer and an approval step node. |
| **FastAPI Agent Endpoint** | [`app/main.py`](../app/main.py) / [`Day_4/app_main.py`](../Day_4/app_main.py) | `POST /agent` endpoint for interactive multi-turn agent querying. |

---

## Formula & Calculation Logic

### 1. Credit Conversion
$$\text{Credits Earned} = \frac{\text{Total Internship Hours}}{45}$$

### 2. Per-Activity Marks
$$\text{Activity Marks} = (0.70 \times \text{Industry Score}) + (0.30 \times \text{Institute Panel Score})$$

### 3. Net Weighted Score
$$\text{Net Score} = \frac{\sum (\text{Activity Marks}_i \times \text{Hours}_i)}{\sum \text{Hours}_i}$$

#### Example:
- **Activity 1:** 90 hours, Industry = 9.0/10, Panel = 6.0/10
  $$\text{Marks}_1 = (0.7 \times 9.0) + (0.3 \times 6.0) = 6.3 + 1.8 = 8.1/10$$
  $$\text{Credits}_1 = 90 / 45 = 2.0\text{ credits}$$
- **Activity 2:** 45 hours, Industry = 8.0/10, Panel = 7.0/10
  $$\text{Marks}_2 = (0.7 \times 8.0) + (0.3 \times 7.0) = 5.6 + 2.1 = 7.7/10$$
  $$\text{Credits}_2 = 45 / 45 = 1.0\text{ credit}$$
- **Net Calculation:**
  $$\text{Total Hours} = 135\text{ hrs} \implies \text{Total Credits} = 3.0\text{ credits}$$
  $$\text{Net Score} = \frac{(8.1 \times 90) + (7.7 \times 45)}{135} = \frac{729 + 346.5}{135} = \frac{1075.5}{135} \approx 7.97/10$$

---

## LangGraph Architecture (Memory + Approval Step)

```
[START]
   │
   ▼
[agent_node] ──(needs approval: credit calculation)──► [approval_node]
   │                                                         │
   │ (in-scope RAG query)                 (approved)         │ (rejected)
   │                                           ▼             ▼
   └────────────────────────────────────► [tools_node]    [synthesize_node] (Action Blocked)
                                               │                 │
                                               ▼                 ▼
                                        [synthesize_node] ────► [END]
```

- **Memory Checkpointer:** Uses `MemorySaver()` with `thread_id` to maintain context across multi-turn queries.
- **One Approval Step:** Evaluates authorization status (`approved=True` vs. `approved=False`). Rejection halts execution and outputs an action-blocked message.

---

## Verification & Testing

### 1. Test Tools Directly
```bash
python Day_9/app_tools.py
```

### 2. Test Hand-written Agent Loop
```bash
python Day_9/app_agent_loop.py
```

### 3. Test LangGraph Agent with Approval Step
```bash
python Day_9/app_graph.py
```

### 4. Test `POST /agent` API Endpoint
Start the server:
```bash
python -m uvicorn Day_4.app_main:app --reload
```

#### Query 1: Credit Calculation with Approval
```bash
curl -X POST "http://127.0.0.1:8000/agent" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "Calculate my credits: 90 hours with 9 industry score and 6 panel score, plus 45 hours with 8 industry and 7 panel.",
       "session_id": "student_sanket",
       "approved": true
     }'
```

#### Query 2: Policy Search via Agent
```bash
curl -X POST "http://127.0.0.1:8000/agent" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "Does an online internship count for AICTE internship credits?",
       "session_id": "student_sanket"
     }'
```
