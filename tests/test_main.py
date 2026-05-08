import pytest
from fastapi.testclient import TestClient
from app.main import app, applications

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_applications():
    applications.clear()
    yield


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

def test_list_applications():
    payload = {
        "company": "Stripe",
        "role": "Backend Intern",
        "status": "applied",
        "applied_date": "2026-05-05"
    }

    client.post("/applications", json=payload)

    response = client.get("/applications")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1

def test_get_application_success():
    payload = {
        "company": "Acme",
        "role": "Engineer",
        "status": "applied",
        "applied_date": "2026-05-07"
    }
    create_response = client.post("/applications", json=payload)
    create_id =create_response.json()["id"]

    response = client.get(f"/applications/{create_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == create_id
    assert data["company"] == "Acme"

def test_get_application_not_found():
    response = client.get("/applications/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_update_application_success():
    payload = {
        "company": "Acme",
        "role": "Engineer",
        "status": "applied",
        "applied_date": "2026-05-07"
    }

    create_response = client.post("/applications", json=payload)
    created_id = create_response.json()["id"]

    update_payload = {"status": "interviewing"}
    response = client.patch(f"/applications/{created_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "interviewing"
    assert data["company"] == "Acme"
    assert data["id"] == created_id

def test_update_application_not_found():
    response = client.patch("/applications/99999999", json={"status": "interviewing"})
    assert response.status_code == 404

def test_delete_application_success():
    payload = {
        "company": "Acme",
        "role": "Engineer",
        "status": "applied",
        "applied_date": "2026-05-07"
    }
    create_response = client.post("/applications", json=payload)
    created_id = create_response.json()["id"]

    delete_response = client.delete(f"/applications/{created_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/applications/{created_id}")
    assert get_response.status_code == 404

def test_delete_application_not_found():
    response = client.delete("/applications/9999999")
    assert response.status_code == 404


