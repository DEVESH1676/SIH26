# Phase 2: Frontend Scaffolding - Research

**Researched:** 2026-04-18
**Domain:** React, Vite, Tailwind CSS, Aceternity/Shadcn UI, SSE, TypeScript
**Confidence:** HIGH

## Summary

This research establishes the technical foundation for the Nexus AI frontend migration from Streamlit to a decoupled React/Vite architecture. The primary focus is on replicating the real-time "alive" feel of the Streamlit pipeline using Server-Sent Events (SSE) while significantly upgrading the visual fidelity with a glassmorphism-focused UI using Shadcn and Aceternity.

**Primary recommendation:** Use a `usePipeline` hook with a `useReducer` pattern to manage the 5-stage pipeline state, consuming the FastAPI SSE stream. Prioritize GPU-accelerated animations for the "Aurora" background to maintain performance.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01: App Structure:** Single-page progressive disclosure Intelligence Feed.
- **D-02: Landing Layout:** Balanced hybrid with split view (Submission hero vs. System Health Pulse).
- **D-03: Submission Experience:** Same-screen split workspace with live logs.
- **D-04: Realtime Behavior:** SSE-first interaction model.
- **D-05: Navbar Behavior:** Status-aware pill navigation.
- **D-06: Mock Scope:** Full experience scaffolding including history and analytics.
- **D-07: State Management:** `useReducer` for pipeline orchestration.
- **D-08: Component Stack:** Shadcn UI (functional) + Aceternity UI (visual).
- **D-09: Motion Language:** Framer Motion for stage reveals and choreography.
- **D-10: API and Type Safety:** Generated TypeScript types from OpenAPI.

### the agent's Discretion
- Exact component naming and folder layout inside the React app.
- Exact Framer Motion easing curves and timing.
- Exact visual treatment of the System Health Pulse cards.
- Exact badge colors as long as they stay within the established premium glass / indigo-blue aesthetic.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| UI-01 | Modern React Shell | Vite + Tailwind + Shadcn/Aceternity stack confirmed. |
| UI-02 | Pipeline Feed | `useReducer` SSE pattern and Framer Motion reveal patterns researched. |
| UI-03 | System Health Pulse | Shadcn Card + Recharts pattern (standard). |
</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Pipeline Orchestration | API / Backend | Client (UI) | API runs logic; Client reflects state via SSE. |
| State Management | Client (React) | — | Pipeline stages, logs, and UI feedback are client-owned. |
| Data Visualization | Client (React) | — | Rendering charts and system health metrics. |
| Animation/Transitions | Client (Framer) | — | Visual feedback and "alive" feel. |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| React | 18.x / 19.x | UI Framework | Industry standard for complex stateful UIs. |
| Vite | 6.x | Build Tool | Extremely fast HMR and optimized builds. |
| Tailwind CSS | 3.x / 4.x | Styling | Utility-first, highly performant, required by Shadcn. |
| Framer Motion | 11.x | Animation | Industry standard for React animations; core of Aceternity. |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|--------------|
| Shadcn UI | 4.3.0 | Foundational UI | Inputs, Buttons, Cards, Dialogs. |
| Aceternity UI | Latest | Premium Visuals | Aurora background, Bento grids, Shimmer effects. |
| openapi-typescript | 7.13.0 | Type Generation | Converting FastAPI spec to TS interfaces. |
| fetch-event-source | 2.0.1 | SSE Client | Use if auth headers or POST methods are needed for SSE. |
| Lucide React | Latest | Icons | Standard icon set for Shadcn. |

**Installation:**
```bash
# Core
npm create vite@latest frontend -- --template react-ts
npm install tailwindcss postcss autoprefixer framer-motion clsx tailwind-merge
# UI
npx shadcn-ui@latest init
# Tools
npm install -D openapi-typescript
```

## Architecture Patterns

### Recommended Project Structure
```
src/
├── components/
│   ├── ui/          # Shadcn primitives + Aceternity ports
│   ├── pipeline/    # StageCard, TerminalLogs, IntelligenceFeed
│   ├── shell/       # Navbar, Footer, Sidebar
│   └── pulse/       # HealthPulse, MetricCard
├── hooks/
│   ├── use-pipeline.ts # SSE orchestration
│   └── use-theme.ts
├── lib/
│   ├── utils.ts     # cn() helper
│   └── api.ts       # Type-safe fetch wrapper
├── types/
│   └── api.ts       # Generated from openapi-typescript
└── App.tsx          # Layout orchestration
```

### Pattern 1: SSE Pipeline Reducer
**What:** Centralized state for the 5-stage pipeline.
**When to use:** Managing transitions from Classify -> Triage -> RAG -> Resolve -> Judge.
**Example:**
```typescript
// Pattern: useReducer + EventSource
type PipelineState = {
  status: 'idle' | 'running' | 'complete' | 'error';
  stages: Record<string, StageData>;
  logs: string[];
};

function pipelineReducer(state: PipelineState, action: Action): PipelineState {
  // Update stage progress, append logs, handle completion
}
```

### Pattern 2: Glassmorphism Primitive
**What:** Reusable Tailwind utility for frosted glass.
**When to use:** All card surfaces in the intelligence feed.
**Implementation:**
```typescript
// tailwind.config.js extension
// backdrop-blur-xl bg-white/5 border border-white/10 shadow-glass
```

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Complex SSE | Raw EventSource | `@microsoft/fetch-event-source` | Better error handling, custom headers, POST support. |
| Type generation | Manual interfaces | `openapi-typescript` | Single source of truth from FastAPI/Pydantic models. |
| Glass UI | Custom CSS | Shadcn + Tailwind classes | Consistent accessibility and theme support. |

## Common Pitfalls

### Pitfall 1: Aurora Background CPU Usage
**What goes wrong:** High CPU usage/fans spinning on landing.
**Why it happens:** Heavy CSS blurs animating on every frame without GPU acceleration.
**How to avoid:** Use `will-change-transform`, animate `opacity` and `transform` only, and use `useInView` to stop the animation when off-screen. [VERIFIED: Aceternity Best Practices]

### Pitfall 2: SSE Memory Leaks
**What goes wrong:** Multiple active connections on route changes.
**Why it happens:** Failing to close `EventSource` in `useEffect` cleanup.
**How to avoid:** Always return `() => es.close()` in the connection effect. [VERIFIED: React Docs]

### Pitfall 3: Type Drift
**What goes wrong:** UI breaks when Backend model changes.
**Why it happens:** Stale generated types.
**How to avoid:** Integrate `openapi-typescript` into the dev workflow (e.g., a `predev` script).

## Code Examples

### Optimized Aurora Background (Framer Motion)
```tsx
// Source: https://ui.aceternity.com/components/aurora-background
// Optimization: useInView + will-change
const containerRef = useRef(null);
const isInView = useInView(containerRef);

return (
  <div ref={containerRef} className="will-change-transform">
    {isInView && (
      <motion.div 
        animate={{ opacity: [0.5, 0.8, 0.5] }}
        transition={{ duration: 10, repeat: Infinity }}
      />
    )}
  </div>
);
```

### Type Generation Command
```bash
# In package.json
"generate-types": "npx openapi-typescript http://localhost:8000/openapi.json -o src/types/api.ts"
```

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | FastAPI provides openapi.json at standard path | Type Safety | Type generation script fails. |
| A2 | User prefers dark mode for Aurora effect | Stack | Visual mismatch with light mode. |
| A3 | No complex auth headers needed for initial SSE | Stack | `EventSource` may need replacement sooner. |

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Node.js | Vite / Build | ✓ | 20.x | — |
| npm | Package Mgmt | ✓ | 10.x | — |
| FastAPI | API / SSE | ✓ | 0.x | Mock JSON |

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Vitest + React Testing Library |
| Config file | `vitest.config.ts` |
| Quick run command | `npm test` |
| Full suite command | `npm run test:ui` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| UI-01 | Vite shell loads | Smoke | `vitest run tests/smoke.test.ts` | ❌ Wave 0 |
| UI-02 | Pipeline updates on SSE | Integration | `vitest run tests/pipeline.test.ts` | ❌ Wave 0 |

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V5 Input Validation | yes | `zod` for form validation |
| V14 Configuration | yes | `.env` for API URLs |

### Known Threat Patterns for React/Vite

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| XSS | Tampering | React auto-escapes; use `DOMPurify` if rendering raw HTML. |
| Dependency Vulnerabilities | Elevation | `npm audit` + `dependabot`. |

## Sources

### Primary (HIGH confidence)
- [Aceternity UI Docs] - Aurora background implementation and performance.
- [Shadcn UI Docs] - Component integration and Tailwind setup.
- [openapi-typescript GitHub] - CLI usage and type generation.
- [Microsoft fetch-event-source] - SSE best practices.

### Secondary (MEDIUM confidence)
- [Framer Motion Performance Guides] - Optimizing blurs and filters.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Industry standard choices.
- Architecture: HIGH - Proven SSE/Reducer pattern.
- Pitfalls: HIGH - Well-documented performance issues.

**Research date:** 2026-04-18
**Valid until:** 2026-05-18
