from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

COMMON_FIELDS: list[str] = ["nome_coordenacao", "centro_custo", "matricula_responsavel"]

PLATFORM_REQUIRED_FIELDS: dict[str, list[str]] = {
    "litellm": ["ambiente", "modelos", "limite_tokens"],
    "langfuse": ["nome_projeto", "ambiente", "limite_trace_mensal"],
    "gemini_enterprise": ["nome_agente", "descricao", "nivel_acesso"],
}


class Ticket(BaseModel):
    id: int | None = None
    platform: str
    nome_coordenacao: str
    centro_custo: str
    matricula_responsavel: str
    fields: dict[str, Any] = Field(default_factory=dict)
    created_at: str | None = None

    @field_validator("centro_custo")
    @classmethod
    def _validate_centro_custo(cls, value: str) -> str:
        if not value.isdigit() or len(value) != 9:
            raise ValueError("centro_custo deve ter exatamente 9 dígitos")
        return value

    @field_validator("matricula_responsavel")
    @classmethod
    def _validate_matricula_responsavel(cls, value: str) -> str:
        if not value.isdigit() or len(value) != 10:
            raise ValueError("matricula_responsavel deve ter exatamente 10 dígitos")
        return value

    @model_validator(mode="after")
    def _validate_platform_fields(self) -> "Ticket":
        required = PLATFORM_REQUIRED_FIELDS.get(self.platform)
        if required is None:
            raise ValueError(f"plataforma desconhecida: {self.platform}")
        missing = [field for field in required if not str(self.fields.get(field, "")).strip()]
        if missing:
            raise ValueError(f"campos obrigatórios ausentes: {', '.join(missing)}")
        return self
