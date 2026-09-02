# Roadmap

## Phase 1: Backend Extraction (API Bridge)

**Goal:** Create a FastAPI backend (`main.py`) that exposes the core ticket classification, RAG retrieval, and agent logic as RESTful endpoints, without immediately deleting the existing Streamlit app.

**Requirements:** API-01, API-02

**Rationale:** Establishing the API bridge allows the new React frontend to consume backend logic independently, laying the standard foundation for UI decoupling without breaking the existing monolithic setup during migration.

**Depends on:** Existing v3.0 core logic modules

**Success criteria:**
1. `main.py` created utilizing FastAPI framework.
2. Endpoint (e.g. `/api/ticket/process`) correctly triggers classification cascade and returns structured JSON output.
3. API is testable via Swagger UI/Docs or cURL without starting Streamlit.

**Status:** COMPLETE

---

## Phase 2: Frontend Scaffolding

**Goal:** Initialize the new UI architecture on the `frontend-v2` branch and establish the Vite/React/Tailwind foundation.

**Requirements:** UI-01, UI-02, UI-03

**Rationale:** Ensure base aesthetics, routing, and modern frontend tools (e.g., Tailwind CSS, Aceternity/Shadcn components) are structured properly before fully migrating functionality and hooking up API endpoints.

**Depends on:** Phase 1 (API Bridge) to test data endpoints

**Plans:** 4 plans
- [x] 02-01-PLAN.md — Setup & Nyquist Validation
- [x] 02-02-PLAN.md — Shell, HealthPulse & Mocks
- [x] 02-03-PLAN.md — Pipeline State & Command Console
- [x] 02-04-PLAN.md — Intelligence Feed & Visual Polish

**Success criteria:**
1. React + Vite project initializes successfully in `frontend-v2/` with passing Wave 0 tests.
2. Tailwind CSS, Shadcn UI, and Glassmorphism design system are functional.
3. Intelligence Feed rendering mocked pipeline states correctly according to the 5-stage logic.
4. HealthPulse, History, and Analytics sections contain high-fidelity mocked metrics and components.

**Status:** COMPLETE

---

## Phase 3: Frontend Robustness & State Sync

**Goal:** Implement client-side validation to prevent backend crashes and fix state management bugs where pipeline data is lost during the SSE stream.

**Requirements:** UI-04, UI-05

**Rationale:** Ensuring the UI is "crash-proof" against validation errors and that the intelligence feed correctly renders real-time data is critical for the "Elite" user experience before legacy code is removed.

**Depends on:** Phase 2 (Frontend Scaffolding)

**Plans:** 3 plans
- [x] 03-01-PLAN.md — Pipeline Logic Unification
- [x] 03-02-PLAN.md — The Validation Wall
- [x] 03-03-PLAN.md — Rich Visual Synthesis

**Success criteria:**
1. UI validation prevents "Launch" for tickets with <3 subject or <10 description chars.
2. React Reducer correctly persists SSE `result` payloads in the state.
3. `StageCard` components dynamically render AI data once the payload is received.

**Status:** COMPLETE

---

## Phase 4: Architectural Observability (The Nexus Blueprint)

**Goal:** Implement a dynamic "Nexus Blueprint" tab using Mermaid.js and a searchable Data Dictionary to visualize logic flows, term definitions, and file dependencies.

**Requirements:** UI-06, UI-07, UI-08

**Rationale:** To facilitate rapid debugging and future-proofing, the system must expose its inner workings (how centroids calculate, where terms are stored) in a visual, searchable format rather than just hidden in code.

**Depends on:** Phase 2 & 3

**Success criteria:**
1. Mermaid.js integrated and rendering a live "Execution Graph" of the 7-step pipeline.
2. Searchable "Term Inspector" maps logical concepts (e.g. "Novelty") to specific code lines and DB columns.
3. Interactive dependency graph shows file-level links across the v4.0 architecture.

**Status:** COMPLETE

---

## Phase 5: The Purge

**Goal:** Systematically remove Streamlit-related code, dependencies, and legacy python-based UI injections across the codebase once the React interface takes over.

**Requirements:** PURGE-01, PURGE-02

**Rationale:** Complete the decoupling by removing UI responsibilities completely from Python logic, enforcing the API-only architecture.

**Depends on:** Phase 2, 3 & 4

**Success criteria:**
1. `app.py` Streamlit entrypoint removed/archived.
2. Direct styling injections (e.g., `st.markdown`) successfully scrubbed from core logic files.
3. Heavy unneeded dependencies (Streamlit, Altair, Watchdog) pruned from `requirements.txt`.

**Status:** PLANNED

---

## Phase 6: Branch Convergence

**Goal:** Finalize the architectural change and stabilize the git repository with the 3-tier realm standard (`core`, `zenith`, `dao`/main).

**Requirements:** MERGE-01

**Rationale:** Integrate verified, decoupled changes from `frontend-v2` into the standard development stream, ensuring the multi-tier repo is ready for staging testing.

**Depends on:** Phase 5

**Success criteria:**
1. `frontend-v2` is successfully merged into the `core` branch.
2. Both Node/React app and FastAPI backend build/run commands are properly documented for developers working on the unified repository.

**Status:** PLANNED

---

## Summary

| # | Phase | Goal | Requirements | Success Criteria | Status |
|---|-------|------|--------------|------------------|--------|
| 1 | Backend Extraction | Expose core logic as REST API | API-01, API-02 | 3 | COMPLETE |
| 2 | Frontend Scaffolding | Build Vite/React/Tailwind Base UI | UI-01–03 | 4 | COMPLETE |
| 3 | Frontend Robustness | Fix Validation Wall & State Sync | UI-04–05 | 3 | COMPLETE |
| 4 | Nexus Blueprint | Architectural Observability | UI-06–08 | 3 | COMPLETE |
| 5 | The Purge | Remove Streamlit + dependencies | PURGE-01–02 | 3 | PLANNED |
| 6 | Branch Convergence | Merge `frontend-v2` to `core` | MERGE-01 | 2 | PLANNED |

---
*Roadmap updated: 2026-04-18*
*Milestone: v4.0 Architectural Decoupling & UI Modernization*
