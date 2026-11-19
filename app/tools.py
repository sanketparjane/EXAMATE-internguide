# app/tools.py
"""
InternGuide Agent Tools for Day 9.

Implements:
1. internship_credit_calculator:
   - Converts hours to credits (1 credit = 45 hours)
   - Computes AICTE internship score:
     * per-activity marks = 70% industry + 30% institute panel
     * net score = hours-weighted average of activity marks
2. rag_search:
   - Grounded knowledge retrieval over InternGuide policy documents
3. Function declarations and schemas for LLM tool calling.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.rag import ask as rag_ask


def internship_credit_calculator(
    activities: Optional[List[Dict[str, Any]]] = None,
    hours: Optional[float] = None,
    industry_score: Optional[float] = None,
    institute_panel_score: Optional[float] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Converts internship hours to credits (1 credit = 45 hours) and computes the
    AICTE internship score:
      - per-activity marks = 70% industry + 30% institute panel
      - net score = hours-weighted average of activity marks

    Args:
      activities: List of activity dictionaries, each containing:
                  - 'title' or 'name': str
                  - 'hours': float/int
                  - 'industry_score': float/int (out of 10 or 100)
                  - 'institute_panel_score': float/int (out of 10 or 100)
      hours: Single activity hours (if activities list not passed)
      industry_score: Single activity industry score
      institute_panel_score: Single activity institute panel score

    Returns:
      Dictionary containing per-activity credits, marks, total credits, and net score.
    """
    parsed_activities = []

    # Case 1: activities passed as a list
    if activities and isinstance(activities, list):
        for idx, act in enumerate(activities):
            h = float(act.get("hours", act.get("total_hours", 0.0)))
            ind = float(act.get("industry_score", act.get("industry_marks", act.get("industry", 0.0))))
            inst = float(act.get("institute_panel_score", act.get("institute_score", act.get("panel_score", 0.0))))
            title = act.get("title", act.get("name", f"Activity {idx + 1}"))

            # per-activity marks = 70% industry + 30% institute panel
            act_marks = round((0.70 * ind) + (0.30 * inst), 2)
            # 1 credit = 45 hours
            act_credits = round(h / 45.0, 2)

            parsed_activities.append({
                "title": title,
                "hours": h,
                "credits": act_credits,
                "industry_score": ind,
                "institute_panel_score": inst,
                "activity_marks": act_marks
            })

    # Case 2: single activity passed via scalar arguments
    elif hours is not None:
        h = float(hours)
        ind = float(industry_score or kwargs.get("industry_marks", 0.0))
        inst = float(institute_panel_score or kwargs.get("institute_score", kwargs.get("panel_score", 0.0)))
        title = kwargs.get("title", "Internship Activity")

        act_marks = round((0.70 * ind) + (0.30 * inst), 2)
        act_credits = round(h / 45.0, 2)

        parsed_activities.append({
            "title": title,
            "hours": h,
            "credits": act_credits,
            "industry_score": ind,
            "institute_panel_score": inst,
            "activity_marks": act_marks
        })

    if not parsed_activities:
        return {
            "error": "No valid activities or hours provided for credit calculation.",
            "total_hours": 0.0,
            "total_credits": 0.0,
            "net_score": 0.0
        }

    total_hours = sum(a["hours"] for a in parsed_activities)
    # 1 credit = 45 hours
    total_credits = round(total_hours / 45.0, 2)

    # net score = hours-weighted average of activity marks
    if total_hours > 0:
        weighted_sum = sum(a["activity_marks"] * a["hours"] for a in parsed_activities)
        net_score = round(weighted_sum / total_hours, 2)
    else:
        net_score = 0.0

    return {
        "status": "success",
        "conversion_standard": "1 credit = 45 hours",
        "formula": "per-activity marks = 70% industry + 30% institute panel; net score = hours-weighted average",
        "activities": parsed_activities,
        "total_hours": total_hours,
        "total_credits": total_credits,
        "net_score": net_score,
        "summary": (
            f"Total Internship Hours: {total_hours} hrs -> Total Credits Earned: {total_credits} credits "
            f"(1 credit = 45 hours). Net AICTE Weighted Score: {net_score}/10."
        )
    }


def rag_search(query: str) -> Dict[str, Any]:
    """
    Search InternGuide knowledge base and policy documents using the RAG pipeline.
    Answers AICTE internship rules and PMIS eligibility with citations.
    """
    return rag_ask(query)


# Tool registry for dynamic tool invocation
tool_registry = {
    "internship_credit_calculator": internship_credit_calculator,
    "rag_search": rag_search
}

if __name__ == "__main__":
    print("Testing internship_credit_calculator with 2 activities:")
    sample_activities = [
        {
            "title": "Industrial Software Internship",
            "hours": 90,
            "industry_score": 9.0,
            "institute_panel_score": 6.0
        },
        {
            "title": "Rural NSS / Community Project",
            "hours": 45,
            "industry_score": 8.0,
            "institute_panel_score": 7.0
        }
    ]
    res = internship_credit_calculator(activities=sample_activities)
    print("Result:")
    print(res["summary"])
    print("Activities:", res["activities"])
    print("Total Credits:", res["total_credits"])
    print("Net Score:", res["net_score"])
