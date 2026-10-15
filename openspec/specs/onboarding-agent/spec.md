# onboarding-agent Specification

## Purpose
Guides employees through the onboarding flow to open an access ticket on the correct AI platform, using a multi-agent graph that classifies the platform, collects required fields, validates them, and opens the ticket.

## Requirements

### Requirement: Classify target platform

The agent SHALL determine which platform the ticket targets based on the user's request, and SHALL resolve it to one of the known platforms (LiteLLM, LangFuse, Gemini Enterprise) before collecting platform-specific fields.

#### Scenario: Known platform requested
- **WHEN** a user asks to open a ticket and names a known platform (e.g. "quero acesso ao LiteLLM")
- **THEN** the agent proceeds to collect the fields for that platform

#### Scenario: Ambiguous or unknown platform
- **WHEN** the user does not name a platform or names one that is not in the contract
- **THEN** the agent asks the user to clarify the platform before continuing

### Requirement: Collect common required fields

The agent SHALL collect the common identification fields for the coordenação before opening a ticket: `nome_coordenacao`, `centro_custo`, and `matricula_responsavel`.

#### Scenario: Common fields collected
- **WHEN** the agent has identified the platform
- **THEN** it asks for `nome_coordenacao`, `centro_custo`, and `matricula_responsavel`

### Requirement: Collect platform-specific required fields

The agent SHALL collect the required fields specific to the target platform, as declared in the platform contract.

#### Scenario: LiteLLM fields
- **WHEN** the target platform is LiteLLM
- **THEN** the agent collects `ambiente`, `modelos`, and `limite_tokens`

#### Scenario: LangFuse fields
- **WHEN** the target platform is LangFuse
- **THEN** the agent collects `nome_projeto`, `ambiente`, and `limite_trace_mensal`

#### Scenario: Gemini Enterprise fields
- **WHEN** the target platform is Gemini Enterprise
- **THEN** the agent collects `nome_agente`, `descricao`, and `nivel_acesso`

### Requirement: Validate required fields before opening a ticket

The agent SHALL validate that all required fields (common and platform-specific) are present and well-formed before opening the ticket, and SHALL return to field collection when any are missing or invalid.

#### Scenario: Missing fields
- **WHEN** validation detects one or more missing or invalid required fields
- **THEN** the agent returns to field collection and asks only for the missing fields

#### Scenario: All fields valid
- **WHEN** all required fields are present and valid
- **THEN** the agent proceeds to open the ticket

### Requirement: Validate field formats

The agent SHALL enforce field formats: `centro_custo` MUST be exactly 9 digits and `matricula_responsavel` MUST be exactly 10 digits.

#### Scenario: Invalid centro_custo length
- **WHEN** the user provides a `centro_custo` that is not 9 digits
- **THEN** the agent rejects it and asks for a valid value

#### Scenario: Invalid matricula_responsavel length
- **WHEN** the user provides a `matricula_responsavel` that is not 10 digits
- **THEN** the agent rejects it and asks for a valid value

### Requirement: Open ticket via tool

The agent SHALL open the ticket by invoking the ticket-opening tool once validation succeeds.

#### Scenario: Ticket opened
- **WHEN** all required fields are valid
- **THEN** the agent invokes the ticket tool and confirms to the user that the ticket was created

### Requirement: Chat API

The backend SHALL expose `POST /chat` that accepts a user message (and an optional thread id) and returns the agent's reply, and `GET /conversation/{thread_id}` that returns the conversation history for a thread.

#### Scenario: Send a chat message
- **WHEN** a client posts a message to `/chat`
- **THEN** the backend returns the agent's next response

#### Scenario: Retrieve conversation
- **WHEN** a client requests `GET /conversation/{thread_id}` for an existing thread
- **THEN** the backend returns that thread's conversation history

#### Scenario: Unknown thread
- **WHEN** a client requests `GET /conversation/{thread_id}` for a thread that does not exist
- **THEN** the backend returns a not-found response

### Requirement: Resume conversation across requests

The agent SHALL persist conversation state (checkpointing) so a conversation can resume across separate requests using a thread id.

#### Scenario: Resume after interruption
- **WHEN** a user resumes a conversation with an existing thread id
- **THEN** the agent continues from the previously saved state rather than starting over
