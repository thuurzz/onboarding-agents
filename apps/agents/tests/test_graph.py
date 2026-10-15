from langgraph.checkpoint.memory import MemorySaver

from app.controllers.builder import build_graph


def _graph():
    return build_graph(checkpointer=MemorySaver())


def test_unknown_platform_asks_for_clarification() -> None:
    graph = _graph()
    result = graph.invoke(
        {"messages": [{"role": "user", "content": "quero acesso"}]},
        config={"configurable": {"thread_id": "t-unknown"}},
    )
    assert result.get("platform") is None
    assert "plataforma" in result.get("reply", "").lower()


def test_missing_fields_flow_loops_back_and_exits() -> None:
    graph = _graph()
    result = graph.invoke(
        {"messages": [{"role": "user", "content": "quero acesso ao litellm"}]},
        config={"configurable": {"thread_id": "t-missing"}},
    )
    assert result.get("platform") == "litellm"
    assert result.get("missing_fields")
    assert result.get("ticket_result") is None
    assert "faltam" in result.get("reply", "")


def test_complete_flow_exits_via_ticket(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.controllers.graph.abrir_ticket",
        lambda platform, common, platform_fields: {
            "id": 1,
            "platform": platform,
        },
    )
    graph = _graph()
    message = (
        "quero acesso ao litellm, nome_coordenacao: Coord IA, "
        "centro_custo: 123456789, matricula_responsavel: 1234567890, "
        "ambiente: prod, modelos: gpt-4o, limite_tokens: 100000"
    )
    result = graph.invoke(
        {"messages": [{"role": "user", "content": message}]},
        config={"configurable": {"thread_id": "t-complete"}},
    )
    assert result.get("ticket_result") is not None
    assert result["ticket_result"]["id"] == 1
    assert "sucesso" in result.get("reply", "")


def test_invalid_centro_custo_asks_again() -> None:
    graph = _graph()
    message = (
        "quero acesso ao litellm, nome_coordenacao: Coord IA, "
        "centro_custo: 123, matricula_responsavel: 1234567890, "
        "ambiente: prod, modelos: gpt-4o, limite_tokens: 100000"
    )
    result = graph.invoke(
        {"messages": [{"role": "user", "content": message}]},
        config={"configurable": {"thread_id": "t-invalid"}},
    )
    assert result.get("ticket_result") is None
    assert "centro_custo" in result.get("reply", "")
