# tests/test_agent_workflow.py
"""
Tests for POST /agent LangGraph workflow with memory and approval step.
"""


def test_agent_endpoint_approved(client):
    """Test POST /agent executes credit calculation when approved."""
    payload = {
        "query": "Calculate my credits: 90 hours with 9 industry score and 6 panel score.",
        "session_id": "test_session_approved",
        "approved": True
    }
    response = client.post("/agent", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["approval_status"] == "approved"
    assert "internship_credit_calculator" in data["tools_used"]
    assert "2.0 credits" in data["response"] or "Credits" in data["response"]


def test_agent_endpoint_rejection_step(client):
    """Test POST /agent halts and rejects calculation when approved=False."""
    payload = {
        "query": "Calculate my credits for 90 hours internship.",
        "session_id": "test_session_rejected",
        "approved": False
    }
    response = client.post("/agent", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["approval_status"] == "rejected"
    assert "Action Blocked" in data["response"]
