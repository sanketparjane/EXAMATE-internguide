# tests/test_search.py
"""
Tests for search endpoints: keyword search (/search) and semantic search (/search/semantic).
"""


def test_keyword_search(client):
    """Test GET /search?q=internship returns matching items."""
    response = client.get("/search?q=internship")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_semantic_search(client):
    """Test GET /search/semantic?q=credit+hours returns Chroma vectorstore hits."""
    response = client.get("/search/semantic?q=credit+hours&limit=4")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    hit = data[0]
    assert "source" in hit
    assert "text" in hit
    assert "similarity_score" in hit or "distance" in hit
