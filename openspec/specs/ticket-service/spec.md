# ticket-service Specification

## Purpose
Provides the Mock Gemud ticket service: a declarative platform contract that defines required fields per platform, and a ticket API with SQLite persistence for creating and listing tickets.

## Requirements

### Requirement: Declarative platform contract

The service SHALL define, in a declarative contract (`contracts/platforms.json`), the list of known platforms and their required fields, so that adding a platform is configuration rather than code.

#### Scenario: Contract lists known platforms
- **WHEN** the system loads the platform contract
- **THEN** it exposes LiteLLM, LangFuse, and Gemini Enterprise with their respective required fields

#### Scenario: Adding a platform is config-only
- **WHEN** a new platform entry is added to `contracts/platforms.json`
- **THEN** the onboarding flow supports the new platform without code changes

### Requirement: Create a ticket

The service SHALL expose `POST /tickets` that accepts a ticket payload and persists it, returning the created ticket with an id.

#### Scenario: Valid ticket created
- **WHEN** a client posts a valid ticket to `/tickets`
- **THEN** the service stores it and returns the ticket with a generated id and all provided fields

#### Scenario: Invalid ticket payload
- **WHEN** a client posts a ticket missing required fields or with invalid field formats
- **THEN** the service returns a validation error and does not store the ticket

### Requirement: List tickets

The service SHALL expose `GET /tickets` that returns all stored tickets.

#### Scenario: List all tickets
- **WHEN** a client requests `GET /tickets`
- **THEN** the service returns all created tickets

### Requirement: Retrieve a single ticket

The service SHALL expose `GET /tickets/{id}` that returns the ticket with the given id.

#### Scenario: Ticket found
- **WHEN** a client requests `GET /tickets/{id}` for an existing id
- **THEN** the service returns that ticket

#### Scenario: Ticket not found
- **WHEN** a client requests `GET /tickets/{id}` for an id that does not exist
- **THEN** the service returns a not-found response

### Requirement: Persist tickets in SQLite

The service SHALL persist tickets in a local SQLite database so they survive process restarts.

#### Scenario: Tickets survive restart
- **WHEN** the service restarts
- **THEN** previously created tickets are still available via `GET /tickets`
