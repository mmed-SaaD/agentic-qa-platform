from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_status_code():
    response = client.get("/health")
    assert response.status_code == 200

def test_health_response_body():
    response = client.get("/health")

    assert response.json() == {
        "status" : "healthy",
        "service" : "agentic-qa-platform"
    }

def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to the Agentic QA Platform"
