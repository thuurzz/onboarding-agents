# Design

## Context

Greenfield monorepo (no application code yet). Three apps plus one Docker container for Postgres.
See proposal.md for the motivation and specs/ for the behavioral requirements. Python apps use `uv`;
the UI uses Next.js App Router with TypeScript strict mode and Tailwind. All UI text is pt-BR.

## Goals / Non-Goals

**Goals:**
- Demonstrate the porteiro → especialista → validador → tool LangGraph flow end-to-end.
- Keep platform onboarding logic declarative (contracts/platforms.json), so new platforms require no code.
- Keep each app independently runnable on the host, with Postgres as the only container.

**Non-Goals:**
- Real authentication/authorization of employees.
- Integration with a real Gemud/IT system (Mock Gemud is in-memory SQLite only).
- Production hardening (retries, observability beyond checkpointing, migrations, CI).

## Decisions

### Monorepo layout
Three top-level app directories: `apps/web` (Next.js), `apps/agents` (FastAPI + LangGraph),
`apps/mock-gemud` (FastAPI). Rationale: matches the three-app framing; keeps per-app tooling isolated.

### LangGraph graph structure
- `porteiro` classifies the platform (LLM call) and stores it in state.
- `especialista` collects/updates field values from the latest user message into state.
- `validador` checks common + platform-specific required fields and their formats against the contract.
- Conditional edge: missing/invalid fields → loop back to `especialista`; otherwise → `abrir_ticket` tool.
- `abrir_ticket` POSTs to Mock Gemud and stores the resulting ticket id/status in state.
- Rationale: the loop is expressed as a conditional edge, not recursion, keeping the graph deterministic.

### State model (Pydantic + LangGraph)
A single `OnboardingState` TypedDict/Pydantic model carrying: `thread_id`, `messages`, `platform`,
`fields` (dict of collected values), `missing_fields`, and `ticket_result`. Rationale: keeps the
checkpointer-serializable state minimal and explicit.

### Checkpointing in Postgres
Use the LangGraph Postgres checkpointer backed by a Dockerized Postgres, with a single container.
Rationale: async conversation resume across `POST /chat` requests via `thread_id`. SQLite is used only
by Mock Gemud; the agents backend does not use SQLite.

### Declarative contract
`apps/agents/contracts/platforms.json` lists platforms, each with `required_fields` (platform-specific).
Common fields (`nome_coordenacao`, `centro_custo`, `matricula_responsavel`) are defined once and merged
with platform fields. Rationale: single source of truth shared by validador and especialista; the Mock
Gemud validation mirrors the same field list (via its own `Ticket` schema) but the contract stays in the
agents app.

### BFF proxying
The Next.js app has no database. `lib/` holds typed HTTP clients for `/chat`, `/conversation/{thread_id}`
and `/tickets`; API routes proxy requests to the two FastAPI backends. Rationale: keeps backend URLs and
auth out of the browser and centralizes error handling.

### Mock Gemud persistence
Single SQLite file under the app directory, opened via a small `db/` module with no ORM (stdlib `sqlite3`
or a light driver). Rationale: zero extra container, easy to reset for the MVP.

## Risks / Trade-offs

- **LLM nondeterminism in porteiro/especialista** → constrain prompts to enumerate platforms/fields; treat
  the validador as the source of truth rather than relying on LLM output alone.
- **Postgres as a hard dependency for checkpointing** → document container startup clearly in the root
  README; fail fast with a clear error if the DB is unreachable.
- **Single shared contract vs. two validation sites (agents + mock gemud)** → risk of drift; mitigate by
  keeping Mock Gemud's validation minimal (required fields + formats) and the agents app authoritative.
- **SQLite write concurrency** → acceptable for an MVP; single-process Mock Gemud avoids locks.

## Migration Plan

Greenfield: no migration. Stand up Postgres via Docker, then start `mock-gemud`, `agents`, and `web` in
that order (documented in the root README). No rollback needed beyond dropping the container/volume.
