# Tasks

## 1. Repository scaffolding

- [x] 1.1 Create monorepo root layout (README.md, apps/web, apps/agents, apps/mock-gemud) and verify directories exist
- [x] 1.2 Add Postgres Docker setup (docker-compose or Dockerfile) for the LangGraph checkpointer and verify `docker compose up` starts a healthy Postgres
- [x] 1.3 Write root README documenting how to start each app (mock-gemud, agents, web) and the Postgres container; verify the steps read end-to-end

## 2. Mock Gemud (FastAPI)

- [x] 2.1 Scaffold the `apps/mock-gemud` uv project with FastAPI and verify `uv sync` succeeds
- [x] 2.2 Define the `Ticket` model (models/) with common + platform fields and format validation; verify a unit test rejects an invalid `centro_custo`/`matricula_responsavel`
- [x] 2.3 Implement SQLite persistence (db/ + controllers/ ticket service) and verify tickets survive a restart via a test
- [x] 2.4 Implement routers (views/): `POST /tickets`, `GET /tickets`, `GET /tickets/{id}`; verify each endpoint returns expected results and 404 for a missing id

## 3. Agents backend (FastAPI + LangGraph)

- [ ] 3.1 Scaffold the `apps/agents` uv project with FastAPI + LangGraph and verify `uv sync` succeeds
- [ ] 3.2 Author `contracts/platforms.json` with common fields and per-platform required fields (LiteLLM, LangFuse, Gemini Enterprise); verify it parses and lists expected fields
- [ ] 3.3 Define the LangGraph state and Pydantic schemas (models/); verify state serializes/deserializes cleanly
- [ ] 3.4 Implement the graph (controllers/): porteiro, especialista, validador, and the validador→especialista conditional loop; verify a missing-field flow loops back and a complete flow exits
- [ ] 3.5 Implement the `abrir_ticket` tool (tools/) that POSTs to Mock Gemud; verify it creates a ticket when pointed at a running Mock Gemud
- [ ] 3.6 Wire Postgres checkpointing so conversations resume by thread_id; verify a second `POST /chat` with the same thread continues rather than restarting
- [ ] 3.7 Implement routers (views/): `POST /chat` and `GET /conversation/{thread_id}`; verify chat replies and history retrieval (including 404 for unknown thread)

## 4. Web UI + BFF (Next.js)

- [ ] 4.1 Scaffold `apps/web` (Next.js App Router, TypeScript strict, Tailwind) and verify `npm run build` succeeds
- [ ] 4.2 Add typed HTTP clients (lib/) for `/chat`, `/conversation/{thread_id}`, and `/tickets`; verify a request reaches a running backend
- [ ] 4.3 Build the "Chat" tab (components/) with pt-BR text; verify sending a message shows the agent's reply
- [ ] 4.4 Build the "Tickets" tab listing created tickets; verify it renders tickets returned by Mock Gemud

## 5. Integration & polish

- [ ] 5.1 Run the full flow end-to-end (web → agents → mock gemud → ticket listed) with all three apps and Postgres up; verify a ticket is created and appears in the Tickets tab
- [ ] 5.2 Confirm all UI text is pt-BR and code follows Conventional Commits / type hints; verify by review and a clean build
