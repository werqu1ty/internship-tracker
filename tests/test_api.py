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


def test_update_application_found(client):
    client.post("/api/applications", json={"company": "Shall", "role": "casheir"})
    response = client.put("/api/applications/1", json={"company": "Shell", "role": "cashier"})
    assert response.status_code == 200
    response = client.get("/api/applications/1")
    assert response.get_json()["company"] == "Shell"
    assert response.get_json()["role"] == "cashier"


def test_update_application_not_found(client):
    client.post("/api/applications", json={"company": "Shell", "role": "cashier"})
    response = client.put("/api/applications/57", json={"company": "Shell", "role": "cashier"})
    assert response.status_code == 404


def test_update_application_missing_role(client):
    client.post("/api/applications", json={"company": "Shell", "role": "cashier"})
    response = client.put("/api/applications/1", json={"company": "Shell"})
    assert response.status_code == 400


def test_add_application_not_json_object(client):
    response1 = client.post("/api/applications", json=[])
    assert response1.status_code == 400
    response2 = client.post("/api/applications", json="hi")
    assert response2.status_code == 400


def test_update_application_not_json_object(client):
    client.post("/api/applications", json={"company": "Shell", "role": "cashier"})
    response1 = client.put("/api/applications/1", json=[])
    assert response1.status_code == 400
    response2 = client.put("/api/applications/1", json="hi")
    assert response2.status_code == 400


def test_add_application_invalid_status(client):
    response = client.post("/api/applications", json={"company": "Shell", "role": "assistant", "status": "banana"})
    assert response.status_code == 400


def test_add_application_default_status(client):
    response = client.post("/api/applications", json={"company": "Shell", "role": "assistant"})
    assert response.status_code == 201
    response = client.get("/api/applications/1")
    assert response.get_json()["status"] == "wishlist"


def test_add_application_all_fields(client):
    response = client.post("/api/applications", json={"company": "Shell", "role": "assistant", "location": "Edinburgh",
                                                       "deadline": "27 Jan 2027", "status": "offer", "notes": "Starting on 1 June", "link": "company.tal.net"})
    assert response.status_code == 201
    response = client.get("/api/applications/1")
    assert response.get_json()["company"] == "Shell"
    assert response.get_json()["role"] == "assistant"
    assert response.get_json()["location"] == "Edinburgh"
    assert response.get_json()["deadline"] == "27 Jan 2027"
    assert response.get_json()["status"] == "offer"
    assert response.get_json()["notes"] == "Starting on 1 June"
    assert response.get_json()["link"] == "company.tal.net"



