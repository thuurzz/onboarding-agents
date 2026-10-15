import os

import httpx

MOCK_GEMUD_URL: str = os.getenv("MOCK_GEMUD_URL", "http://localhost:8001")


def abrir_ticket(platform: str, common: dict[str, str], platform_fields: dict[str, str]) -> dict:
    payload = {
        "platform": platform,
        "nome_coordenacao": common.get("nome_coordenacao", ""),
        "centro_custo": common.get("centro_custo", ""),
        "matricula_responsavel": common.get("matricula_responsavel", ""),
        "fields": platform_fields,
    }
    response = httpx.post(f"{MOCK_GEMUD_URL}/tickets", json=payload, timeout=10.0)
    response.raise_for_status()
    return response.json()
