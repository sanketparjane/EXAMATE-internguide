# tests/test_agent_tools.py
"""
Tests for agent tools: internship_credit_calculator (45 hrs/credit, 70:30 weighting) and rag_search.
"""

from app.tools import internship_credit_calculator, rag_search


def test_credit_calculator_conversion_45_hours(sample_activities):
    """
    Test credit conversion where 1 credit = 45 hours.
    Activity 1: 90 hours -> 2.0 credits
    Activity 2: 45 hours -> 1.0 credit
    Total: 135 hours -> 3.0 credits
    """
    result = internship_credit_calculator(activities=sample_activities)
    assert result["status"] == "success"
    assert result["total_hours"] == 135.0
    assert result["total_credits"] == 3.0
    assert result["activities"][0]["credits"] == 2.0
    assert result["activities"][1]["credits"] == 1.0


def test_credit_calculator_evaluation_marks_70_30(sample_activities):
    """
    Test per-activity marks formula: 70% industry + 30% institute panel.
    Activity 1: (0.7 * 9.0) + (0.3 * 6.0) = 6.3 + 1.8 = 8.1
    Activity 2: (0.7 * 8.0) + (0.3 * 7.0) = 5.6 + 2.1 = 7.7
    """
    result = internship_credit_calculator(activities=sample_activities)
    acts = result["activities"]
    assert acts[0]["activity_marks"] == 8.1
    assert acts[1]["activity_marks"] == 7.7


def test_credit_calculator_net_hours_weighted_score(sample_activities):
    """
    Test net score formula: hours-weighted average of activity marks.
    Net = [(8.1 * 90) + (7.7 * 45)] / 135 = (729 + 346.5) / 135 = 1075.5 / 135 = 7.97
    """
    result = internship_credit_calculator(activities=sample_activities)
    assert result["net_score"] == 7.97


def test_credit_calculator_empty_input():
    """Test credit calculator handles empty inputs gracefully."""
    result = internship_credit_calculator(activities=[])
    assert "error" in result
    assert result["total_credits"] == 0.0


def test_rag_search_tool():
    """Test rag_search tool returns grounded response with citations."""
    res = rag_search("How many hours is one internship credit as per AICTE?")
    assert "answer" in res
    assert "credit" in res["answer"].lower()
    assert len(res["citations"]) > 0
