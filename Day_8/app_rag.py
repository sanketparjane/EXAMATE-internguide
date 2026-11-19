# Day_8/app_rag.py
"""
Day 8 RAG pipeline entry point for InternGuide.
Imports and exposes the ask function and RAG pipeline from app.rag.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.rag import ask

if __name__ == "__main__":
    print("Testing Day 8 RAG Pipeline:")
    q1 = "How many hours is one internship credit as per AICTE?"
    print(f"\nQ1: {q1}")
    res1 = ask(q1)
    print("Answer:", res1["answer"])
    print("Citations:", res1["citations"])

    q6 = "Which specific IT companies in Pune are offering paid AI internships this summer?"
    print(f"\nQ6 (Out of scope refusal): {q6}")
    res6 = ask(q6)
    print("Answer:", res6["answer"])
    print("Citations:", res6["citations"])
