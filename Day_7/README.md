# Day 7: Document Chunking, ChromaDB Vectorstore & Semantic Search

## Overview
Day 7 implements the retrieval foundation for InternGuide:
1. **Document Chunking (`app/chunking.py`):** Parses raw policy PDFs (`data/raw/`) and curated rules (`data/records.json`) into 346 semantic passages while preserving essential metadata (`source`, `page`, `title`).
2. **Persistent Vectorstore (`app/vectorstore.py`):** Indexes all chunks into a local, persistent ChromaDB collection (`data/chroma`).
3. **Semantic Search & Evaluation (`app/embed.py`):** Evaluates semantic retrieval on the 10 official InternGuide questions and logs the results in `eval/search_results.md`.
4. **FastAPI Semantic Search API (`GET /search/semantic?q=`):** Exposes semantic query capability over the indexed vectorstore.

---

## Deliverables Summary

| Component | Path | Description |
|---|---|---|
| **Chunking Engine** | [`app/chunking.py`](../app/chunking.py) | Chunks PDF & JSON documents, attaching `source`, `page`, and `title`. |
| **Chroma Vectorstore** | [`app/vectorstore.py`](../app/vectorstore.py) | Manages persistent Chroma collection (`data/chroma`), batch upsert, and similarity querying. |
| **Embedding & Evaluation** | [`app/embed.py`](../app/embed.py) | Evaluates semantic retrieval across the 10 user questions. |
| **Evaluation Report** | [`eval/search_results.md`](../eval/search_results.md) | Ground-truth hit analysis with source pages, similarity scores, and text snippets. |
| **FastAPI Semantic Endpoint** | [`Day_4/app_main.py`](../Day_4/app_main.py) & [`app/main.py`](../app/main.py) | `GET /search/semantic?q=` returning top ranked chunks. |

---

## Metadata Schema
Each chunk stored in the Chroma collection includes:
- `id`: Unique identifier (e.g., `internship_doc_1_p7_c1`, `record_5`)
- `text`: Chunk text snippet (approx. 400–600 chars with 100-char overlap)
- `metadata`:
  - `source`: File path or document name (`internship_doc_1.pdf`, `records.json`)
  - `page`: 1-based page number (integer)
  - `title`: Document or section title
  - `chunk_index`: Sequence number within the page/record

---

## How to Test

### 1. Run Semantic Search Evaluation
```bash
python app/embed.py
```
This inspects the persistent Chroma store, evaluates all 10 questions, and writes `eval/search_results.md`.

### 2. Test the API Server
Start the Uvicorn server:
```bash
python -m uvicorn Day_4.app_main:app --reload
```

Query the semantic search endpoint:
```bash
curl "http://127.0.0.1:8000/search/semantic?q=How%20many%20hours%20is%20one%20internship%20credit%20as%20per%20AICTE%3F"
```

Response JSON snippet:
```json
[
  {
    "id": "internship_doc_1_p7_c1",
    "source": "internship_doc_1.pdf",
    "page": 7,
    "title": "AICTE Internship Policy: Guidelines & Procedures (2019)",
    "distance": 0.3429,
    "similarity_score": 0.7447,
    "text": "CHAPTER - 2 AICTE GUIDELINES FOR ORGANIZING INTERNSHIP..."
  }
]
```
