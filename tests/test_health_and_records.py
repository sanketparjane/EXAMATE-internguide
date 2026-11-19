# tests/test_health_and_records.py
"""
Tests for /health and /records endpoints.
"""


def test_health_endpoint(client):
    """Test GET /health returns status ok and project name."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["project"] == "InternGuide"


def test_records_list_endpoint(client):
    """Test GET /records returns non-empty list of parsed records."""
    response = client.get("/records")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    first_record = data[0]
    assert "id" in first_record
    assert "activity_head" in first_record or "title" in first_record


def test_records_limit_parameter(client):
    """Test GET /records?limit=3 limits output length."""
    response = client.get("/records?limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 3


def test_record_by_id_success(client):
    """Test GET /records/1 returns the first record."""
    response = client.get("/records/1")
    assert response.status_code == 200
    data = response.json()
    assert data.get("id") == 1


def test_record_by_id_not_found(client):
    """Test GET /records/999999 returns 404."""
    response = client.get("/records/999999")
    assert response.status_code == 404
