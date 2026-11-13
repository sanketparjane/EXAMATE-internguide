# Day 6: LLM Integration & Prompt Engineering

## What was built

| File | Purpose |
|---|---|
| `app/llm.py` | Gemini provider wrapper (`ask()` function) with retry + model fallback |
| `Day_4/app_main.py` | Added `POST /chat` endpoint using `app/llm.py` |
| `prompts/system_prompt.md` | InternGuide system prompt (role, rules, response format) |
| `prompts/task_prompt_v1.md` | V1: Direct answer mode (concise, rule-first) |
| `prompts/task_prompt_v2.md` | V2: Mentor mode (explain + calculate + next steps) |
| `eval/prompt_compare.md` | Comparison of V1 vs V2 on all 10 test questions |
| `.env.example` | Template for API key (committed; actual `.env` NOT committed) |

## Setup

```bash
# 1. Copy and fill in your key
cp .env.example .env
# Edit .env and set: GEMINI_API_KEY=your_actual_key

# 2. Run the API
python -m uvicorn Day_4.app_main:app --reload
```

## Test the /chat endpoint

```bash
# Using curl
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How many hours is one internship credit as per AICTE?"}'
```

Expected response:
```json
{
  "answer": "As per AICTE Internship Policy 2019, 1 credit = 30 hours...",
  "confidence": "high",
  "follow_up": "What is the minimum credit requirement for a B.Tech internship?",
  "model_used": "gemini-3.8-flash"
}
```

## Key Design Decisions

- **`.env` NOT committed** — API key stays secret; `.env.example` documents the format
- **Model fallback chain** — tries gemini-3.8-flash → 3.7 → 3.6 → 3.5 on 503 errors
- **Structured JSON output** — `/chat` always returns `answer`, `confidence`, `follow_up`
- **V2 prompt wins** — mentor mode better serves confused students (see `eval/prompt_compare.md`)
