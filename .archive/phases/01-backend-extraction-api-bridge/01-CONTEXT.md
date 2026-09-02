# Phase 1: Backend Extraction (API Bridge) - Context

**Gathered:** 2026-04-18
**Status:** Ready for planning

<domain>
## Phase Boundary

Wrap the classification cascade, RAG system, agent workflows, and judgement mechanisms into a standard RESTful API using FastAPI without breaking the existing Streamlit app.
</domain>

<decisions>
## Implementation Decisions

### API Routing Structure (Hybrid Orchestration)
- Implement a **Master Orchestrator** (`/pipeline/run`) as the primary endpoint for the React frontend, handling the full 5-Mode Agentic Decision Tree in a single trip.
- Implement **Modular Endpoints** (`/classify`, `/retrieve`, `/verify`) for granular testing, security audits, and Human-in-the-loop overrides.

### Data Contracts (I/O)
- Use **strongly typed Pydantic models** for all inputs and outputs.
- Define a `TicketResponse` model that includes a `decisions` list and a `metadata` dictionary for RAG evidence.
- Rely on FastAPI's automatic Swagger documentation to satisfy "Technical Feasibility" assessment criteria.

### Response Handling (SSE)
- Utilize **Server-Sent Events (SSE)** for the main pipeline endpoint (`/pipeline/stream` or similar) to stream real-time progression status (e.g., "Extracting embeddings...", "Searching vector DB...") directly matching the existing Streamlit state updates.

### Escalation Formatting
- API will ALWAYS return `200 OK` but explicitly use a `decision_mode` field inside the JSON payload to differentiate states.
- Auto-Resolve mode payload includes `resolution_steps` array.
- Escalate mode payload includes `escalation_summary` and `target_tier`.
- Clarification mode (triggered if confidence < 0.75) prompts for more information.

### Code Preservation Guarantee
- **Absolute requirement:** Existing backend intelligence code (e.g., `core/classifier.py`, `core/rag.py`, `core/agent.py`) must be WRAPPED and IMPORTED, not rewritten. All previously built intelligence paths are retained.
</decisions>

<canonical_refs>
## Canonical References

No external specs — requirements are fully captured in decisions above. Downstream planners must ensure existing core modules remain untouched algorithmically.

</canonical_refs>

<specifics>
## Specific Ideas

- The user specified that they are a Computer Engineering student and this project serves as a technical assessment. The FastAPI Swagger UI will be used as a "Technical Feasibility" win.
- SSE streams must reflect the exact "Intelligence Pipeline" steps currently shown in the monolithic Streamlit app.
</specifics>

<deferred>
## Deferred Ideas

- None — discussion stayed within phase scope.
</deferred>

---

*Phase: 01-backend-extraction-api-bridge*
*Context gathered: 2026-04-18*
