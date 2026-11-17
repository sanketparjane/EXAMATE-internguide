# app/agent_loop.py
"""
Hand-written Agent Loop for InternGuide (Day 9 - S1).
Capable of reasoning over user requests and orchestrating:
1. rag_search (InternGuide knowledge base retrieval & citations)
2. internship_credit_calculator (1 credit = 45 hours; 70% industry + 30% panel; hours-weighted net score)
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.tools import internship_credit_calculator, rag_search, tool_registry


def extract_calculation_params(text: str) -> Optional[List[Dict[str, Any]]]:
    """
    Heuristically extracts activities, hours, and scores from user prompts.
    Examples:
      - '90 hours internship with 9/10 from company and 6/10 from college panel'
      - '45 hours rural NSS camp with 8 industry and 7 college panel'
    """
    text_lower = text.lower()
    activities = []

    # Match hour patterns: e.g., 90-hour or 90 hours
    hour_matches = list(re.finditer(r'(\d+(?:\.\d+)?)\s*(?:-|–|\s*)?(?:hour|hr)s?', text_lower))

    if hour_matches:
        for idx, m in enumerate(hour_matches):
            hours_val = float(m.group(1))
            start_span = m.start()
            end_span = hour_matches[idx + 1].start() if idx + 1 < len(hour_matches) else len(text)
            segment = text[start_span:end_span]
            segment_lower = segment.lower()

            # Default scores if unspecified
            ind_score = 8.0
            inst_score = 7.0

            # Find scores with explicit "/10" or next to industry/company/panel
            scores_found = re.findall(r'(\d+(?:\.\d+)?)\s*(?:/\s*10|\s*out of\s*10)', segment_lower)
            if len(scores_found) >= 2:
                ind_score = float(scores_found[0])
                inst_score = float(scores_found[1])
            elif len(scores_found) == 1:
                ind_score = float(scores_found[0])
            else:
                # Look for number near company/industry
                comp_m = re.search(r'(?:company|industry|supervisor)[^\d]{1,15}(\d+(?:\.\d+)?)', segment_lower)
                if comp_m:
                    ind_score = float(comp_m.group(1))
                # Look for number near panel/college/institute
                panel_m = re.search(r'(?:panel|college|institute|mentor)[^\d]{1,15}(\d+(?:\.\d+)?)', segment_lower)
                if panel_m:
                    inst_score = float(panel_m.group(1))

            title = "Internship Activity"
            if "rural" in segment_lower or "nss" in segment_lower:
                title = "Rural NSS / Community Activity"
            elif "industry" in segment_lower or "company" in segment_lower or "software" in segment_lower:
                title = "Industry Internship"

            activities.append({
                "title": title,
                "hours": hours_val,
                "industry_score": ind_score,
                "institute_panel_score": inst_score
            })

    return activities if activities else None


def run_agent_handwritten(query: str, activities_input: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Hand-written agent loop:
    1. Evaluates user intent: Calculation, Policy Retrieval, or Compound.
    2. Calls the appropriate tool(s).
    3. Synthesizes a unified response.
    """
    q_lower = query.lower()
    tools_used = []
    tool_results = {}
    citations = []

    # Check for credit calculation intent
    needs_calc = any(k in q_lower for k in [
        "calculate", "calculator", "credits earned", "net score", "weighted score",
        "marks", "credit and net score", "how many credits do i get for"
    ]) or ("hour" in q_lower and ("score" in q_lower or "panel" in q_lower or "company" in q_lower))

    # Check for policy retrieval intent
    needs_search = any(k in q_lower for k in [
        "policy", "rule", "guideline", "aicte", "ugc", "pmis", "pm internship",
        "leave", "eligible", "eligibility", "online internship", "noc", "stipend",
        "which companies", "who can apply", "what is"
    ]) or not needs_calc

    # 1. Execute calculation tool if requested
    calc_result = None
    if needs_calc or activities_input:
        acts = activities_input or extract_calculation_params(query)
        if acts:
            calc_result = internship_credit_calculator(activities=acts)
        else:
            # Fallback default activity from query numbers
            calc_result = internship_credit_calculator(hours=45.0, industry_score=8.0, institute_panel_score=7.0)
        tools_used.append("internship_credit_calculator")
        tool_results["internship_credit_calculator"] = calc_result

    # 2. Execute RAG search tool if requested
    rag_result = None
    if needs_search:
        rag_result = rag_search(query)
        tools_used.append("rag_search")
        tool_results["rag_search"] = rag_result
        if isinstance(rag_result, dict):
            citations = rag_result.get("citations", [])

    # 3. Synthesize the final answer
    answer_parts = []

    if calc_result:
        answer_parts.append(f"**Internship Credit & Score Calculation:**\n{calc_result['summary']}")
        breakdown = []
        for a in calc_result["activities"]:
            breakdown.append(
                f"- **{a['title']}**: {a['hours']} hours -> **{a['credits']} credits** "
                f"(Industry: {a['industry_score']}, Panel: {a['institute_panel_score']} -> Activity Marks: {a['activity_marks']}/10)"
            )
        answer_parts.append("\n".join(breakdown))
        answer_parts.append(f"**Total Credits:** {calc_result['total_credits']} credits | **Net Score:** {calc_result['net_score']}/10")

    if rag_result:
        rag_text = rag_result.get("answer", "") if isinstance(rag_result, dict) else str(rag_result)
        if calc_result:
            answer_parts.append(f"\n**Relevant Policy Guidelines:**\n{rag_text}")
        else:
            answer_parts.append(rag_text)

    final_answer = "\n\n".join(answer_parts).strip()

    return {
        "query": query,
        "answer": final_answer,
        "tools_used": tools_used,
        "tool_results": tool_results,
        "citations": citations
    }


def agent_loop():
    """Interactive CLI agent loop matching classwork demonstration."""
    print("=" * 60)
    print("InternGuide Agent CLI (Type 'exit' to quit)")
    print("Tools: rag_search, internship_credit_calculator")
    print("=" * 60)

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input or user_input.lower() == "exit":
                break

            response = run_agent_handwritten(user_input)
            print("\n[Tools Used]:", response["tools_used"])
            print("\nAgent:", response["answer"])
            if response["citations"]:
                print("\nCitations:", response["citations"])
        except (KeyboardInterrupt, EOFError):
            break


if __name__ == "__main__":
    test_queries = [
        "How many hours is one internship credit as per AICTE?",
        "I did a 90-hour internship with 9/10 from company and 6/10 from college panel, plus 45-hour rural camp with 8/10 industry and 7/10 panel. Calculate my credits and net score.",
        "Which specific IT companies in Pune are offering paid AI internships this summer?"
    ]

    for q in test_queries:
        print("\n" + "=" * 50)
        print("Query:", q)
        res = run_agent_handwritten(q)
        print("Tools Used:", res["tools_used"])
        print("Answer:\n", res["answer"])
