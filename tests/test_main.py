from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_application():
    payload= {
        "company": "Stripe",
        "role": "Backend Intern",
        "status": "applied",
        "applied_date": "2026-05-05"
    }
    response = client.post("/applications", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["company"] == "Stripe"
    assert data["role"] == "Backend Intern"
    assert data["status"] == "applied"
    assert data["applied_date"] == "2026-05-05"
    assert isinstance(data["id"], int)
    assert data["id"] >= 1

def test_create_application_invalid_status():
    payload = {
        "company": "Stripe",
        "role": "Backend Intern",
        "status": "active",
        "applied_date": "2026-05-05"
    }

    response = client.post("/applications", json=payload)
    assert response.status_code == 422