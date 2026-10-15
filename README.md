# onboarding-agents

MVP de um sistema multi-agente que orienta colaboradores no onboarding a plataformas de IA
(LiteLLM, LangFuse, Gemini Enterprise) e abre automaticamente o ticket de acesso no Mock Gemud.

## Arquitetura

Monorepo com três aplicações e um único container Docker (Postgres):

| Aplicação | Diretório | Stack | Porta |
|-----------|-----------|-------|-------|
| Web (UI + BFF) | `apps/web` | Next.js (App Router, TypeScript strict, Tailwind) | 3000 |
| Agents (multi-agente) | `apps/agents` | FastAPI + LangGraph | 8001 |
| Mock Gemud (tickets) | `apps/mock-gemud` | FastAPI + SQLite | 8000 |
| Postgres (checkpointer) | `docker-compose.yml` | postgres:16-alpine | 5433 |

O fluxo de agentes: **porteiro** (classifica a plataforma) → **especialista** (coleta campos) →
**validador** (valida campos obrigatórios) → **abrir_ticket** (abre o ticket). Quando há campos
faltantes, o validador retorna ao especialista.

Os campos obrigatórios por plataforma são declarativos (`apps/agents/contracts/platforms.json`):
adicionar uma plataforma é configuração, não código.

## Pré-requisitos

- [uv](https://docs.astral.sh/uv/) (Python)
- Node.js 18+ e npm
- Docker + Docker Compose

## Como executar

Suba o Postgres (checkpointer do LangGraph):

```bash
docker compose up -d
```

### 1. Mock Gemud (tickets)

```bash
cd apps/mock-gemud
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

### 2. Agents (multi-agente)

```bash
cd apps/agents
uv sync
uv run uvicorn app.main:app --reload --port 8001
```

### 3. Web (UI + BFF)

```bash
cd apps/web
npm install
npm run dev
```

Abra http://localhost:3000. A aba **Chat** conversa com o agente; a aba **Tickets** lista os
tickets criados no Mock Gemud.

## Configuração

Os backends são configurados por variáveis de ambiente (com defaults locais):

| Variável | Default | Descrição |
|----------|---------|-----------|
| `MOCK_GEMUD_URL` | `http://localhost:8000` | URL do Mock Gemud (usada pelos agents) |
| `DATABASE_URL` | `postgresql://onboarding:onboarding@localhost:5433/onboarding` | Postgres do checkpointer |

## Convenções

- Texto da interface em português (pt-BR).
- Commits seguem Conventional Commits.
- TypeScript em modo strict; Python com `uv` e type hints.
