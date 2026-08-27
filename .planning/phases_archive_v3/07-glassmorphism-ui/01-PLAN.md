---
phase: 7
plan: 1
title: "Glassmorphism CSS System & Aurora Environment"
wave: 1
depends_on: []
files_modified:
  - app.py
  - .streamlit/config.toml
requirements: [GLASS-01, GLASS-02, GLASS-03, GLASS-04, GLASS-05]
autonomous: true
estimated_tasks: 5
must_haves:
  - "Aurora animated background renders on .stApp with smooth 20s breathing cycle"
  - "All primary containers use frosted glass material (blur(20px) + rgba(255,255,255,0.03))"
  - "Tabs render as floating glass islands with active tab lifted via translateY(-5px)"
  - "Sidebar collapse button is always visible (z-index 99999, fixed position, glowing border)"
  - "Inputs use obsidian-dark backgrounds with glowing indigo border on focus"
  - "All existing CSS class names (.glass, .metric-card, .pill-*, .kv, .banner-*, .step-*, .score-ring) remain functional"
  - "No GPU lag — blur restricted to top-level containers only"
---

# Plan: Glassmorphism CSS System & Aurora Environment

## Objective

Replace the existing CSS injection block in `app.py` (lines 32–308) with a complete, production-ready Glassmorphism design system that transforms the Nexus AI dashboard into a premium, futuristic SaaS interface. This is a **CSS-only** operation — no Python logic, no backend changes, no tab structure changes.

## Architecture

```
app.py CSS Block (lines 32-308)
├── @import: Google Fonts (Inter)
├── Section 1: Aurora Dynamic Environment
│   ├── @keyframes auroraBreathing (background-position cycle)
│   └── .stApp background + animation
├── Section 2: Core Glassmorphism (Glass Cards)
│   ├── [data-testid="stForm"] — frosted glass
│   ├── [data-testid="stStatusWidget"] — frosted glass
│   └── .glass, .glass-accent classes — preserved + upgraded
├── Section 3: Floating Tab Navigation
│   ├── [data-baseweb="tab-list"] — transparent, gapped
│   ├── [data-baseweb="tab"] — individual glass islands
│   ├── [data-baseweb="tab"]:hover — glow effect
│   ├── [aria-selected="true"] — lifted + neon accent
│   └── [data-baseweb="tab-highlight"] — hidden
├── Section 4: Sidebar Recovery Protocol
│   ├── [data-testid="collapsedControl"] — fixed, z-index, glow
│   └── [data-testid="stSidebar"] — dark glass
├── Section 5: Input & Button Styling
│   ├── .stTextInput input / .stTextArea textarea — obsidian + glow
│   └── [data-testid="stFormSubmitButton"] — gradient + lift
├── Section 6: Preserved Component Classes
│   ├── .metric-card, .metric-val, .metric-label
│   ├── .kv, .kv-key, .kv-val
│   ├── .pill-* (green/amber/red/purple/blue/indigo)
│   ├── .pri-* (p1/p2/p3/p4)
│   ├── .banner-* (danger/info/success)
│   ├── .step-* (flow/done/active/pending/arrow)
│   ├── .section-title, .section-icon
│   └── .score-ring
├── Section 7: Animations
│   ├── @keyframes slideUp, fadeIn, pulseGlow, shimmer, borderPulse
│   └── .animate-in, .fade-in
└── Section 8: Scrollbar & Misc
    ├── ::-webkit-scrollbar
    ├── .stMarkdown overflow
    └── .block-container padding
```

---

## Tasks

<task id="7.1.1">
<title>Aurora Dynamic Background</title>
<read_first>
- app.py (lines 32-50 — current background styling)
- .streamlit/config.toml (dark mode enforcement)
</read_first>
<action>
Replace the current static `.stApp` background with an animated Aurora environment.

**Add the keyframe animation:**
```css
@keyframes auroraBreathing {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
```

**Replace the `.stApp` rule with:**
```css
.stApp {
    background: linear-gradient(-45deg, #0d0e17, #111222, #1a1c2c, #0d0e17);
    background-size: 400% 400%;
    animation: auroraBreathing 20s ease infinite;
    color: #e2e8f0;
}
```

**Hide Streamlit header (preserve):**
```css
[data-testid="stHeader"] { display: none !important; }
.block-container { padding-top: 2rem !important; max-width: 1300px; }
```

**Verify `.streamlit/config.toml` contains:**
```toml
[theme]
base = "dark"
```
</action>
<acceptance_criteria>
- app.py CSS contains `@keyframes auroraBreathing` with `background-position` transitions
- `.stApp` rule contains `background: linear-gradient(-45deg, #0d0e17, #111222, #1a1c2c, #0d0e17)`
- `.stApp` rule contains `background-size: 400% 400%`
- `.stApp` rule contains `animation: auroraBreathing 20s ease infinite`
- `[data-testid="stHeader"]` is hidden with `display: none`
- `.streamlit/config.toml` contains `base = "dark"`
</acceptance_criteria>
</task>

<task id="7.1.2">
<title>Core Glassmorphism Material System</title>
<read_first>
- app.py (lines 91-111 — current .glass and .glass-accent rules)
- app.py (lines 196-213 — current stForm and stStatusWidget rules)
</read_first>
<action>
Replace the container styling with the Glassmorphism frosted-glass material spec.

**Update `[data-testid="stForm"]` to:**
```css
[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.03) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    padding: 24px !important;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1) !important;
    transition: transform 0.3s ease, border-color 0.3s ease !important;
}
```

**Update `.glass` class to:**
```css
.glass {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1);
    transition: all 0.25s ease;
}
.glass:hover {
    border-color: rgba(129, 140, 248, 0.15);
    box-shadow: 0 12px 36px -10px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.15);
}
```

**Update `.glass-accent` to:**
```css
.glass-accent {
    background: rgba(99, 102, 241, 0.04);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(99, 102, 241, 0.15);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 10px 30px -10px rgba(99,102,241,0.1), inset 0 1px 0 rgba(255,255,255,0.08);
}
```

**KEY:** Background uses `rgba(255, 255, 255, 0.03)` (faint white opacity), NOT `rgba(15, 23, 42, 0.65)` (the old dark opacity). This change is what makes the aurora gradient visible through the glass.
</action>
<acceptance_criteria>
- `[data-testid="stForm"]` contains `background: rgba(255, 255, 255, 0.03)`
- `[data-testid="stForm"]` contains `backdrop-filter: blur(20px)`
- `[data-testid="stForm"]` contains `box-shadow:` with `inset 0 1px 0 rgba(255,255,255,0.1)`
- `.glass` class contains `rgba(255, 255, 255, 0.03)` (NOT `rgba(15, 23, 42, 0.65)`)
- `.glass` class contains `backdrop-filter: blur(20px)`
- `.glass-accent` contains `rgba(99, 102, 241, 0.04)`
- No occurrence of `rgba(15, 23, 42, 0.65)` remains in the main container rules (stForm, .glass)
</acceptance_criteria>
</task>

<task id="7.1.3">
<title>Floating Tab Navigation System</title>
<read_first>
- app.py (lines 247-265 — current tab styling)
</read_first>
<action>
Replace the flat tab styling with the floating glass island navigation system.

**Replace `[data-baseweb="tab-list"]` with:**
```css
[data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 12px !important;
    border-bottom: none !important;
    padding-bottom: 20px !important;
    padding-top: 10px !important;
}
```

**Replace `[data-baseweb="tab"]` with:**
```css
[data-baseweb="tab"] {
    background: rgba(255, 255, 255, 0.02) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    margin: 0 !important;
    color: #94a3b8 !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
```

**Add hover glow for inactive tabs:**
```css
[data-baseweb="tab"]:hover {
    background: rgba(255, 255, 255, 0.06) !important;
    color: #e2e8f0 !important;
    box-shadow: 0 0 15px rgba(129, 140, 248, 0.15) !important;
}
```

**Replace active tab styling with lifted neon accent:**
```css
[data-baseweb="tab"][aria-selected="true"] {
    background: rgba(99, 102, 241, 0.1) !important;
    color: #ffffff !important;
    border: 1px solid rgba(129, 140, 248, 0.5) !important;
    transform: translateY(-5px) !important;
    box-shadow: 0 12px 24px -8px rgba(99, 102, 241, 0.3), inset 0 1px 2px rgba(255,255,255,0.2) !important;
}
```

**Hide the default Streamlit tab highlight bar:**
```css
[data-baseweb="tab-highlight"] { display: none !important; }
```
</action>
<acceptance_criteria>
- `[data-baseweb="tab-list"]` contains `background: transparent`
- `[data-baseweb="tab-list"]` contains `gap: 12px`
- `[data-baseweb="tab-list"]` contains `border-bottom: none`
- `[data-baseweb="tab"]` contains `rgba(255, 255, 255, 0.02)` background
- `[data-baseweb="tab"]` contains `backdrop-filter: blur(10px)`
- `[data-baseweb="tab"]` contains `border-radius: 12px`
- `[data-baseweb="tab"]:hover` contains `box-shadow:.*rgba(129, 140, 248`
- `[aria-selected="true"]` contains `transform: translateY(-5px)`
- `[aria-selected="true"]` contains `rgba(129, 140, 248, 0.5)` border
- `[data-baseweb="tab-highlight"]` contains `display: none`
- No `border-bottom: 2px solid` remains on tab active state (old style removed)
</acceptance_criteria>
</task>

<task id="7.1.4">
<title>Sidebar Recovery Protocol</title>
<read_first>
- app.py (lines 267-276 — current sidebar styling)
</read_first>
<action>
Add the sidebar recovery CSS to ensure the collapse/expand button is never trapped.

**Add `[data-testid="collapsedControl"]` rule:**
```css
[data-testid="collapsedControl"] {
    z-index: 99999 !important;
    position: fixed !important;
    top: 20px !important;
    left: 20px !important;
    background: rgba(15, 23, 42, 0.8) !important;
    backdrop-filter: blur(8px) !important;
    -webkit-backdrop-filter: blur(8px) !important;
    border: 1px solid rgba(168, 85, 247, 0.4) !important;
    border-radius: 50% !important;
    box-shadow: 0 0 15px rgba(168, 85, 247, 0.3) !important;
    transition: all 0.3s ease !important;
}
[data-testid="collapsedControl"]:hover {
    box-shadow: 0 0 25px rgba(168, 85, 247, 0.6) !important;
    transform: scale(1.1) !important;
}
```

**Update sidebar styling to match glass theme:**
```css
section[data-testid="stSidebar"] {
    background: rgba(10, 14, 26, 0.8) !important;
    backdrop-filter: blur(25px) !important;
    -webkit-backdrop-filter: blur(25px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
}
```
</action>
<acceptance_criteria>
- `[data-testid="collapsedControl"]` contains `z-index: 99999`
- `[data-testid="collapsedControl"]` contains `position: fixed`
- `[data-testid="collapsedControl"]` contains `border-radius: 50%`
- `[data-testid="collapsedControl"]` contains `rgba(168, 85, 247, 0.4)` border
- `[data-testid="collapsedControl"]:hover` contains `transform: scale(1.1)`
- `[data-testid="stSidebar"]` contains `backdrop-filter: blur(25px)`
- `[data-testid="stSidebar"]` contains `rgba(10, 14, 26, 0.8)` background
</acceptance_criteria>
</task>

<task id="7.1.5">
<title>Input & Button Styling + Preserved Components</title>
<read_first>
- app.py (lines 215-246 — current input and button styling)
- app.py (lines 127-299 — all component class definitions)
</read_first>
<action>
Update text inputs to obsidian-dark styling with glowing focus borders. Ensure all existing component classes remain in the CSS output.

**Update input styling:**
```css
.stTextInput input, .stTextArea textarea {
    background: #090a10 !important;
    color: #f8fafc !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2) !important;
    background: #0c0d14 !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {
    color: #475569 !important;
}
```

**Update form submit button with scale + lift:**
```css
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
    color: white !important;
    border: none !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    height: 3.5rem !important;
    letter-spacing: 0.5px !important;
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease !important;
}
[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 10px 25px -5px rgba(168, 85, 247, 0.5) !important;
}
```

**CRITICAL:** Preserve ALL these class definitions in the final output (they are used in HTML throughout `app.py`):
- `.metric-card`, `.metric-val`, `.metric-label` — update `.metric-card` background to `rgba(255,255,255,0.02)` with `blur(12px)` (lighter than top-level containers)
- `.kv`, `.kv-key`, `.kv-val` — preserve exactly
- `.pill-*` (green/amber/red/purple/blue/indigo) — preserve exactly
- `.pri-*` (p1/p2/p3/p4) — preserve exactly
- `.banner-*` (danger/info/success) — preserve exactly
- `.step-*` (flow/done/active/pending/arrow) — preserve exactly
- `.section-title`, `.section-icon` — preserve exactly
- `.score-ring` — preserve exactly
- `.animate-in`, `.fade-in` — preserve exactly
- All `@keyframes` (slideUp, fadeIn, pulseGlow, shimmer, borderPulse) — preserve exactly
- Scrollbar styling — preserve exactly
- `.stMarkdown` overflow fix — preserve exactly
</action>
<acceptance_criteria>
- `.stTextInput input` contains `background: #090a10`
- `.stTextInput input:focus` contains `border-color: #818cf8`
- `.stTextInput input:focus` contains `box-shadow:.*rgba(129, 140, 248, 0.2)`
- `[data-testid="stFormSubmitButton"] > button:hover` contains `scale(1.02)`
- CSS contains `.metric-card` class definition
- CSS contains `.kv` class definition
- CSS contains `.pill-green` class definition
- CSS contains `.pill-amber` class definition
- CSS contains `.banner-danger` class definition
- CSS contains `.step-done` class definition
- CSS contains `.score-ring` class definition
- CSS contains `@keyframes slideUp`
- CSS contains `@keyframes pulseGlow`
- CSS contains `.animate-in` class definition
- CSS contains `::-webkit-scrollbar` rules
- No occurrences of old input background `rgba(15, 23, 42, 0.8)` in text input rules
</acceptance_criteria>
</task>

---

## Verification

### Automated Checks
```bash
# Verify the glassmorphism key properties are present
grep -c 'auroraBreathing' app.py  # expect: 2+ (keyframe + animation reference)
grep -c 'backdrop-filter: blur(20px)' app.py  # expect: 3+ (stForm, .glass, .glass-accent)
grep -c 'translateY(-5px)' app.py  # expect: 1 (active tab)
grep -c 'collapsedControl' app.py  # expect: 2+ (base + hover rules)
grep -c 'rgba(255, 255, 255, 0.03)' app.py  # expect: 2+ (glass cards)
grep -c '#090a10' app.py  # expect: 1 (obsidian input background)

# Verify NO old dark-glass backgrounds on primary containers
grep 'rgba(15, 23, 42, 0.65).*stForm\|stForm.*rgba(15, 23, 42, 0.65)' app.py  # expect: 0

# Verify all required CSS classes are present
for cls in metric-card kv pill-green pill-amber banner-danger step-done score-ring animate-in; do
  grep -q "\.$cls" app.py && echo "✓ .$cls" || echo "✗ .$cls MISSING"
done

# Verify app runs without syntax errors
source venv/bin/activate && python -c "import ast; ast.parse(open('app.py').read()); print('✓ Syntax OK')"
```

### Visual Verification (Manual)
1. Run `streamlit run app.py` and confirm:
   - Background slowly animates between navy and purple (20s cycle)
   - Ticket form and status box appear as frosted glass with visible aurora gradient bleeding through
   - Tabs look like individual floating pills, not flat underlined text
   - Clicking a tab causes it to visually "lift" above the others
   - Collapsing the sidebar reveals a glowing purple toggle button at top-left
   - Input fields have near-black backgrounds that glow indigo on focus
2. Submit a test ticket and confirm all 5 tabs render data correctly (no visual regression)
3. During pipeline execution, confirm no visible frame drops or stuttering
