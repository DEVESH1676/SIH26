# Phase 2 Validation Framework

## Domain Boundaries
- **Frontend Core:** Vite, React, TypeScript, Vitest.
- **Visual Design:** Glassmorphism, Tailwind v4, Aurora animations, Framer Motion.
- **Realtime Integration:** SSE Hooks, HealthPulse metrics.

## Invariants
- **SSE Connection Management:** SSE connection MUST close on unmount to prevent resource leaks (T-02-04 mitigation).
- **GPU Acceleration:** Aurora background and motion-heavy components MUST use GPU acceleration via `will-change: transform` or `will-change: opacity`.
- **Metrics Standard:** HealthPulse MUST use Recharts for consistent metric visualization.
- **Type Safety:** All API interactions MUST use Zod-validated schemas or generated TypeScript types.

## Verification Dimensions

### D4: Realtime Behavior (SSE)
- **Constraint:** Pipeline updates must reflect in UI within 200ms of event reception.
- **Test:** `pipeline.test.ts` stubs for event handling logic.

### D8: Glassmorphism Standard
- **Constraint:** Glass components must have `backdrop-blur-xl`, `bg-white/5` (or dark equivalent), and `border-white/10`.
- **Manual Verification:** UI inspection of the Elite Dashboard.

### D9: Motion Choreography
- **Constraint:** All state transitions (e.g., ticket classification) must use choreographed Framer Motion transitions.
- **Manual Verification:** Visual check of layout shifts and entry/exit animations.

## Automated Verification Wave 0
- [ ] `npm run test` executes Vitest and passes.
- [ ] Smoke tests confirm React component rendering.
- [ ] Pipeline stubs confirm basic event processing structure.
