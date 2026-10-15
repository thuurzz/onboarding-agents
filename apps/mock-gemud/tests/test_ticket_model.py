import pytest
from pydantic import ValidationError

from app.models.ticket import Ticket


def _valid_ticket(**overrides) -> dict:
    payload = {
        "platform": "litellm",
        "nome_coordenacao": "Coordenacao de IA",
        "centro_custo": "123456789",
        "matricula_responsavel": "1234567890",
        "fields": {"ambiente": "prod", "modelos": "gpt-4o", "limite_tokens": "100000"},
    }
    payload.update(overrides)
    return payload


def test_valid_ticket() -> None:
    ticket = Ticket(**_valid_ticket())
    assert ticket.centro_custo == "123456789"


def test_invalid_centro_custo_rejected() -> None:
    with pytest.raises(ValidationError):
        Ticket(**_valid_ticket(centro_custo="12345"))


def test_invalid_matricula_responsavel_rejected() -> None:
    with pytest.raises(ValidationError):
        Ticket(**_valid_ticket(matricula_responsavel="123"))


def test_unknown_platform_rejected() -> None:
    with pytest.raises(ValidationError):
        Ticket(**_valid_ticket(platform="desconhecida"))


def test_missing_platform_field_rejected() -> None:
    with pytest.raises(ValidationError):
        Ticket(**_valid_ticket(fields={"ambiente": "prod"}))
