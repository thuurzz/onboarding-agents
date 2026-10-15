from fastapi.testclient import TestClient

from app.db import database
from app.main import app


def _ticket_payload(**overrides) -> dict:
    payload = {
        "platform": "litellm",
        "nome_coordenacao": "Coord IA",
        "centro_custo": "111222333",
        "matricula_responsavel": "1112223334",
        "fields": {"ambiente": "prod", "modelos": "gpt-4o", "limite_tokens": "100000"},
    }
    payload.update(overrides)
    return payload


def test_create_list_and_get_ticket(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "api.db")
    database.init_db()

    with TestClient(app) as client:
        created = client.post("/tickets", json=_ticket_payload())
        assert created.status_code == 201
        body = created.json()
        assert body["id"] is not None

        listed = client.get("/tickets")
        assert listed.status_code == 200
        assert len(listed.json()) == 1

        fetched = client.get(f"/tickets/{body['id']}")
        assert fetched.status_code == 200
        assert fetched.json()["platform"] == "litellm"


def test_get_missing_ticket_returns_404(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "api404.db")
    database.init_db()

    with TestClient(app) as client:
        response = client.get("/tickets/9999")
        assert response.status_code == 404


def test_invalid_ticket_returns_validation_error(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "api_invalid.db")
    database.init_db()

    with TestClient(app) as client:
        response = client.post("/tickets", json=_ticket_payload(centro_custo="12"))
        assert response.status_code == 422
        assert client.get("/tickets").json() == []
