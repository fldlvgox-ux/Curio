# Curio Theme Plugin — Cross-Agent Handoff Specification

> **Instructions for the AI Assistant / Remote Model:**
> You are tasked with generating a visual theme plugin for the **Curio** web and desktop application.
> Read the contract rules below and output **two code blocks**:
> 1. `manifest.json` (metadata and CSS variable tokens)
> 2. `theme.css` (custom component rules scoped strictly under `[data-theme="curio-theme-<id>"]`)

---

## 1. Strict Contract Requirements (Version 1.0.0)

### Mandatory Tokens in `manifest.json`
You MUST define every token below under the `"tokens"` object in `manifest.json`. Unused tokens must be set to a harmless default (`"none"`, `"0"`, or `"transparent"`), never omitted.

#### Colors (13 required)
* `--bg`: Canvas / page background
* `--surface`: Card, panel, and modal background
* `--surface-2`: Raised/nested surface level
* `--text`: Primary high-contrast text color
* `--text-dim`: Secondary or muted text color
* `--accent`: Primary interactive color (buttons, highlights)
* `--accent-text`: Text color when rendered on top of `--accent`
* `--border`: Standard border stroke
* `--select-bg`: Selected item or active tab background
* `--select-fg`: Selected item text color
* `--danger`: Destructive/danger state color
* `--ok`: Success/positive state color
* `--warn`: Warning/caution state color

#### Typography (5 required)
* `--font-ui`: Primary UI font stack (e.g. `'Segoe UI', sans-serif`, `'MS Sans Serif'`)
* `--font-display`: Heading/display font stack (or `"inherit"`)
* `--font-mono`: Monospace font stack (for data/readouts)
* `--font-size-base`: Base font size (e.g. `"14px"`, `"11px"`)
* `--font-smoothing`: `"antialiased"` or `"auto"`

#### Spacing & Density (8 required)
* `--space-1` to `--space-5`: Relative spacing increments (default `"4px"`, `"8px"`, `"12px"`, `"16px"`, `"24px"`)
* `--row-height`: Table/list row height (e.g. `"36px"`)
* `--control-height`: Standard input/button height (e.g. `"32px"`)
* `--pixel-scale`: Integer scale factor (typically `"1"`, or `"2"` for retro pixel art)

#### Shape (8 required)
* `--radius-window`: Window and modal corner radius (e.g. `"12px"`, `"0px"`)
* `--radius-control`: Button and input corner radius (e.g. `"6px"`, `"0px"`)
* `--radius-chip`: Tag and pill radius (e.g. `"999px"`, `"0px"`)
* `--avatar-shape`: Avatar border radius (e.g. `"50%"`, `"0px"`)
* `--cut-tl`, `--cut-tr`, `--cut-br`, `--cut-bl`: Corner chamfer cuts for HUD/sci-fi shapes (default `"0px"`)

#### Material & Depth (10 required)
* `--bevel-light`: 3D bevel top/left highlight color
* `--bevel-dark`: 3D bevel bottom/right shadow color
* `--bevel-width`: Bevel thickness (e.g. `"2px"`, `"0px"`)
* `--shadow-raised`: Box-shadow for resting cards/modals
* `--shadow-pressed`: Inset box-shadow for pressed buttons
* `--shadow-hard`: Hard offset shadow (e.g. `"4px 4px 0px #000"`, or `"none"`)
* `--gradient-title`: Gradient for titlebars (or `"none"`)
* `--gradient-button`: Gradient for buttons (or `"none"`)
* `--grain`: Grain filter id or `"none"`
* `--dither-pattern`: Dither texture or `"none"`

#### Focus (2 required)
* `--focus-ring`: Outline/ring on keyboard focus (e.g. `"0 0 0 2px var(--accent)"`)
* `--default-button-ring`: Special highlight ring for primary actions or `"none"`

---

## 2. Security Rules (Mandatory)

1. **NO JavaScript**: Theme plugins are strictly declarative (CSS + JSON).
2. **NO `@import`**: You cannot import external CSS stylesheets.
3. **NO External URLs**: `url("https://...")` is forbidden. Only inline `data:` URIs or SVG masks are allowed.
4. **NO `<script>` in SVG**: Icons or ornaments cannot contain scripts or event listeners (`onclick`, etc.).
5. **Strict Scoping**: Every selector in `theme.css` must begin with `[data-theme="curio-theme-<id>"]`.

---

## 3. Curio UI Component Class Map

Use these standard classes in your `theme.css`:
* **App Chrome**: `.toolbar`, `.top-bar`, `.sidebar`, `.header`, `.footer`
* **Navigation**: `.drawer`, `.drawer-item`, `.tab-btn`, `.active`
* **Containers**: `.modal-content`, `.dialog-box`, `.panel`, `.catalog-card`, `.item-card`
* **Controls**: `.btn`, `.btn-primary`, `.btn-danger`, `.btn-icon`
* **Inputs**: `input[type="text"]`, `input[type="search"]`, `textarea`, `select`, `.checkbox`
* **Display**: `.badge`, `.status-pill`, `.progress-bar`, `.tag`, `.results-count`

---

## 4. Output Format

Respond strictly with the two code blocks below:

### Block 1: `manifest.json`
```json
{
  "id": "curio-theme-<your-theme-name>",
  "name": "<Display Name>",
  "version": "1.0.0",
  "type": "theme",
  "contract": "1.0.0",
  "author": "<Author or AI Model Name>",
  "description": "<One sentence aesthetic summary>",
  "family": "<retro-os | cyberpunk | minimal | organic | modern>",
  "preview": "preview.png",
  "files": {
    "css": "theme.css"
  },
  "tokens": {
    // ... all 46 required tokens from Section 1 ...
  }
}
```

### Block 2: `theme.css`
```css
/* Scoped overrides */
[data-theme="curio-theme-<your-theme-name>"] {
  /* ... custom styling rules ... */
}
```
