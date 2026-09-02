# Phase 8: Elite UI/UX & Micro-Interactions

## Goal
Elevate the Nexus AI platform to "Elite" status through high-fidelity CSS micro-interactions, advanced data visualizations with Plotly, dynamic navbar states, and comprehensive deep glassmorphism features (floating sidebar, FAB, and frosted overlays).

## Tasks

### 8.1 Motion System (CSS)
- Update the Streamlit CSS in `app.py` to add `delay-x` staggered animation classes.
- Add hover-swell `transform: scale(1.02)` and neon glow to `.glass` and `.glass-accent` cards.
- Add a smooth fade-in for tab panel content.

### 8.2 Advanced Data Visualizations
- In `app.py`, update the Plotly bar chart in the Classification tab to be an interactive Sankey diagram showing the classification flow.
- Add a unified custom dark theme for Plotly using `PLOTLY_THEME` palette.
- Render RAG evidence scores as a colored heatmap.

### 8.3 Dynamic Navbar & UX Enhancements
- Modify the Elite Floating Pill Navbar CSS (in `app.py`) to allow for a dynamic "Status: Online" vs "Processing..." text/badge based on `st.session_state` during pipeline runs.
- Add a Command Palette (search bar) at the top of the layout.
- Add keyboard shortcuts help tooltip.

### 8.4 Deep Glassmorphism Components
- Implement a detached floating glass Sidebar that does not touch the edges of the screen.
- Implement a Floating Action Button (FAB) for "Quick Submit/Feedback" in the bottom-right corner.
- Replace standard expanders with Frosted Overlays for the Resolution Judge safety gate.

## Verification
- All UIs render correctly without breaking layout.
- Animations trigger smoothly (Slide up, fade in).
- Plotly charts render in dark theme.
- Dynamic Status shows accurately.
