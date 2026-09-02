# Phase 4 Research: Architectural Observability (The Nexus Blueprint)

**Researched:** 2026-04-19
**Status:** COMPLETE
**Confidence:** HIGH

## 1. Intelligence Pipeline Mapping (The 7 Steps)
The master orchestrator logic resides in `api/routes/pipeline.py`.

| Step | Component | Function | File |
|:--- | :--- | :--- | :--- |
| **1. Classify** | `TicketClassifier` | `.classify()` | `core/classifier.py` |
| **2. Triage** | `TriageAgent` | `.run()` | `core/agent.py` |
| **3. RAG Retrieval** | `ResolutionEngine` | `.suggest_resolution()` | `core/rag.py` |
| **4. Ranking** | `ResolutionEngine` | `._rank_retrieved_chunks()` | `core/rag.py` |
| **5. Resolution** | `ResolutionAgent` | `.run()` | `core/agent.py` |
| **6. Judge** | `ResolutionJudge` | `.judge()` | `core/judge.py` |
| **7. Automation** | `AutomationDiscoveryAgent` | `.run()` | `core/agent.py` |

## 2. Storage & Metadata Map (Term Inspector)
Every core term in the system maps to specific persistent storage.

- **`feedback.db` (SQLite):** Stores `category`, `confidence`, `resolution_steps`, `judge_scores`, and `agent_action`.
- **ChromaDB (Local):** Stores embedded document content and metadata (`category`, `priority`, `resolution`, `department`).

## 3. Frontend Visualization Strategy
- **Library:** `beautiful-mermaid` (v1.1.3).
- **Interactivity:** We will use standard Mermaid `graph TD` definitions. 
- **Contextual Zoom:** When a user searches a term, we will use `container.querySelectorAll('.node')` to apply CSS classes that highlight relevant nodes and dim the rest. This avoids expensive Mermaid re-renders.

## 4. Dependencies
- **Entry:** `App.tsx` -> `usePipeline.tsx` -> `GET /api/pipeline/stream`.
- **Core:** `pipeline.py` is the central hub, importing all `core/` modules.
- **Models:** `api/models.py` defines the Pydantic contracts for the entire flow.
