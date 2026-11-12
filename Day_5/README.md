# Day 5: How LLMs Work & Checkpoint 1

## 1. Documentation Created
- [`docs/how_llms_work.md`](docs/how_llms_work.md): Explains how Large Language Models work (tokenization, Transformer attention layers, next-token prediction), includes the basic architecture diagram, and lists 10 real InternGuide test questions.

## 2. Checkpoint 1: Run FastAPI & Explain a Function

### Run the Server
From the project root (`EXAMATE-internguide`), run:

```bash
uvicorn Day_4.app_main:app --reload
```

If `uvicorn` is not recognized on your PATH, use:

```bash
python -m uvicorn Day_4.app_main:app --reload
```

Then open Swagger UI in your browser at:
`http://127.0.0.1:8000/docs`

### Explain One Function (`/search` endpoint from Day 4)
> "The `search` function (`GET /search` in `Day_4/app_main.py`) takes a user's text query `q` and passes it to our `search_records` logic in `Day_4/app_smart_search.py`. It uses TF-IDF (`TfidfVectorizer`) to convert the internship rule records (`activity_head`, `sub_activity`, `evidence_document`) and the query into numerical vectors, calculates the cosine similarity between them, and returns the matching records ranked by `relevance_score` (filtering out scores <= 0.05)."

## 3. Commit and Tag Checkpoint-1
Run these Git commands from the project root when you are ready:

```bash
git add Day_5/
git commit -m "day-05: added how llms work doc and 10 test questions"
git push origin main
git tag checkpoint-1
git push origin checkpoint-1
```
