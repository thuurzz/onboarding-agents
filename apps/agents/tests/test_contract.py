from app.contracts import (
    all_required_fields,
    common_fields,
    platform_ids,
    platform_name,
    platform_required_fields,
)


def test_contract_lists_platforms() -> None:
    assert platform_ids() == ["litellm", "langfuse", "gemini_enterprise"]


def test_common_fields() -> None:
    assert common_fields() == ["nome_coordenacao", "centro_custo", "matricula_responsavel"]


def test_platform_required_fields() -> None:
    assert platform_required_fields("litellm") == ["ambiente", "modelos", "limite_tokens"]
    assert platform_required_fields("langfuse") == [
        "nome_projeto",
        "ambiente",
        "limite_trace_mensal",
    ]
    assert platform_required_fields("gemini_enterprise") == [
        "nome_agente",
        "descricao",
        "nivel_acesso",
    ]


def test_all_required_fields_merge_common_and_platform() -> None:
    assert all_required_fields("litellm") == [
        "nome_coordenacao",
        "centro_custo",
        "matricula_responsavel",
        "ambiente",
        "modelos",
        "limite_tokens",
    ]


def test_platform_name() -> None:
    assert platform_name("litellm") == "LiteLLM"
    assert platform_name("gemini_enterprise") == "Gemini Enterprise"
    assert platform_name("desconhecida") is None
