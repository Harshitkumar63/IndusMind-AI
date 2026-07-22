"""
IndusMind AI — Test Fixtures

Shared pytest fixtures for the backend test suite.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Create a test client for the FastAPI application."""
    return TestClient(app)
