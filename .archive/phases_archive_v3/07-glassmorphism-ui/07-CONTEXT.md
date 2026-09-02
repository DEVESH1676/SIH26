# Phase 7: Premium Glassmorphism UI Transformation - Context

**Gathered:** 2026-04-14
**Status:** Ready for planning

<domain>
## Phase Boundary

Transform the existing Nexus AI Streamlit UI (Phase 6 output) from a functional dark-themed dashboard into a premium, futuristic SaaS-grade experience using Glassmorphism, dynamic aurora backgrounds, floating tab navigation, and a sidebar recovery protocol. The scope is limited to CSS injection via `st.markdown(..., unsafe_allow_html=True)` — no backend or pipeline logic changes.

### What changes:
- The global `<style>` block in `app.py` (lines 32–308) is replaced with the new Glassmorphism CSS system
- The `.streamlit/config.toml` dark theme enforcement remains
- All existing HTML class names (`.glass`, `.metric-card`, `.pill-*`, `.kv`, `.banner-*`, `.step-*`, `.score-ring`) must be preserved or migrated

### What does NOT change:
- No modifications to `core/classifier.py`, `core/rag.py`, `core/agent.py`, `core/judge.py`, or `core/feedback.py`
- No modifications to the Python logic in `app.py` (only the CSS block)
- Tab structure, column layout, and pipeline execution flow remain identical
</domain>

<decisions>
## Implementation Decisions

### D-01: Core Visual Identity — Glassmorphism Material Spec
Every primary container (Ticket Form via `[data-testid="stForm"]`, Status Box via `[data-testid="stStatusWidget"]`, and the tab navigation via `[data-baseweb="tab-list"]`) must use:
- Background: `rgba(255, 255, 255, 0.03)` (faint white opacity, NOT dark rgba — lets aurora bleed through)
- Blur: `backdrop-filter: blur(20px)` + `-webkit-backdrop-filter: blur(20px)`
- Border: `1px solid rgba(255, 255, 255, 0.08)`
- Depth: Multi-layered box shadow: `0 10px 30px -10px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1)`
- Border-radius: `16px`

### D-02: 5-Category Floating Tab Navigation
Target `[data-baseweb="tab"]` elements individually:
- **Inactive:** `rgba(255, 255, 255, 0.02)` background, `blur(10px)`, `1px solid rgba(255,255,255,0.05)` border, color `#94a3b8`
- **Hover (inactive):** `rgba(255, 255, 255, 0.06)` background, `box-shadow: 0 0 15px rgba(129,140,248,0.15)` glow
- **Active (`[aria-selected="true"]`):** `rgba(99, 102, 241, 0.1)` background, `1px solid rgba(129,140,248,0.5)` border, `transform: translateY(-5px)`, neon shadow `0 12px 24px -8px rgba(99,102,241,0.3)`
- **Tab list container (`[data-baseweb="tab-list"]`):** Remove bottom border, add `gap: 12px`, transparent background
- **Hide default highlight:** `[data-baseweb="tab-highlight"] { display: none }`

### D-03: Aurora Dynamic Environment
- CSS `@keyframes auroraBreathing` cycling `background-position` from `0% 50%` → `100% 50%` → `0% 50%`
- Applied to `.stApp` with `background: linear-gradient(-45deg, #0d0e17, #111222, #1a1c2c, #0d0e17)`
- `background-size: 400% 400%`
- `animation: auroraBreathing 20s ease infinite`
- Must be subtle — no distracting rapid motion

### D-04: Sidebar Recovery Protocol
- Target `[data-testid="collapsedControl"]` with:
  - `z-index: 99999`, `position: fixed`, `top: 20px`, `left: 20px`
  - `background: rgba(15, 23, 42, 0.8)`, `backdrop-filter: blur(8px)`
  - `border: 1px solid rgba(168, 85, 247, 0.4)`, `border-radius: 50%`
  - `box-shadow: 0 0 15px rgba(168, 85, 247, 0.3)`
  - Hover: `box-shadow: 0 0 25px rgba(168,85,247,0.6)`, `transform: scale(1.1)`
- Target sidebar itself: dark blur `rgba(10, 14, 26, 0.8)`, `blur(25px)`, subtle right border

### D-05: Input Styling — Deep Obsidian with Glow
- `.stTextInput input, .stTextArea textarea`: `background: #090a10`, border `1px solid rgba(255,255,255,0.1)`
- Focus: `border-color: #818cf8`, `box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2)`
- Preserve existing placeholder color at `#475569`

### D-06: Performance Constraint
- Heavy blur (`blur(20px)`) ONLY on top-level containers: `[data-testid="stForm"]`, `[data-baseweb="tab"]`, sidebar
- Interior components (`.metric-card`, `.pill-*`, `.banner-*`, `.kv`, `.step-*`) use lighter blur (`blur(12px)`) or none
- No nested blur stacking (child glass inside parent glass)

### Agent's Discretion
- Exact animation timing curves and easing functions
- Transition durations for hover effects
- Whether to add a subtle noise/grain texture overlay
- Scrollbar re-styling approach
- Any additional micro-animations for the form submit button

</decisions>

<code_context>
## Existing Code Insights

### CSS Block Location
The current CSS block in `app.py` spans lines 32–308, injected via `st.markdown("""<style>...</style>""", unsafe_allow_html=True)`.

### Existing CSS Classes Used Elsewhere in app.py
These class names are referenced in HTML throughout app.py and MUST remain functional:
- `.glass`, `.glass-accent` — container wrappers
- `.metric-card`, `.metric-val`, `.metric-label` — score displays
- `.kv`, `.kv-key`, `.kv-val` — key-value rows
- `.pill`, `.pill-green/amber/red/purple/blue/indigo` — status badges
- `.pri`, `.pri-p1/p2/p3/p4` — priority badges
- `.banner-danger/info/success` — alert banners
- `.step-flow`, `.step`, `.step-done/active/pending`, `.step-arrow` — pipeline flow
- `.section-title`, `.section-icon` — section headings
- `.score-ring` — judge score display
- `.animate-in`, `.fade-in` — entrance animations

### Streamlit DOM Selectors
Already in use and must remain targeted:
- `[data-testid="stHeader"]` — hidden
- `[data-testid="stForm"]` — glass card
- `[data-testid="stStatusWidget"]` — status box
- `[data-testid="stSidebar"]` — sidebar
- `[data-baseweb="tab-list"]`, `[data-baseweb="tab"]` — tabs
- `.stTextInput input`, `.stTextArea textarea` — inputs
- `[data-testid="stFormSubmitButton"]` — submit button

### Font Stack
`@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap')` — must be preserved.
</code_context>

<specifics>
## Specific Ideas

### Linear/Vercel Design DNA
- Linear uses monochrome dark with single-accent-color highlights and ultra-clean typography
- Vercel uses glassmorphism with gradient borders and floating cards
- Both use subtle motion that feels "alive" without being distracting
- Both limit heavy effects to structural containers, keeping content areas clean

### Color Palette
- Background: `#0d0e17` (deep space navy) ↔ `#1a1c2c` (cosmic purple)
- Accent primary: `#6366f1` (Indigo 500) → `#818cf8` (Indigo 400) for glows
- Accent secondary: `#a855f7` (Purple 500) → `#c084fc` (Purple 400) for gradients
- Text: `#f8fafc` (primary), `#e2e8f0` (secondary), `#94a3b8` (muted), `#64748b` (dim)
- Success: `#4ade80`, Warning: `#fbbf24`, Error: `#f87171`

### Glassmorphism Reference Values
| Property | Glass Card | Glass Tab (inactive) | Glass Tab (active) |
|----------|-----------|---------------------|-------------------|
| bg opacity | 0.03 white | 0.02 white | 0.10 indigo |
| blur | 20px | 10px | 10px |
| border | 0.08 white | 0.05 white | 0.50 indigo |
| shadow | multi-layer | none | neon glow |
</specifics>

<deferred>
## Deferred Ideas

- Particle effects or floating orbs in the background (too heavy for Streamlit)
- Custom SVG-based animated logo in the header
- Three.js 3D background integration (performance risk)
- Per-tab unique accent colors (keep single indigo/purple palette for now)
</deferred>

---

*Phase: 07-glassmorphism-ui*
*Context gathered: 2026-04-14 via user design specification*
