# web-ui Specification

## Purpose
Provides the web UI (with a BFF) through which employees converse with the onboarding agent and view the tickets they have created, with all interface text in Brazilian Portuguese.

## Requirements

### Requirement: Chat tab

The UI SHALL provide a "Chat" tab where the user can send messages to the onboarding agent and see the agent's replies.

#### Scenario: Send a message to the agent
- **WHEN** the user types a message in the Chat tab and sends it
- **THEN** the message is forwarded to the agents backend and the agent's reply is displayed

#### Scenario: Conversation continues across messages
- **WHEN** the user sends multiple messages in the same chat session
- **THEN** the agent keeps the conversation context via the thread id

### Requirement: Tickets tab

The UI SHALL provide a "Tickets" tab that lists the tickets created by the current user.

#### Scenario: List created tickets
- **WHEN** the user opens the Tickets tab
- **THEN** the UI shows the list of created tickets retrieved from the mock Gemud backend

### Requirement: Backend proxy (BFF)

The UI SHALL act only as a proxy to the agents and mock Gemud backends, holding no database of its own.

#### Scenario: UI proxies requests
- **WHEN** the UI needs to chat or list tickets
- **THEN** it forwards the request to the corresponding FastAPI backend and renders the response

### Requirement: Portuguese interface

All user-facing UI text SHALL be in Brazilian Portuguese (pt-BR).

#### Scenario: Interface language
- **WHEN** the user interacts with the UI
- **THEN** all labels, buttons, and messages are displayed in Brazilian Portuguese
