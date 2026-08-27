# Phase 4 Plan: Architectural Observability (The Nexus Blueprint)

## Goal
Establish a high-fidelity "Blueprint" tab that visualizes the system's execution flow and provides a searchable dictionary of logical terms and dependencies.

## Tasks

### 4.1 Integration of Mermaid.js (UI-06)
- **Action:** Install and configure `mermaid` and `react-mermaid` (or a custom wrapper) in `frontend-v2`.
- **Action:** Create a `Mermaid` component to handle dynamic diagram rendering with custom glassmorphism styles.
- **Verification:** Successfully render a static "Hello World" diagram in the UI.

### 4.2 Blueprint Data Definition (UI-07)
- **Action:** Create `frontend-v2/src/config/blueprint.ts` containing the mapping of terms, logic flows, and file dependencies.
- **Logic Mapping:** Map the 7 steps: Classify -> Triage -> RAG -> Rank -> Resolve -> Judge -> Automate.
- **Verification:** The file exports a valid TypeScript object containing at least 10 core system terms.

### 4.3 The "Nexus Blueprint" Tab (UI-08)
- **Action:** Build the `Blueprint` component with a dual-pane layout:
    - **Left Pane:** Search bar + Filterable List of terms/files.
    - **Right Pane:** Dynamic Mermaid diagram showing the selected flow or dependency map.
- **Action:** Integrate the Blueprint tab into the `MainLayout` or `CommandCenter`.
- **Verification:** Users can search for "Confidence" and see the diagram update to highlight the classification logic.

## Verification
- **Automated:** `npm --prefix frontend-v2 run build` passes without errors.
- **Manual:** Navigate to the "Blueprint" tab, search for a term, and verify the Mermaid diagram renders and highlights correctly.
