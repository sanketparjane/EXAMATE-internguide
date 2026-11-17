# Day_9/app_agent_loop.py
"""
Day 9 Hand-written Agent Loop entry point for InternGuide.
Imports and exposes run_agent_handwritten and agent_loop from app.agent_loop.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.agent_loop import run_agent_handwritten, agent_loop

if __name__ == "__main__":
    print("Testing Day 9 Hand-written Agent Loop:")
    q = "I completed a 90-hour industry internship with 9/10 from company and 6/10 from panel. Calculate credits and net score."
    print("\nQuery:", q)
    res = run_agent_handwritten(q)
    print("Tools Used:", res["tools_used"])
    print("Answer:\n", res["answer"])
