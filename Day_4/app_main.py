from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from Day_4.app_smart_search import search_records
from app.llm import ask

app = FastAPI(title="InternGuide API")

def load_data():
    with open('data/records.json', 'r') as f:
        return json.load(f)

class QuestionModel(BaseModel):
    user_id: str
    query: str

class ChatRequest(BaseModel):
    question: str

@app.get("/health")
def health_check():
    return {"status": "ok", "project": "InternGuide"}

@app.get("/records")
def get_records(limit: int = 10):
    records = load_data()
    return records[:limit]

@app.get("/records/{record_id}")
def get_record(record_id: int):
    records = load_data()
    for r in records:
        if r.get('id') == record_id:
            return r
    raise HTTPException(status_code=404, detail="Record not found")

@app.get("/search")
def search(q: str):
    results = search_records(q)
    return results

@app.get("/search/semantic")
def search_semantic(q: str, limit: int = 5):
    """
    Perform semantic search over chunked InternGuide documents in persistent Chroma vectorstore.
    Returns: list of matching chunks with source, page, title, and similarity score.
    """
    from app.embed import semantic_search
    results = semantic_search(q, top_k=limit)
    return results

@app.post("/questions")
def post_question(question: QuestionModel):
    return {
        "message": "Question received successfully",
        "user": question.user_id,
        "query": question.query
    }

@app.post("/chat")
def chat(request: ChatRequest):
    """
    Send a question to InternGuide AI (Gemini).
    Returns: answer, confidence, follow_up
    """
    result = ask(request.question)
    return result
