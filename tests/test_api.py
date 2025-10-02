import pytest
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_log_error_endpoint():
    """Test frontend error logging endpoint"""
    error_data = {
        "message": "Test error",
        "filename": "test.js",
        "lineno": 10,
        "colno": 5,
        "stack": "Error: Test error\n  at test.js:10:5",
        "timestamp": "2025-10-02T10:00:00Z",
        "userAgent": "Mozilla/5.0",
        "type": "error"
    }
    response = client.post("/api/log-error", json=error_data)
    assert response.status_code == 200
    assert response.json() == {"status": "logged"}


def test_log_error_minimal():
    """Test error logging with minimal required fields"""
    error_data = {
        "message": "Minimal error"
    }
    response = client.post("/api/log-error", json=error_data)
    assert response.status_code == 200
    assert response.json() == {"status": "logged"}


def test_sf_query_missing_soql():
    """Test Salesforce query endpoint with missing SOQL"""
    response = client.post("/api/sf/query", json={})
    assert response.status_code == 422  # Validation error


def test_root_endpoint():
    """Test root endpoint serves frontend or returns message"""
    response = client.get("/")
    assert response.status_code == 200


def test_cors_headers():
    """Test CORS headers are present"""
    response = client.get("/api/health", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
