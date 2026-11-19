# Day_9/app_graph.py
"""
Day 9 LangGraph Agent with Memory & One Approval Step entry point for InternGuide.
Imports and exposes run_langgraph_agent and build_agent_graph from app.graph.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.graph import run_langgraph_agent

if __name__ == "__main__":
    print("Testing Day 9 LangGraph Agent (With Memory & Approval Step):")
    q = "Calculate credits and net score for 90 hours with 9 industry score and 6 panel score."
    print("\nQuery:", q)
    res = run_langgraph_agent(q, session_id="cli_demo", approved=True)
    print("Approval Status:", res["approval_status"])
    print("Tools Used:", res["tools_used"])
    print("Response:\n", res["response"])
