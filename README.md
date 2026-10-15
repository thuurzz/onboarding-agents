# Onboarding de Agentes

Sistema multi-agente que guia colaboradores no onboarding a plataformas de IA e abre,
automaticamente, o ticket de acesso correto.

---

## 💡 A ideia e a motivação de negócio

Numa empresa que gerencia múltiplas plataformas de IA — **LiteLLM** (gateway de LLM),
**LangFuse** (observabilidade) e **Gemini Enterprise** (agentes low-code) — cada uma tem um
**processo de onboarding diferente**, com campos obrigatórios próprios e a abertura de um
ticket de acesso no sistema de TI (aqui simulado pelo **Mock Gemud**).

O problema: pedir acesso hoje é **manual e sujeito a erro**. O colaborador não sabe qual
plataforma escolher, quais campos preencher nem em que formato — e o ticket sai incompleto
ou errado, gerando retrabalho para quem gerencia as plataformas (o time de LLM Ops).

**A solução:** um agente conversacional que entende a intenção do colaborador em linguagem
natural, coleta apenas o que falta, valida o preenchimento e abre o ticket certo, no formato
certo — servindo também como **prova de valor**: cada solicitação vira um ticket rastreável.

---

## 🏗️ Arquitetura da aplicação

Monorepo com **três aplicações** e **um container de banco**, tudo orquestrado por um único
`docker-compose.yml`:

| Aplicação | Diretório | Stack | Porta |
|-----------|-----------|-------|-------|
| **Web** (UI + BFF) | `apps/web` | Next.js (App Router, TypeScript, Tailwind) | 3005 |
| **Agentes** | `apps/agents` | FastAPI + LangGraph + LiteLLM | 8002 |
| **Mock Gemud** (tickets) | `apps/mock-gemud` | FastAPI + SQLite | 8001 |
| **Postgres** (checkpointer) | `docker-compose.yml` | postgres:16-alpine | 5433 |

```
┌──────────────┐   POST /chat   ┌─────────────────────┐   POST /tickets   ┌───────────────┐
│   Web (UI)   │ ─────────────▶ │  Agentes (LangGraph) │ ────────────────▶ │  Mock Gemud   │
│ Chat + BFF   │                │  porteiro→espec→val  │                   │  (tickets)    │
└──────────────┘                └──────────┬──────────┘                   └───────┬───────┘
                                           │  checkpoint                         │
                                           ▼                                     ▼
                                   ┌───────────────┐                    ┌───────────────┐
                                   │   Postgres    │                    │    SQLite     │
                                   │  (estado)     │                    │  (tickets)    │
                                   └───────────────┘                    └───────────────┘
```

- A **Web** só faz proxy para os dois backends FastAPI — não tem banco próprio.
- Os **Agentes** orquestram a conversa num grafo LangGraph, com estado persistido no Postgres.
- O **Mock Gemud** persiste os tickets em SQLite (um arquivo local, zero container extra).

---

## 🤖 Arquitetura do agente

O coração do sistema é um **grafo LangGraph** com **gerenciamento de estado** e
**checkpointing**: a conversa é assíncrona e pode ser retomada a qualquer momento pelo
`thread_id`, sem perder o que já foi coletado.

### O grafo

```
┌──────────┐   classifica   ┌──────────────┐   coleta   ┌────────────┐   OK   ┌──────────────┐
│ Porteiro │ ─────────────▶ │ Especialista │ ─────────▶ │ Validador  │ ─────▶ │ abrir_ticket │
└──────────┘                └──────────────┘            └────────────┘        └──────────────┘
                                  ▲                           │
                                  └─────── falta campo ◀──────┘
```

1. **Porteiro** — classifica a plataforma alvo a partir da intenção do usuário
   (keyword rápida + fallback para LLM quando o texto é ambíguo).
2. **Especialista** — extrai os campos do ticket a partir de linguagem natural
   (regex para `campo: valor` + LLM para texto livre).
3. **Validador** — a *fonte da verdade*: confere os campos obrigatórios e seus formatos
   (ex.: `centro_custo` = 9 dígitos). Se algo falta, **volta ao especialista**; se está
   tudo certo, segue para abrir o ticket. O LLM sugere, o validador decide.
4. **abrir_ticket** — a tool que efetivamente abre o ticket no Mock Gemud.

### Estado

O estado (`OnboardingState`) carrega: `thread_id`, `messages`, `platform`, `fields`
(campos já coletados), `missing_fields`, `attempts` e `ticket_result`. Persistido num
checkpointer Postgres, permite retomar a conversa entre requisições HTTP.

### Tools

| Tool | Função |
|------|--------|
| `abrir_ticket` | Abre o ticket no Mock Gemud (`POST /tickets`) com os campos validados |

### Contrato declarativo

Os campos obrigatórios por plataforma vivem em `apps/agents/contracts/platforms.json`.
**Adicionar uma plataforma é config, não código** — basta um novo bloco com seus
`required_fields`.

### LLM plugável

A extração/classificação usa o **LiteLLM SDK**, então o provider é trocado por variável de
ambiente (`LLM_MODEL` / `LLM_API_BASE` / `LLM_API_KEY`) — sem refatorar o grafo.

---

## ▶️ Como executar (Docker)

```bash
docker compose up --build
```

Isso sobe os 4 serviços de uma vez. Abra **http://localhost:3005**.

> Precisa definir `LLM_API_KEY` (chave do seu provider de LLM) antes de subir — veja
> `.env.example` em `apps/agents`.

### Execução manual (sem Docker)

Cada app roda independente (para desenvolvimento):

```bash
# 1. Postgres
docker compose up -d postgres

# 2. Mock Gemud
cd apps/mock-gemud && uv sync && uv run uvicorn app.main:app --port 8001

# 3. Agentes (defina LLM_API_KEY em apps/agents/.env)
cd apps/agents && uv sync && uv run uvicorn app.main:app --port 8002

# 4. Web
cd apps/web && npm install && npm run dev -- --port 3005
```

### Uso

- Aba **Chat** — converse com o agente em linguagem natural (ex.: *"quero criar um agente
  no Gemini para o financeiro"*). Ele pede só o que faltar e abre o ticket.
- Aba **Tickets** — lista todos os tickets criados.

---

## 🧭 Estrutura do monorepo

```
apps/
  web/            # Next.js (UI + BFF) — abas Chat e Tickets
  agents/         # FastAPI + LangGraph — grafo porteiro→especialista→validador→tool
    app/
      controllers/  # grafo e orquestração
      models/       # schemas Pydantic + estado do grafo
      views/        # routers HTTP (POST /chat, GET /conversation/{id})
      tools/        # tool abrir_ticket
      contracts/    # platforms.json (declarativo)
      llm.py        # abstração LiteLLM
  mock-gemud/     # FastAPI + SQLite — CRUD de tickets
    app/
      controllers/  # serviço de tickets
      models/       # schema Ticket
      views/        # routers (POST/GET /tickets, GET /tickets/{id})
      db/           # SQLite
docker-compose.yml  # postgres + os 3 apps
```

---

## ⚙️ Variáveis de ambiente

| Variável | Serviço | Default | Descrição |
|----------|---------|---------|-----------|
| `LLM_MODEL` | agents | `openai/deepseek-v4-pro` | Modelo do LLM (LiteLLM) |
| `LLM_API_BASE` | agents | `https://ollama.com/v1` | URL base do provider |
| `LLM_API_KEY` | agents | — | Chave de API (obrigatória) |
| `MOCK_GEMUD_URL` | agents | `http://localhost:8001` | URL do serviço de tickets |
| `DATABASE_URL` | agents | `postgresql://onboarding:onboarding@localhost:5433/onboarding` | Postgres do checkpointer |
| `NEXT_PUBLIC_AGENTS_API_URL` | web | `http://localhost:8002` | URL dos agentes |
| `NEXT_PUBLIC_MOCK_GEMUD_API_URL` | web | `http://localhost:8001` | URL do Mock Gemud |

---

## 🧪 Testes

```bash
cd apps/agents && uv run pytest
cd apps/mock-gemud && uv run pytest
```

---

## 📋 Convenções

- Interface em português (pt-BR).
- Conventional Commits.
- TypeScript strict; Python com `uv` e type hints.
