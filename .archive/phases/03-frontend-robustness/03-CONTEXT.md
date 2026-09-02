# Phase 3 Context: Frontend Robustness & State Sync

## Objective
Harden the React frontend against validation errors (FastAPI 422s) and fix the state synchronization bug where AI results are not correctly displayed in the Intelligence Feed.

## Locked Decisions

### D-01: Validation Feedback (Inline)
- **Decision:** Implement inline validation messages for the `Subject` and `Description` fields.
- **Rules:**
  - Subject: "Minimum 3 characters required" (red text if <3)
  - Description: "Minimum 10 characters required" (red text if <10)
- **Outcome:** Prevents backend 422 errors and provides immediate UX feedback.

### D-02: SSE Reducer & Key Mapping (State Sync)
- **Decision:** Refactor `usePipeline.tsx` reducer and `IntelligenceFeed.tsx` to use consistent keys that match the backend `type` fields exactly.
- **Mapping:**
  - Backend: `classification` -> State: `classification`
  - Backend: `triage`         -> State: `triage`
  - Backend: `rag`            -> State: `rag`
  - Backend: `resolution`     -> State: `resolution` (Fixing `resolve` mismatch)
  - Backend: `judge`          -> State: `judge`

### D-03: Rich Data Presentation (Rich Components)
- **Decision:** Move away from raw JSON dumps in `StageCard.tsx`.
- **Requirements:**
  - **Classification:** Render as a "Category Badge" + "Confidence %".
  - **Triage:** Render as "Priority Level" + "Routing Reason".
  - **RAG:** Render as a "Context Source Count" + snippet of the best match.
  - **Resolution:** Render as a numbered list of technical steps.
  - **Judge:** Render as a "Safety Verdict" + specific rubric scores.

### D-04: Animation Strategy (Holographic Reveal)
- **Decision:** Implement the blur-to-focus and staggered entrance animation for stage data.
- **Implementation:** Use `AnimatePresence` combined with `motion.div` targeting `initial={{ opacity: 0, height: 0, filter: 'blur(10px)' }}`.

## Technical Context
- **Vite Proxy:** Port 8001 (FastAPI).
- **Hooks:** `usePipeline` context provides the global pipeline state.
- **Libraries:** Framer Motion for motion, Tailwind for styling.
