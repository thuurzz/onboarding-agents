"""Abstração de LLM via LiteLLM SDK.

Permite trocar de provider (Ollama Cloud, LightLLM, OpenAI, etc.) sem refatorar os nós
do grafo — basta mudar as variáveis LLM_MODEL / LLM_API_BASE / LLM_API_KEY no ambiente.

Configuração (env):
  LLM_MODEL     — ex.: "ollama/deepseek-v4-pro" ou "openai/gpt-4o-mini"
  LLM_API_BASE  — URL base do provider (opcional; OpenAI-compatible)
  LLM_API_KEY   — chave de API
"""

import json
import os

import litellm

litellm.drop_params = True  # ignora params não suportados pelo provider alvo


def _model() -> str:
    return os.getenv("LLM_MODEL", "openai/deepseek-v4-pro")


def _kwargs() -> dict:
    kwargs: dict = {}
    base = os.getenv("LLM_API_BASE")
    key = os.getenv("LLM_API_KEY")
    if base:
        kwargs["api_base"] = base
    if key:
        kwargs["api_key"] = key
    return kwargs


def _complete_json(messages: list[dict]) -> dict:
    """Chama o LLM pedindo JSON e devolve o dict parseado ({} em falha)."""
    try:
        response = litellm.completion(
            model=_model(),
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0,
            **_kwargs(),
        )
        raw = response.choices[0].message.content or ""
        return json.loads(raw)
    except Exception:
        return {}


def classify_platform(message: str, platforms: list[dict]) -> str | None:
    """Classifica a plataforma a partir de texto livre (retorna o id, ou None)."""
    names = ", ".join(p["name"] for p in platforms)
    ids = [p["id"] for p in platforms]
    prompt = (
        f"Identifique qual destas plataformas o usuário quer acessar: {names}. "
        f"IDs válidos: {ids}. "
        'Responda APENAS com JSON no formato {"platform": "<id>"} — use null se '
        "nenhuma plataforma for mencionada."
    )
    result = _complete_json([
        {"role": "system", "content": "Você é um classificador de intenção."},
        {"role": "user", "content": prompt + "\n\nMensagem do usuário:\n" + message},
    ])
    platform = result.get("platform")
    return platform if platform in ids else None


def extract_fields(message: str, field_names: list[str]) -> dict[str, str]:
    """Extrai campos a partir de linguagem natural (ex.: 'quero um agente pro
    financeiro, ambiente de produção' -> {nome_agente, ambiente, ...})."""
    if not field_names:
        return {}
    prompt = (
        f"Extraia do texto os seguintes campos: {', '.join(field_names)}. "
        "O usuário pode ter informado em linguagem natural, não só 'campo: valor'. "
        "Responda APENAS com JSON contendo as chaves encontradas e seus valores "
        "(string). Não invente valores; omita chaves que não aparecerem no texto."
    )
    result = _complete_json([
        {"role": "system", "content": "Você extrai dados estruturados de texto."},
        {"role": "user", "content": prompt + "\n\nTexto:\n" + message},
    ])
    return {
        field: str(value)
        for field, value in result.items()
        if field in field_names and str(value).strip()
    }
