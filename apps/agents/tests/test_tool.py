from app.tools import gemud


def test_abrir_ticket_posts_to_mock_gemud(monkeypatch) -> None:
    captured: dict = {}

    class FakeResponse:
        def raise_for_status(self) -> None:
            pass

        def json(self) -> dict:
            return {"id": 1, "platform": "litellm"}

    def fake_post(url, json=None, timeout=None):
        captured["url"] = url
        captured["json"] = json
        return FakeResponse()

    monkeypatch.setattr(gemud.httpx, "post", fake_post)

    result = gemud.abrir_ticket(
        "litellm",
        {
            "nome_coordenacao": "Coord IA",
            "centro_custo": "123456789",
            "matricula_responsavel": "1234567890",
        },
        {"ambiente": "prod", "modelos": "gpt-4o", "limite_tokens": "100000"},
    )

    assert result["id"] == 1
    assert captured["url"] == "http://localhost:8000/tickets"
    payload = captured["json"]
    assert payload["platform"] == "litellm"
    assert payload["centro_custo"] == "123456789"
    assert payload["fields"] == {"ambiente": "prod", "modelos": "gpt-4o", "limite_tokens": "100000"}
