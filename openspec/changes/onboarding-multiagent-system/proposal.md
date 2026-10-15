# Proposal

## Why

Employees need access to AI platforms (LiteLLM, LangFuse, Gemini Enterprise) but the onboarding
process — figuring out which platform, collecting the right fields, and opening the access ticket —
is manual and error-prone. This MVP demonstrates a multi-agent architecture that guides the employee
through that flow and opens the ticket automatically.

## What Changes

- **New Next.js app (UI + BFF)**: two tabs — "Chat" (converse with the onboarding agent) and "Tickets"
  (list created tickets). Acts purely as a proxy to the two FastAPI backends; no own database.
- **New FastAPI + LangGraph agents backend**: MVC layout (`models/`, `controllers/`, `views/`, `tools/`,
  `contracts/`) exposing `POST /chat` and `GET /conversation/{thread_id}`. Implements the
  porteiro → especialista → validador → tool graph with a validador→especialista loop, checkpointing
  in Postgres (Docker) for async resume.
- **New Mock Gemud FastAPI backend**: MVC layout with a `Ticket` schema and SQLite persistence,
  exposing `POST /tickets`, `GET /tickets`, `GET /tickets/{id}`.
- **Declarative platform contract** (`contracts/platforms.json`) driving required fields per platform,
  so adding a platform is config, not code.
- **Root README** documenting how to start each app, plus Python tooling via `uv` and Conventional Commits.

## Capabilities

### New Capabilities

- `onboarding-agent`: the LangGraph multi-agent conversation flow (porteiro classifies the platform,
  especialista collects fields, validador checks required fields, tool opens the ticket) and its HTTP
  surface (`POST /chat`, `GET /conversation/{thread_id}`) with Postgres checkpointing.
- `ticket-service`: the Mock Gemud ticket API (`POST /tickets`, `GET /tickets`, `GET /tickets/{id}`)
  with SQLite persistence and the declarative `contracts/platforms.json` that defines required fields.
- `web-ui`: the Next.js UI + BFF with Chat and Tickets tabs that proxy to the two backends.

### Modified Capabilities

<!-- None: this is a greenfield project with no existing specs. -->

## Impact

- New monorepo layout with three apps (Next.js, agents FastAPI, mock-gemud FastAPI).
- New Postgres Docker container for LangGraph checkpointing.
- Dependencies: Next.js/TypeScript/Tailwind (UI), FastAPI + LangGraph + LangGraph Postgres checkpointer
  (agents), FastAPI + SQLite (mock gemud), `uv` for both Python apps.
- No changes to existing code (project currently has no application code).
