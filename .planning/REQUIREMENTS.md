# Requirements: Nexus AI Ticket Intelligence Platform

**Defined:** 2026-04-18
**Core Value:** Every ticket gets classified, routed, and resolved with transparent confidence scoring and safety gates — completely decoupled via API to allow for elite modern UX.

## v4.0 Requirements - UI Decoupling & Architecture Modernization

Requirements for milestone v4.0. Each maps to roadmap phases to transition the platform to a modern React + FastAPI architecture.

### Backend Extraction
- [x] **API-01**: Wrap core Nexus functionality within a FastAPI service (`main.py`)
- [x] **API-02**: Core intelligence paths (classification cascade, RAG, evaluators) output pure JSON responses without embedded UI styling code

### Frontend Scaffolding
- [x] **UI-01**: Initialize Vite/React single-page application under `frontend-v2` branch/working space
- [x] **UI-02**: Configure Tailwind CSS alongside premium component libraries (Aceternity UI/Shadcn) for a high-end application aesthetic
- [x] **UI-03**: Create dashboard to process tickets, surfacing pipeline stage data accurately from the new API structure

### Frontend Robustness
- [x] **UI-04**: Implement client-side validation for ticket inputs to prevent 422 backend crashes
- [x] **UI-05**: Ensure React state correctly captures and renders SSE result payloads across all pipeline stages (COMPLETE: State sync unified in 03-01, Rich UI in 03-03)

### Architectural Observability
- [x] **UI-06**: Integrate Mermaid.js to visualize live execution flows
- [x] **UI-07**: Build a searchable "Term Inspector" glossary of core logic concepts
- [x] **UI-08**: Display file-level dependency mapping within the UI

### The Purge
- [ ] **PURGE-01**: Remove Streamlit application (`app.py`), archiving functionality securely into legacy if needed
- [ ] **PURGE-02**: Clean `requirements.txt` of all presentation-layer Python libraries (Streamlit, Altair, etc.)

### Branch Convergence
- [ ] **MERGE-01**: Bring `frontend-v2` work into the core git flow supporting the `core` / `zenith` / `main` environment architecture.

## Deferred / Future Requirements (v5.0+)

### Learning Loop
- **LEARN-01**: System retrains classification centroids from feedback table corrections
- **LEARN-02**: System adjusts confidence thresholds based on override patterns

### Enterprise Integration
- **INTEG-01**: System ingests tickets from ServiceNow / Jira Service Management APIs

### Advanced Agents
- **AIOPS-01**: AIOps agent correlates tickets with observability signals
- **SELFHEAL-01**: Self-healing agent applies known remediations automatically

## Previous Milestones (v3.0) - Completed

### Calibration, Cascade, & Enhanced RAG
- ✓ **CALIB-01**: System validates classifier confidence bands
- ✓ **FDBK-01**: System stores pipeline run feedback in SQLite
- ✓ **CASC-01 to CASC-04**: Fast path, LLM judge, and novelty escalation functioning
- ✓ **RANK-01 to RANK-02**: Chunk ranking enabled
- ✓ **MHOP-01 to MHOP-02**: Multi-hop semantic traversal

### Agentic Workflows & Safety
- ✓ **TRIAGE-01 to TRIAGE-02**: TriageAgent rationale routing
- ✓ **RESOLVE-01 to RESOLVE-02**: ResolutionAgent JSON structures
- ✓ **AUTODISC-01 to AUTODISC-02**: AutomationDiscoveryAgent checks for pattern repetitions
- ✓ **JUDGE-01 to JUDGE-04**: LLM Judge evaluates responses with hard gating for safety

## Out of Scope

| Feature | Reason |
|---------|--------|
| Microservices architecture | Keep the backend monolithic for the prototype while decoupling frontend |
| GraphQL API | Standard RESTful API covers all basic requirement states |

## Traceability

| Requirement | Phase (v4.0) | Status |
|-------------|--------------|--------|
| API-01      | Phase 1      | COMPLETE |
| API-02      | Phase 1      | COMPLETE |
| UI-01       | Phase 2      | COMPLETE |
| UI-02       | Phase 2      | COMPLETE |
| UI-03       | Phase 2      | COMPLETE |
| UI-04       | Phase 3      | COMPLETE |
| UI-05       | Phase 3      | COMPLETE |
| UI-06       | Phase 4      | COMPLETE |
| UI-07       | Phase 4      | COMPLETE |
| UI-08       | Phase 4      | COMPLETE |
| PURGE-01    | Phase 5      | PLANNED |
| PURGE-02    | Phase 5      | PLANNED |
| MERGE-01    | Phase 6      | PLANNED |

---
*Last updated: 2026-04-18 after Milestone 4.0 initialization*
