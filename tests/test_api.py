import pytest
import db
from app import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "test.db"))
    db.init_db()
    return app.test_client()


def test_add_application(client):
    response = client.post("/api/applications", json={"company": "BP", "role": "Analyst"})
    assert response.status_code == 201


def test_add_aplication_missing_role(client):
    response = client.post("/api/applications", json={"company": "JP"})
    assert response.status_code == 400


def test_get_application_not_found(client):
    response = client.get("/api/applications/999")
    assert response.status_code == 404


def test_get_application_found(client):
    client.post("/api/applications", json={"company": "Shell", "role": "cashier"})
    response = client.get("/api/applications/1")
    assert response.status_code == 200
    assert response.get_json()["company"] == "Shell"


def test_delete_application_found(client):
    client.post("/api/applications", json={"company": "Shell", "role": "cashier"})
    response = client.delete("/api/applications/1")
    assert response.status_code == 200
    response = client.get("/api/applications/1")
    assert response.status_code == 404


def test_delete_application_not_found(client):
    client.post("/api/applications", json={"company": "Shell", "role": "cashier"})
    response = client.delete("/api/applications/5")
    assert response.status_code == 404