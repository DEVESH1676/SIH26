# Phase 4 Context: Architectural Observability (The Nexus Blueprint)

## Objective
Implement a dynamic "Nexus Blueprint" tab in the React frontend to expose the system's inner workings through real-time Mermaid.js diagrams and a searchable term glossary. This ensures the platform is self-documenting and facilitates rapid debugging.

## Locked Decisions

### D-01: UI Integration - Nav Tab
- **Decision:** The Blueprint will live in its own dedicated navigation tab.
- **UX:** Switching to the Blueprint tab swaps the main view from "Operations" to "Architecture".

### D-02: Data Strategy - Dynamic API
- **Decision:** All architectural metadata will be served via a new `/api/blueprint` endpoint in FastAPI.
- **Rationale:** This ensures the "latest workflow" is always displayed. The backend will define the Mermaid graph strings and term definitions as the single source of truth.

### D-03: Diagram Interactivity - Contextual Zoom
- **Decision:** The UI will implement "Contextual Zooming" for diagrams.
- **Feature:** Searching for a term in the glossary will automatically highlight relevant nodes in the Mermaid diagram and dim non-related paths using CSS selectors on the generated SVG.

### D-04: The Term Inspector (Metadata Map)
- **Requirement:** Every core term (e.g., "Confidence," "Centroid") must provide a map to its:
    - **Logical Meaning**: Business definition.
    - **Code Implementation**: Specific file and function (e.g., `classifier.py -> _calculate()`).
    - **Storage Location**: Database table and column.

## Downstream Guidance
- **Researcher:** 
    - Investigate how to apply dynamic CSS classes to Mermaid.js SVG outputs in React.
    - Identify all 7 pipeline steps' code paths and storage columns for the initial API data.
- **Planner:** 
    - Task 1: Build the `/api/blueprint` FastAPI router.
    - Task 2: Implement the `MermaidCanvas` and `TermInspector` React components.
    - Task 3: Integrate the new tab and search-trigger-highlight logic.
