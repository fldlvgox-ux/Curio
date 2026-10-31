# Curio Theme Plugin — Cross-Agent Remote Prompt & Handoff Specification

> **Copy & Paste this entire file into any AI model (Claude, ChatGPT, Gemini, DeepSeek, local LLM) to generate a fully immersive Curio Theme Plugin.**

---

## Remote Agent Prompt Instructions

You are tasked with generating a production-grade visual theme plugin for **Curio** (an offline-first visual catalog, creative vault, and game design document tool).

In Curio, themes **must never be shallow color palette swaps**. Every theme must have its own **unique physical design, silhouette, tactile materials, and personality**—acting as an immersive artifact designed to transport the user into another machine, era, or reality.

You must respond with **TWO code blocks**:
1. `manifest.json` — plugin metadata and all 46 mandatory CSS tokens.
2. `theme.css` — component styles, tactile states, and 7 mandatory procedural SVG artwork zones, all scoped strictly under `[data-theme="curio-theme-<id>"]` and `[data-theme="<id>"]`.

---

## 1. The 6-Channel Immersion Mandate

Every Curio theme must engage all six design channels:
1. **Tokens**: Full 46-token contract compliance with intentional palette discipline.
2. **Parts**: Deep component-level styling across windows, cards, sidebars, buttons, inputs, and inspectors.
3. **Shapes**: Intentional silhouettes (0px brutalist blocks, 45° chamfers, 9-slice pixel corners, or curved CRT housings).
4. **Materials**: Tactile finishes (leather grain, cream laminate, brushed steel, warm timber, or parchment).
5. **Ornaments & Atmospheric Overlays**:
   - `body::after` or root pseudo-elements with `pointer-events: none` for atmospheric environmental textures (procedural stone bricks, CRT scanlines, tungsten vignettes, CAD blueprint grids, tactile dither).
   - Period signature details (tilted rubber stamps, dashed sewn stitching, sci-fi corner brackets, inventory slot recesses).
6. **Icons & Custom Logos**:
   - Replace default folder icons with custom inline vector SVG emblems (`data:image/svg+xml`).

---

## 2. Mandatory 7-Zone Custom Artwork Requirement

Themes must embed **unique, lore-specific decorative artwork** into each of the 7 major UI zones:
1. **`.brand-header` / `.brand-title::before`** — Custom logo emblem reflecting the theme's world (e.g. sci-fi delta, 16-bit shield, typewriter seal).
2. **`.sidebar::after`** — Decorative crest, medallion, or lore motif placed at the bottom or top of the sidebar.
3. **`.top-bar::before` or `.top-bar::after`** — Engraved brass rail, HUD telemetry stripe, or banner art along the toolbar edge.
4. **`.filter-panel::before`** — Decorative ruled divider, architectural detail, or thematic separator art.
5. **`.item-card::before` / `.item-card::after`** — Frame corners, border inlays, rivets, or themed border art. Never leave a card as a plain flat rectangle.
6. **`.modal-header::before` or `.modal-title`** — Scroll endcaps, hazard striping, carved header border, or dedicated plaque.
7. **`body::after`** — Global atmospheric texture with `pointer-events: none; z-index: 0;`.

All artwork must be procedural inline SVG data URIs (`data:image/svg+xml,...`) or pure CSS gradients.

---

## 3. High Contrast & Accessibility Discipline

- **Dark Surfaces**: When styling dark surfaces (`.sidebar`, `.filter-panel`, `#catalog-selector`, `.select-custom`, `.tag-search-input`), explicitly set text and labels to high-contrast colors (cream `#EDE0C4`, gold `#FCE28A`, amber `#FFA63D`, or white `#FFFFFF`).
- **Hazard / Dense Patterns**: Never place raw dark text directly over high-contrast repeating patterns (e.g. hazard stripes). Always place an opaque plaque (`background: #0A0A0A; border: 1px solid #FFD700; padding: 4px 8px;`) behind `.brand-title` and `.modal-title`.
- Never allow elements to inherit unreadable low-contrast text.

---

## 4. Strict 46-Token Contract (`manifest.json`)

You MUST define every single token below in the `"tokens"` object:

```json
{
  "id": "curio-theme-<your-id>",
  "name": "<Theme Display Name>",
  "version": "1.0.0",
  "type": "theme",
  "author": "<Your Name>",
  "description": "<One sentence summary>",
  "family": "<classic | retro-sci-fi | fantasy | paper | aero | modern>",
  "entry": "theme.css",
  "tokens": {
    "--bg": "#090d16",
    "--surface": "#111726",
    "--surface-2": "#182238",
    "--text": "#f1f5f9",
    "--text-dim": "#94a3b8",
    "--accent": "#06b6d4",
    "--accent-text": "#ffffff",
    "--border": "#1e293b",
    "--select-bg": "#3b82f6",
    "--select-fg": "#ffffff",
    "--danger": "#f43f5e",
    "--ok": "#10b981",
    "--warn": "#f59e0b",
    "--font-ui": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "--font-display": "inherit",
    "--font-mono": "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
    "--font-size-base": "14px",
    "--font-smoothing": "antialiased",
    "--space-1": "4px",
    "--space-2": "8px",
    "--space-3": "12px",
    "--space-4": "16px",
    "--space-5": "24px",
    "--row-height": "36px",
    "--control-height": "32px",
    "--pixel-scale": "1",
    "--radius-window": "8px",
    "--radius-control": "4px",
    "--radius-chip": "999px",
    "--avatar-shape": "50%",
    "--cut-tl": "0px",
    "--cut-tr": "0px",
    "--cut-br": "0px",
    "--cut-bl": "0px",
    "--bevel-light": "transparent",
    "--bevel-dark": "transparent",
    "--bevel-width": "0px",
    "--shadow-raised": "0 2px 8px rgba(0,0,0,0.3)",
    "--shadow-pressed": "inset 0 2px 4px rgba(0,0,0,0.3)",
    "--shadow-hard": "none",
    "--gradient-title": "none",
    "--gradient-button": "none",
    "--grain": "none",
    "--dither-pattern": "none",
    "--focus-ring": "0 0 0 2px #06b6d4",
    "--default-button-ring": "none"
  }
}
```

---

## 5. Security & Zero-Build Constraint

1. **NO JavaScript**: Theme plugins are strictly CSS + JSON.
2. **NO `@import`**: External CSS stylesheets are prohibited.
3. **NO External URLs**: No `http://` or `https://` font or image URLs. Only procedural `data:image/svg+xml,...` URIs are allowed.
4. **Scoping**: All CSS rules must begin with both `[data-theme="curio-theme-<id>"]` and `[data-theme="<id>"]`.

---

## 6. How to Package and Install

### Method A: Scaffold Locally
```powershell
powershell ./tools/scaffold-theme.ps1 -ThemeId "curio-theme-<id>" -ThemeName "<Display Name>" -Family "<family>"
```

### Method B: Pack into ZIP for Instant Import
```powershell
powershell ./tools/pack-theme.ps1 -ThemeId "curio-theme-<id>"
```
Then in Curio:
1. Open **Settings -> Themes**.
2. Click **"Import Theme (.zip)"**.
3. Select the generated `.zip` file — Curio mounts and activates it immediately without page refresh!
