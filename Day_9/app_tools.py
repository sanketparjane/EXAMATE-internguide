# Day_9/app_tools.py
"""
Day 9 Agent Tool entry point for InternGuide.
Imports and exposes internship_credit_calculator and rag_search from app.tools.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.tools import internship_credit_calculator

if __name__ == "__main__":
    print("Testing Day 9 Agent Tool: internship_credit_calculator")
    sample_activities = [
        {
            "title": "Industrial Internship",
            "hours": 90,
            "industry_score": 9.0,
            "institute_panel_score": 6.0
        },
        {
            "title": "Rural NSS Camp",
            "hours": 45,
            "industry_score": 8.0,
            "institute_panel_score": 7.0
        }
    ]
    res = internship_credit_calculator(activities=sample_activities)
    print("Summary:", res["summary"])
    print("Total Credits (1 credit = 45 hours):", res["total_credits"])
    print("Net Score (70% industry + 30% panel, hours-weighted):", res["net_score"])
