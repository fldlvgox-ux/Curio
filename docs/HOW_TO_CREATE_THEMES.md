# How to Create a Curio Theme Plugin Using Any AI Model

This guide walks you through generating and installing custom Curio themes using **any external AI model** (such as ChatGPT, Claude, Gemini, DeepSeek, or local LLMs).

Curio themes support **full visual transformation**: colors, fonts, shapes, **custom brand logos**, **custom icon sets**, and **atmospheric overlays** (CRT scanlines, vignettes, paper grain, grids).

---

## ⚡ Quick 30-Second Summary

1. **Copy** the prompt from [Section 2](#2-copy--paste-prompt-for-the-other-ai) into your AI.
2. **Tell it your theme idea** (e.g. *"GameBoy LCD"*, *"TVA Bureaucracy"*, *"Cyberpunk 2077 HUD"*).
3. **Save** the two code blocks it gives you:
   - `manifest.json`
   - `theme.css`
4. **Install**:
   - **Easiest**: Put both files in a `.zip` file, open Curio **Settings ➔ Import Theme (.zip)**.
   - **Alternative**: Put both files in `plugins/curio-theme-<your-id>/` and run `powershell tools/update-plugin-index.ps1`.

---

## 2. Copy & Paste Prompt for the Other AI

Copy the entire block below into your AI chat session, replacing the `[YOUR THEME IDEA GOES HERE]` section at the bottom:

```markdown
You are a senior UI/UX designer and frontend engineer creating a custom theme plugin for Curio (a visual cataloging web and desktop app).

Please generate two production-ready files:
1. `manifest.json`
2. `theme.css`

### Strict Contract Requirements:
1. Manifest must use contract version "1.0.0" and type "theme".
2. The "tokens" object in manifest.json must define all 46 tokens:
   - Colors: --bg, --surface, --surface-2, --text, --text-dim, --accent, --accent-text, --border, --select-bg, --select-fg, --danger, --ok, --warn
   - Typography: --font-ui, --font-display, --font-mono, --font-size-base, --font-smoothing
   - Spacing: --space-1, --space-2, --space-3, --space-4, --space-5, --row-height, --control-height, --pixel-scale
   - Shapes: --radius-window, --radius-control, --radius-chip, --avatar-shape, --cut-tl, --cut-tr, --cut-br, --cut-bl
   - Materials: --bevel-light, --bevel-dark, --bevel-width, --shadow-raised, --shadow-pressed, --shadow-hard, --gradient-title, --gradient-button, --grain, --dither-pattern
   - Focus: --focus-ring, --default-button-ring
3. All CSS rules in `theme.css` MUST be strictly scoped under:
   [data-theme="curio-theme-<your-id>"], [data-theme="<your-id>"]
4. No external network URLs or @import statements (local zero-build security constraint). Use inline SVG data: URIs (data:image/svg+xml,...) for custom vector graphics.

### Advanced Design Channels (Include these in theme.css):
1. **Custom Brand Logo**: Replace the default folder logo in `.brand-title` by hiding `.brand-title svg` and injecting an inline vector SVG emblem via `.brand-title::before` using `background-image: url("data:image/svg+xml,...");`.
2. **Atmospheric Overlay**: Add an atmospheric environmental overlay on `body::after` (e.g. CRT scanlines, subtle vignette, CAD blueprint grid, or paper noise) with `pointer-events: none; position: fixed; inset: 0; z-index: 99999;`.
3. **Contrast Discipline**: Ensure `.sidebar`, `.catalog-select-dropdown`, `.filter-panel`, and `.filter-label` maintain high text contrast against their background. Never put dark text on dark surfaces.
4. **Signature Ornaments**: Add theme-specific ornaments (e.g. tilted rubber-stamp badges, chamfered cuts, brass buttons, or glowing terminal inputs).

---
### My Theme Concept:
[YOUR THEME IDEA GOES HERE - e.g. "GameBoy Pocket 4-shade olive green monochrome LCD aesthetic with pixelated typography, custom handheld D-pad logo, and LCD pixel grid overlay"]
```

---

## 3. How Advanced Custom Designs Work

Curio's architecture supports **6 complete design channels** procedurally:

### 1. Custom Brand Logo via Inline SVG
A theme can swap Curio's logo procedurally:
```css
/* Hide default SVG */
[data-theme="curio-theme-mytheme"] .brand-title svg {
  display: none !important;
}

/* Inject custom theme logo */
[data-theme="curio-theme-mytheme"] .brand-title::before {
  content: "" !important;
  display: inline-block !important;
  width: 22px !important;
  height: 22px !important;
  background-size: contain !important;
  background-repeat: no-repeat !important;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23FFA63D'%3E...%3C/svg%3E") !important;
  margin-right: 8px !important;
}
```

### 2. Custom Icon Replacement via CSS Masking
You can swap any UI icon (search, drawers, actions) with your own vector graphics:
```css
[data-theme="curio-theme-mytheme"] .search-icon {
  -webkit-mask: url("data:image/svg+xml,%3Csvg ...%3E%3C/svg%3E") no-repeat center !important;
  mask: url("data:image/svg+xml,%3Csvg ...%3E%3C/svg%3E") no-repeat center !important;
  background-color: var(--accent) !important;
}
[data-theme="curio-theme-mytheme"] .search-icon * {
  display: none !important;
}
```

### 3. Atmospheric Overlays (Scanlines, Grids, Grain)
Add full-screen environmental overlays:
```css
[data-theme="curio-theme-mytheme"] body::after {
  content: "" !important;
  position: fixed !important;
  inset: 0 !important;
  pointer-events: none !important;
  z-index: 99999 !important;
  background: repeating-linear-gradient(0deg, rgba(0,0,0,0.08), rgba(0,0,0,0.08) 2px, transparent 2px, transparent 4px) !important;
  box-shadow: inset 0 0 100px rgba(0,0,0,0.5) !important;
}
```

---

## 4. How to Install Your New Theme

### Option A: In-App ZIP Import (Recommended — No Terminal)
1. On your computer, put `manifest.json` and `theme.css` in a folder.
2. Compress the folder to a `.zip` archive (e.g. `curio-theme-mytheme.zip`).
3. Open Curio (`app.html`) in your browser.
4. Go to **Settings (⚙️) ➔ Plugin Hub**.
5. Click **📦 Import Theme (.zip)** and select your `.zip` file.
6. The theme is validated, extracted, and activated immediately!

### Option B: Folder Drop-In
1. Create a folder: `plugins/curio-theme-<your-id>/` containing `manifest.json` and `theme.css`.
2. Run in PowerShell:
   ```powershell
   powershell tools/update-plugin-index.ps1
   ```
3. Refresh Curio and select your theme in Settings!

---

## 5. Contrast Checklist for Themes

When inspecting your theme, check these three areas:
- **Sidebar Header**: Is `.brand-title` bright and readable against `.sidebar` background?
- **Catalog Dropdown**: Is `.catalog-select-dropdown` text bright and clear?
- **Filter Labels**: Are `.filter-label` ("GROUP BY:", "STATUS:") readable against `.filter-panel`?
- **Buttons**: Is button text (`--accent-text`) legible against the button background?
