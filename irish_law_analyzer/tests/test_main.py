import pytest
from fastapi.testclient import TestClient
from pathlib import Path

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Irish Law Document Analyzer" in response.text

def test_upload_pdf(client, test_pdf):
    with open(test_pdf, "rb") as f:
        response = client.post(
            "/upload/",
            files={"file": ("test.pdf", f, "application/pdf")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "analysis" in data
    assert "risk_score" in data["analysis"]
    assert "findings" in data["analysis"]

def test_upload_invalid_file(client):
    response = client.post(
        "/upload/",
        files={"file": ("test.txt", b"invalid content", "text/plain")}
    )
    assert response.status_code == 415

def test_upload_large_file(client):
    large_content = b"0" * (10 * 1024 * 1024 + 1)  # 10MB + 1 byte
    response = client.post(
        "/upload/",
        files={"file": ("large.pdf", large_content, "application/pdf")}
    )
    assert response.status_code == 413

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"