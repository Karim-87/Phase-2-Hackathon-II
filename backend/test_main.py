import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_docs_available():
    """Test that the API documentation is available."""
    response = client.get("/api/docs")
    assert response.status_code == 200

def test_redoc_available():
    """Test that the ReDoc documentation is available."""
    response = client.get("/api/redoc")
    assert response.status_code == 200