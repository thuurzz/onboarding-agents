import re

from app.contracts import (
    all_required_fields,
    common_fields,
    platform_ids,
    platform_name,
)
from app.models.state import OnboardingState
from app.tools.gemud import abrir_ticket

PLATFORM_KEYWORDS: dict[str, list[str]] = {
    "litellm": ["litellm", "lite llm", "lite-llm"],
    "langfuse": ["langfuse", "lang fuse", "lang-fuse"],
    "gemini_enterprise": ["gemini enterprise", "gemini"],
}

FORMAT_RULES: dict[str, tuple[str, int]] = {
    "centro_custo": ("9", 9),
    "matricula_responsavel": ("10", 10),
}


def latest_user_message(state: OnboardingState) -> str:
    for message in reversed(state.get("messages", [])):
        if message.get("role") == "user":
            return message.get("content", "")
    return ""


def classify_platform(message: str) -> str | None:
    lower = message.lower()
    for platform_id, keywords in PLATFORM_KEYWORDS.items():
        for keyword in keywords:
            if keyword in lower:
                return platform_id
    return None


def extract_fields(message: str, field_names: list[str]) -> dict[str, str]:
    extracted: dict[str, str] = {}
    for field in field_names:
        # Captura o valor até a próxima vírgula/ponto-e-vírgula (ou fim), para
        # preservar valores com espaço (ex.: "Coord IA", "agente do financeiro").
        pattern = rf"{re.escape(field)}\s*[:=]\s*([^,;]+)"
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            extracted[field] = match.group(1).strip(' .,"\'')
    return extracted


def validate_format(field: str, value: str) -> str | None:
    if field in FORMAT_RULES:
        label, length = FORMAT_RULES[field]
        if not (value.isdigit() and len(value) == length):
            return f"{field} deve ter exatamente {length} dígitos"
    return None


def porteiro(state: OnboardingState) -> dict:
    updates: dict = {"attempts": 0, "missing_fields": [], "invalid_fields": []}
    platform = state.get("platform")
    if platform:
        return updates
    latest = latest_user_message(state)
    detected = classify_platform(latest)
    if detected:
        name = platform_name(detected) or detected
        reply = (
            f"Entendi! Você quer acesso à plataforma {name}. "
            "Vou coletar os dados necessários."
        )
        updates.update(
            {
                "platform": detected,
                "reply": reply,
                "messages": [{"role": "assistant", "content": reply}],
            }
        )
    else:
        names = ", ".join(platform_name(pid) or pid for pid in platform_ids())
        reply = f"Olá! Para qual plataforma você precisa de acesso? Opções: {names}."
        updates.update(
            {
                "reply": reply,
                "messages": [{"role": "assistant", "content": reply}],
            }
        )
    return updates


def route_after_porteiro(state: OnboardingState) -> str:
    return "especialista" if state.get("platform") else "end"


def especialista(state: OnboardingState) -> dict:
    platform = state.get("platform")
    latest = latest_user_message(state)
    required = all_required_fields(platform)
    extracted = extract_fields(latest, required)
    return {"fields": extracted}


def validador(state: OnboardingState) -> dict:
    platform = state.get("platform")
    fields = dict(state.get("fields", {}))
    required = all_required_fields(platform)

    missing = [field for field in required if not str(fields.get(field, "")).strip()]
    invalid = [
        field
        for field in required
        if str(fields.get(field, "")).strip() and validate_format(field, fields[field])
    ]

    if missing or invalid:
        attempts = (state.get("attempts") or 0) + 1
        problems: list[str] = []
        if missing:
            problems.append(f"faltam: {', '.join(missing)}")
        problems.extend(validate_format(field, fields[field]) for field in invalid)
        reply = "Ainda preciso de alguns dados — " + "; ".join(problems) + ". "
        reply += "Informe no formato campo: valor."
        return {
            "missing_fields": missing,
            "invalid_fields": invalid,
            "attempts": attempts,
            "reply": reply,
            "messages": [{"role": "assistant", "content": reply}],
        }

    return {"missing_fields": [], "invalid_fields": [], "attempts": 0}


def route_after_validador(state: OnboardingState) -> str:
    has_problems = bool(state.get("missing_fields") or state.get("invalid_fields"))
    if not has_problems:
        return "abrir_ticket"
    if (state.get("attempts") or 0) <= 1:
        return "especialista"
    return "end"


def abrir_ticket_node(state: OnboardingState) -> dict:
    platform = state.get("platform")
    fields = dict(state.get("fields", {}))
    common = {field: fields.get(field, "") for field in common_fields()}
    platform_field_names = [
        field for field in all_required_fields(platform) if field not in common_fields()
    ]
    platform_fields = {field: fields.get(field, "") for field in platform_field_names}
    result = abrir_ticket(platform, common, platform_fields)
    reply = f"Ticket aberto com sucesso! ID: {result.get('id')}."
    return {
        "ticket_result": result,
        "reply": reply,
        "messages": [{"role": "assistant", "content": reply}],
    }
