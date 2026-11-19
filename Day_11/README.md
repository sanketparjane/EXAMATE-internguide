# Day 11: Pytest Test Suite, Ruff Linting & Dockerization

## Overview
Day 11 implements comprehensive testing, linting compliance, and multi-service containerization for InternGuide:
1. **Pytest Test Suite (`tests/`):**
   - 17 unit and integration tests covering all core system components:
     * **Health & Records:** `/health`, `/records`, `/records/{id}`, and 404 validation.
     * **Search Systems:** Keyword TF-IDF search (`/search`) and Chroma persistent vectorstore semantic retrieval (`/search/semantic`).
     * **RAG Pipeline (`/ask`):** Grounded question answering with citations, fake LLM mocking, and strict Q6 out-of-scope refusal (*"I don't know based on the provided information"*).
     * **Agent Tools:** `internship_credit_calculator` (1 credit = 45 hours, 70% industry + 30% panel marks, hours-weighted net score), and `rag_search`.
     * **LangGraph Agent Workflow:** `/agent` endpoint testing with memory and approval step authorization.
2. **Ruff Linter Compliance:**
   - Full repository complies with `ruff check .` with **0 errors**.
3. **Containerization:**
   - `Dockerfile`, `.dockerignore`, and `docker-compose.yml` to orchestrate both the FastAPI API and the Streamlit UI in isolated containers.
4. **README Documentation:**
   - Detailed instructions under **Run with Docker**.

---

## Deliverables Summary

| Component | Path | Description |
|---|---|---|
| **Test Suite** | [`tests/`](../tests/) | 17 pytest tests across all API endpoints, tools, and workflows. |
| **Linter Configuration** | [`ruff.toml`](../ruff.toml) | Configured rules ensuring clean, warning-free code. |
| **Test Runner** | [`Day_11/run_tests.py`](./run_tests.py) | Automated script running `ruff check .` and `pytest -v`. |
| **Dockerfile** | [`Dockerfile`](../Dockerfile) | Python 3.11-slim container building API and UI. |
| **Docker Ignore** | [`.dockerignore`](../.dockerignore) | Excludes venvs, caches, and unnecessary artifacts from container build. |
| **Docker Compose** | [`docker-compose.yml`](../docker-compose.yml) | Orchestrates `api` (port 8000) and `ui` (port 8501) with health checks. |

---

## Pytest Test Results (17/17 Passed)

```text
tests/test_agent_tools.py::test_credit_calculator_conversion_45_hours PASSED
tests/test_agent_tools.py::test_credit_calculator_evaluation_marks_70_30 PASSED
tests/test_agent_tools.py::test_credit_calculator_net_hours_weighted_score PASSED
tests/test_agent_tools.py::test_credit_calculator_empty_input PASSED
tests/test_agent_tools.py::test_rag_search_tool PASSED
tests/test_agent_workflow.py::test_agent_endpoint_approved PASSED
tests/test_agent_workflow.py::test_agent_endpoint_rejection_step PASSED
tests/test_ask_rag.py::test_ask_endpoint_with_fake_llm PASSED
tests/test_ask_rag.py::test_ask_out_of_scope_q6_refusal PASSED
tests/test_ask_rag.py::test_ask_missing_input_validation PASSED
tests/test_health_and_records.py::test_health_endpoint PASSED
tests/test_health_and_records.py::test_records_list_endpoint PASSED
tests/test_health_and_records.py::test_records_limit_parameter PASSED
tests/test_health_and_records.py::test_record_by_id_success PASSED
tests/test_health_and_records.py::test_record_by_id_not_found PASSED
tests/test_search.py::test_keyword_search PASSED
tests/test_search.py::test_semantic_search PASSED

============================= 17 passed in 1.40s ==============================
```

---

## Run with Docker

To run both the InternGuide FastAPI API and Streamlit UI in Docker containers:

### 1. Build and Start Services
```bash
docker compose up --build
```

### 2. Access the Application
- **FastAPI Interactive API Documentation:** [`http://localhost:8000/docs`](http://localhost:8000/docs)
- **FastAPI Health Endpoint:** [`http://localhost:8000/health`](http://localhost:8000/health)
- **Streamlit Web Application & Progress Bar:** [`http://localhost:8501`](http://localhost:8501)

### 3. Stop Services
```bash
docker compose down
```

---

## How to Run Tests Locally

```bash
# Run the combined test & lint runner
python Day_11/run_tests.py

# Or run pytest directly
pytest -v

# Or run ruff linter directly
ruff check .
```
