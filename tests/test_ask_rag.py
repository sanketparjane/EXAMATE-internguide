# tests/test_ask_rag.py
"""
Tests for POST /ask RAG endpoint with fake LLM mocking and refusal validation.
"""

from unittest.mock import patch


def test_ask_endpoint_with_fake_llm(client):
    """
    Test POST /ask using a fake LLM mock to verify answer generation,
    grounded synthesis, and citation inclusion without network dependencies.
    """
    fake_response = {
        "question": "How many hours is one internship credit as per AICTE?",
        "answer": "As per AICTE Internship Policy 2019, 1 credit is 30 hours. [internship_doc_1.pdf, Page 7]",
        "citations": [
            {
                "source": "internship_doc_1.pdf",
                "page": 7,
                "title": "AICTE Guidelines for Organizing Internship"
            }
        ],
        "retrieved_chunks": [
            {
                "source": "internship_doc_1.pdf",
                "page": 7,
                "text": "1 credit is equivalent to minimum 30-45 hours."
            }
        ]
    }

    with patch("app.rag.ask", return_value=fake_response):
        payload = {"question": "How many hours is one internship credit as per AICTE?"}
        response = client.post("/ask", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "citations" in data
        assert len(data["citations"]) > 0
        assert data["citations"][0]["source"] == "internship_doc_1.pdf"
        assert data["citations"][0]["page"] == 7
        assert "[internship_doc_1.pdf, Page 7]" in data["answer"]


def test_ask_out_of_scope_q6_refusal(client):
    """
    Test POST /ask strictly returns 'I don't know' for Q6 (Pune IT companies)
    and provides empty citations.
    """
    payload = {
        "question": "Which specific IT companies in Pune are offering paid AI internships this summer?"
    }
    response = client.post("/ask", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert "I don't know based on the provided information" in data["answer"]
    assert data["citations"] == []


def test_ask_missing_input_validation(client):
    """Test POST /ask without question/query returns 400 Bad Request."""
    response = client.post("/ask", json={})
    assert response.status_code == 400
