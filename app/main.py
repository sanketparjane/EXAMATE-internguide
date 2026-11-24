# app/main.py
"""
FastAPI application for InternGuide API.
Exposes endpoints for records, keyword search, Gemini chat, and Chroma semantic search.
"""

from pathlib import Path
import sys
import json
from typing import Optional, List, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Day_4.app_smart_search import search_records
from app.llm import ask
from app.embed import semantic_search

app = FastAPI(title="InternGuide API")

def load_data():
    records_file = PROJECT_ROOT / "data" / "records.json"
    with open(records_file, "r", encoding="utf-8") as f:
        return json.load(f)

class QuestionModel(BaseModel):
    user_id: str
    query: str

class ChatRequest(BaseModel):
    question: str

class AskRequest(BaseModel):
    question: Optional[str] = None
    query: Optional[str] = None
    prompt: Optional[str] = None

class AgentRequest(BaseModel):
    query: Optional[str] = None
    question: Optional[str] = None
    prompt: Optional[str] = None
    session_id: Optional[str] = "default_session"
    approved: Optional[bool] = True
    activities: Optional[List[Dict[str, Any]]] = None

@app.get("/")
def root():
    return {
        "message": "Welcome to InternGuide API",
        "docs": "/docs",
        "health": "/health",
        "records": "/records",
        "status": "running"
    }

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
        if r.get("id") == record_id:
            return r
    raise HTTPException(status_code=404, detail="Record not found")

@app.get("/search")
def search(q: str):
    """Keyword search using TF-IDF and cosine similarity."""
    results = search_records(q)
    return results

@app.get("/search/semantic")
def search_semantic(q: str, limit: int = 5):
    """
    Perform semantic search over chunked InternGuide documents in persistent Chroma vectorstore.
    Returns: list of matching chunks with source, page, title, and similarity score.
    """
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

@app.post("/ask")
def ask_rag_endpoint(request: AskRequest):
    """
    RAG endpoint: answers InternGuide questions from retrieved chunks with citations.
    Must say 'I don't know' for Q6 and out-of-scope queries.
    Enforces input length limits, prompt-injection defense, and caching.
    """
    q = request.question or request.query or request.prompt
    if not q:
        raise HTTPException(status_code=400, detail="Question, query, or prompt is required")
    from app.security import validate_input_length
    is_valid, err_msg = validate_input_length(q)
    if not is_valid:
        raise HTTPException(status_code=400, detail=err_msg)
    from app.rag import ask as rag_ask
    return rag_ask(q)

@app.post("/agent")
def agent_endpoint(request: AgentRequest):
    """
    Day 9 Agent endpoint:
    Runs the LangGraph agent with memory and one approval step.
    Orchestrates RAG search and internship_credit_calculator (1 credit = 45 hours, 70% industry + 30% panel).
    """
    q = request.query or request.question or request.prompt
    if not q and not request.activities:
        raise HTTPException(status_code=400, detail="Query, question, prompt, or activities list is required")
    if q:
        from app.security import validate_input_length
        is_valid, err_msg = validate_input_length(q)
        if not is_valid:
            raise HTTPException(status_code=400, detail=err_msg)
    from app.graph import run_langgraph_agent
    res = run_langgraph_agent(
        query=q or "Calculate internship credits and score",
        session_id=request.session_id or "default_session",
        approved=True if request.approved is None else request.approved,
        activities=request.activities
    )
    return res
