/**
 * Nexus AI — Global Theme Configuration
 * Edit these values to change the entire application's aesthetic in one go.
 */

export const THEME = {
  // Brand Colors (Ultra-Bright for Visibility)
  primary: "#00f2ff",    // Pure Glowing Cyan
  secondary: "#6366f1",  // Electric Indigo
  accent: "#a855f7",     // Tech Purple

  // Neutral / Backgrounds
  background: "#020617", // Slate-950
  surface: "#0f172a",    // Slate-900

  // Status Colors
  success: "#00ffc2",    // Carbon Mint
  warning: "#fbbf24",    // Amber
  danger: "#ff4757",     // Vibrant Coral-Red

  // Glassmorphism (High Contrast)
  glass: {
    bg: "rgba(15, 23, 42, 0.7)", // Higher opacity to see the texture
    border: "rgba(255, 255, 255, 0.15)",
    glow: "rgba(0, 242, 255, 0.2)", // Stronger primary glow
  },

  // Typography
  text: {
    base: "#f1f5f9",     // Slate-100 (Slightly softer than pure Slate-50)
    muted: "#94a3b8",    // Slate-400
    dim: "#475569",      // Slate-600
  },

  aurora: ["#0ea5e9", "#2dd4bf", "#6366f1", "#a855f7", "#0ea5e9"]
};
