"""
IndusMind AI — Health Check Tests

Smoke tests for the application health and root endpoints.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Tests for the /health endpoint."""

    def test_health_returns_200(self) -> None:
        """Health check should return 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_status_healthy(self) -> None:
        """Health check should indicate healthy status."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_returns_app_name(self) -> None:
        """Health check should return the application name."""
        response = client.get("/health")
        data = response.json()
        assert data["name"] == "IndusMind AI"

    def test_health_returns_version(self) -> None:
        """Health check should return a version string."""
        response = client.get("/health")
        data = response.json()
        assert "version" in data
        assert isinstance(data["version"], str)

    def test_health_returns_demo_mode(self) -> None:
        """Health check should indicate demo mode status."""
        response = client.get("/health")
        data = response.json()
        assert "demo_mode" in data


class TestRootEndpoint:
    """Tests for the / root endpoint."""

    def test_root_returns_200(self) -> None:
        """Root endpoint should return 200 OK."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_returns_app_info(self) -> None:
        """Root endpoint should return application info."""
        response = client.get("/")
        data = response.json()
        assert data["name"] == "IndusMind AI"
        assert "version" in data
        assert "docs" in data
        assert "health" in data

    def test_root_points_to_docs(self) -> None:
        """Root endpoint should reference the docs URL."""
        response = client.get("/")
        data = response.json()
        assert data["docs"] == "/docs"
