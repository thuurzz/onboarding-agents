import json

from app.models.state import OnboardingState


def test_state_serializes_and_deserializes() -> None:
    state: OnboardingState = {
        "thread_id": "t1",
        "messages": [{"role": "user", "content": "oi"}, {"role": "assistant", "content": "olá"}],
        "platform": "litellm",
        "fields": {"nome_coordenacao": "Coord IA", "centro_custo": "123456789"},
        "missing_fields": ["matricula_responsavel"],
        "attempts": 1,
        "ticket_result": {"id": 1, "platform": "litellm"},
        "reply": "Ticket aberto",
    }

    serialized = json.dumps(state)
    restored = json.loads(serialized)

    assert restored == state
    assert restored["platform"] == "litellm"
    assert restored["fields"]["centro_custo"] == "123456789"
