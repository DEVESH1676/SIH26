# Phase 2: Frontend Scaffolding - Context

**Gathered:** 2026-04-18
**Status:** Ready for planning

<domain>
## Phase Boundary

Initialize a modern React + Vite + Tailwind frontend foundation for the decoupled Nexus AI app. This phase establishes the new UI architecture, premium visual system, mocked product surfaces, and API-ready state flow for ticket submission and dashboard rendering against the Phase 1 FastAPI contract.
</domain>

<decisions>
## Implementation Decisions

### D-01: App Structure - Single-Page Intelligence Feed
- Replace the old tabbed model with a **single-page progressive disclosure** layout.
- Keep the established 5-stage pipeline logic, but present it as a vertically scrolling **Intelligence Feed** rather than separate pages.
- The pill navbar remains, but it acts as **section navigation** into the feed instead of route-level navigation.
- The core flow to preserve is still: Classify -> Triage -> RAG -> Resolve -> Judge.

### D-02: Landing Layout - Balanced Hybrid
- Above the fold should show a **split view** with:
- Left: a submission-focused hero / command center.
- Right: a high-level **System Health Pulse** panel.
- This must communicate that Nexus AI is an agentic operations console, not just a form.
- History and analytics live **below the fold** so the top of the page stays focused while still supporting high data density as users scroll.

### D-03: Submission Experience - Command Center Workspace
- Use a **same-screen split workspace** as the default operating mode.
- Left panel contains the active submission form and **live terminal-style logs**.
- Right panel contains **holographic result cards** that materialize as stages complete.
- The submission workspace should remain accessible while results are revealed; the user should not be pushed to a separate page for normal operation.

### D-04: Realtime Behavior - SSE First
- The React frontend must treat **SSE streaming** as the primary interaction model for pipeline runs.
- Consume the Phase 1 stream endpoint with a dedicated pipeline state layer rather than a one-shot request/response flow.
- Use the `0.0` to `1.0` stream progress values to drive a glowing frosted-glass progress bar.
- Each stage result should animate into view as stream events arrive, reinforcing the "alive" system feel.

### D-05: Navbar Behavior - Status-Aware Pill Navigation
- The pill navbar must support **scroll-to-section**, **active section tracking**, and **compact status indicators**.
- Use viewport tracking to keep the current section highlighted as the user moves through the intelligence feed.
- While a stage is processing, its pill can show a subtle pulse/spinner.
- Once a stage completes, the pill should shift to a soft success state to indicate the confidence-calibrated path is clear.

### D-06: Mock Scope - Full Experience Scaffolding
- For this phase, mock more than the ticket form.
- Include mocked states for:
- The live workflow surface.
- Recent run history.
- High-level analytics / system cards.
- This is required to validate the new layout, motion system, and glassmorphism treatment across the full page before all live wiring is complete.

### D-07: State Management - Pipeline Nerve Center
- Implement a custom `usePipeline` hook for SSE consumption and pipeline orchestration.
- Use `useReducer` to track stage status, progress, incoming payloads, and log messages across the pipeline.
- Maintain a logs collection in state to power the live terminal-style feed.
- Design state so mocked mode and real API mode can share the same UI contracts.

### D-08: Component and Styling Stack
- Use **Shadcn UI** for foundational application primitives such as inputs, cards, sheets, and data display.
- Use **Aceternity UI** selectively for premium hero/background treatments where it materially supports the visual direction.
- Define the glassmorphism material as a reusable design primitive in Tailwind/CSS variables so the feed, cards, pills, and system panels share one coherent surface language.

### D-09: Motion Language
- Use **Framer Motion** for stage reveal, blur-to-focus transitions, and live-response choreography.
- Motion should emphasize progression through the intelligence pipeline, not decorative motion for its own sake.
- The "Resolution Fabric" should feel continuous across hero, logs, result cards, history, and analytics states.

### D-10: API and Type Safety
- Keep the frontend aligned to the FastAPI backend contract through generated TypeScript types from the OpenAPI schema.
- Configure the Vite dev server to proxy `/api` locally so development matches production-style paths and avoids CORS friction.
- Planning should assume the Phase 1 API is the canonical contract for streaming and structured stage payloads.

### Restored Collaborator Context - Original Technical Decisions
- The original collaborator-authored technical decisions are preserved below in their original wording and heading structure instead of being summarized away.

#### State Management (The "Nerve Center")
- **SSE Consumption:** Implement a custom `usePipeline` hook utilizing the browser's native `EventSource` API to consume the `/api/pipeline/stream` endpoint.
- **Reducer Pattern:** Use `useReducer` to manage the multi-stage state (Classify -> Triage -> RAG -> Resolve -> Judge), tracking progress values (0.0-1.0) and incoming data objects per stage.
- **Live Logs:** Maintain a "logs" array in state to append real-time progress messages, surfacing autonomous reasoning as it happens.

#### UI Architecture (The "Elite Shell")
- **Component Stack:**
- **Aceternity UI:** Used for high-end "Hero" components and the dynamic Aurora background.
- **Shadcn UI:** Used for functional utility components (inputs, cards, modals).
- **UX Flow:** Transition from tabs to a **Step-Aware Dashboard**. Components (e.g., RAG Evidence) will "unfold" or slide into view only after their corresponding backend logic finishes.

#### Styling & Animation (The "Aurora Breathing")
- **Performance Animation:** Use **Framer Motion** combined with Tailwind arbitrary values to animate gradient "blobs" for the aurora effect, ensuring zero CPU spikes.
- **Glassmorphism Standard:** Define a custom Tailwind plugin for a unified "Glass" material: `backdrop-filter: blur(20px)`, `background: rgba(255, 255, 255, 0.03)`, and `1px` subtle borders.
- **Holographic Accents:** Implement `animate-gradient-xy` for holographic linear-gradient borders on status buttons.

#### Integration & Type Safety
- **Single Source of Truth:** Use `openapi-typescript` to auto-generate TypeScript interfaces from the FastAPI Pydantic models.
- **Dev Proxy:** Configure Vite dev server to proxy `/api` requests to `localhost:8001` to eliminate CORS issues and mirror production pathing.

#### Precedence Rule
- When there is tension between this restored collaborator context and the newer D-01 through D-10 decisions above, the newer decisions take precedence only where they directly conflict.

### the agent's Discretion
- Exact component naming and folder layout inside the React app.
- Exact Framer Motion easing curves and timing.
- Exact visual treatment of the System Health Pulse cards.
- Exact badge colors as long as they stay within the established premium glass / indigo-blue aesthetic.
</decisions>

<specifics>
## Specific Ideas

- The app should feel like an **agentic operations center**, not a static form workflow.
- The right-hand result surface should read like a **holographic intelligence board** as stage cards appear.
- The left-hand side should feel like a **command console**, with the ticket form and live log feed always nearby.
- The navigation should feel intelligent: pills react to processing state, completion state, and viewport position.
- The historical v3 Streamlit experience is a product reference for pipeline visibility, but not for page structure.
- The UI must feel "alive" and modern, matching the HP Omen 16 user experience.
- The "Technical Feasibility" win is reinforced by the use of SSE and auto-generated type safety.
</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase and milestone definition
- `.planning/ROADMAP.md` — Phase 2 goal, dependencies, and success criteria
- `.planning/REQUIREMENTS.md` — UI-01 through UI-03 requirements for the React frontend
- `.planning/phases/01-backend-extraction-api-bridge/01-CONTEXT.md` — locked backend contract assumptions for the React frontend, especially SSE-first interaction

### Existing product behavior and visual precedent
- `app.py` — current 5-stage Streamlit pipeline UX, progressive disclosure content, and data presentation model
- `.planning/phases_archive_v3/06-unified-ui/06-CONTEXT.md` — prior decision to expose all 5 pipeline stages clearly
- `.planning/phases_archive_v3/07-glassmorphism-ui/07-CONTEXT.md` — locked premium visual language and glassmorphism direction that should inform the React migration
- `https://ui.aceternity.com/` — canonical reference for Aceternity UI
- `https://ui.shadcn.com/` — canonical reference for Shadcn UI
- `https://www.framer.com/motion/` — canonical reference for Framer Motion

### Local workflow / workspace constraints
- `.agents/rules/workspace.md` — verify filesystem state before file operations because multiple agents may be working concurrently
- `.agents/rules/progress.md` — progress tracking and `tillnow.md` update expectations
- `.agents/rules/phase.md` — phase-driven execution and documentation expectations
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `app.py` — provides the current stage-by-stage UX, content groupings, and the specific result surfaces that need to be re-expressed in React
- Phase 1 FastAPI work — provides the SSE stream and structured JSON contracts the React state layer should consume

### Established Patterns
- The product already favors **progressive disclosure** of the intelligence pipeline rather than a hidden black-box output
- The visual direction is already biased toward **premium glassmorphism**, animated depth, and high-contrast operator-console aesthetics
- Session-driven UI state exists today in Streamlit (`st.session_state.pipeline_result` / history); React needs an equivalent app-state layer rather than ad hoc component state

### Integration Points
- The frontend should integrate directly with the Phase 1 `/api` contract, especially the pipeline streaming route
- Mock data should mirror the real backend payload shapes so the mock-first scaffolding does not create a second incompatible data model
- Navbar state, feed sections, logs, and stage cards should all derive from one shared pipeline state source
</code_context>

<deferred>
## Deferred Ideas

- Advanced live observability beyond the high-level System Health Pulse
- Full production analytics accuracy and real historical persistence
- Additional capabilities outside the Phase 2 scope, such as new ticket-management features not already implied by the current pipeline
</deferred>

---

*Phase: 02-frontend-scaffolding*
*Context gathered: 2026-04-18*
