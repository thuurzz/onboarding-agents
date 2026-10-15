from app.controllers import ticket_service
from app.db import database
from app.models.ticket import Ticket


def _ticket(**overrides) -> Ticket:
    payload = {
        "platform": "langfuse",
        "nome_coordenacao": "Coord Observabilidade",
        "centro_custo": "987654321",
        "matricula_responsavel": "0987654321",
        "fields": {"nome_projeto": "proj", "ambiente": "staging", "limite_trace_mensal": "5000"},
    }
    payload.update(overrides)
    return Ticket(**payload)


def test_tickets_survive_restart(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    database.init_db()

    created = ticket_service.create_ticket(_ticket())
    assert created.id is not None

    listed = ticket_service.list_tickets()
    assert len(listed) == 1
    assert listed[0].nome_coordenacao == "Coord Observabilidade"

    fetched = ticket_service.get_ticket(created.id)
    assert fetched is not None
    assert fetched.platform == "langfuse"


def test_get_ticket_missing_returns_none(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test2.db")
    database.init_db()
    assert ticket_service.get_ticket(9999) is None
