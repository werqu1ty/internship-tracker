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