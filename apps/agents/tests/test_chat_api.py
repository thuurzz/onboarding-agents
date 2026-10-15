from fastapi.testclient import TestClient

from tests.conftest import make_app


def test_chat_returns_reply_and_thread_id() -> None:
    with TestClient(make_app()) as client:
        response = client.post("/chat", json={"message": "quero acesso ao litellm"})
        assert response.status_code == 200
        body = response.json()
        assert body["thread_id"]
        assert "plataforma" in body["reply"] or "faltam" in body["reply"]


def test_chat_resumes_same_thread(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.controllers.graph.abrir_ticket",
        lambda platform, common, platform_fields: {"id": 1, "platform": platform},
    )
    with TestClient(make_app()) as client:
        first = client.post("/chat", json={"message": "quero acesso ao litellm"}).json()
        thread_id = first["thread_id"]

        second = client.post(
            "/chat",
            json={
                "thread_id": thread_id,
                "message": (
                    "nome_coordenacao: Coord IA, centro_custo: 123456789, "
                    "matricula_responsavel: 1234567890, ambiente: prod, "
                    "modelos: gpt-4o, limite_tokens: 100000"
                ),
            },
        )
        assert second.status_code == 200
        body = second.json()
        assert body["thread_id"] == thread_id
        assert "faltam" not in body["reply"]


def test_conversation_returns_history() -> None:
    with TestClient(make_app()) as client:
        client.post("/chat", json={"message": "quero acesso ao litellm"})
        thread_id = client.post("/chat", json={"message": "quero acesso ao langfuse"}).json()[
            "thread_id"
        ]
        response = client.get(f"/conversation/{thread_id}")
        assert response.status_code == 200
        messages = response.json()["messages"]
        assert any(m["role"] == "user" for m in messages)


def test_conversation_unknown_thread_returns_404() -> None:
    with TestClient(make_app()) as client:
        response = client.get("/conversation/nao-existe")
        assert response.status_code == 404
