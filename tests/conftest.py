# tests/conftest.py
"""
Shared fixtures for InternGuide pytest test suite.
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.main import app


@pytest.fixture(scope="session")
def client():
    """FastAPI TestClient fixture."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_activities():
    """Sample internship activities for testing calculation tool."""
    return [
        {
            "title": "Industrial Software Internship",
            "hours": 90.0,
            "industry_score": 9.0,
            "institute_panel_score": 6.0
        },
        {
            "title": "Rural NSS Community Engagement",
            "hours": 45.0,
            "industry_score": 8.0,
            "institute_panel_score": 7.0
        }
    ]
