# How to Create a Curio Theme Plugin Using Any AI Model

This guide walks you through generating and installing custom Curio themes using **any external AI model** (such as ChatGPT, Claude, Gemini, DeepSeek, or local LLMs).

No coding knowledge is required. You can have a new theme live in Curio in under 2 minutes.

---

## ⚡ Quick 30-Second Summary

1. **Copy** the prompt from [Section 2](#2-copy--paste-prompt-for-the-other-ai) into your AI.
2. **Tell it your theme idea** (e.g. *"GameBoy LCD"*, *"Solarized Dark"*, *"Barbiecore Pink"*).
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

Please generate two files:
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
   [data-theme="curio-theme-<your-id>"]
4. No external network URLs or @import statements (local zero-build security constraint).

---
### My Theme Concept:
[YOUR THEME IDEA GOES HERE - e.g. "GameBoy Pocket 4-shade olive green monochrome LCD aesthetic with pixelated typography and retro handheld nostalgia"]
```

---

## 3. What the AI Will Output

The AI will output two files. Here is what they look like:

### File 1: `manifest.json`
```json
{
  "id": "curio-theme-gameboy",
  "name": "GameBoy Pocket",
  "version": "1.0.0",
  "type": "theme",
  "contract": "1.0.0",
  "author": "Community Designer",
  "description": "Authentic 4-shade olive green monochrome LCD handheld aesthetic.",
  "family": "retro-handheld",
  "preview": null,
  "files": {
    "css": "theme.css"
  },
  "tokens": {
    "--bg": "#8b956d",
    "--surface": "#9bbc0f",
    "--surface-2": "#8bac0f",
    "--text": "#0f380f",
    "--text-dim": "#306230",
    "--accent": "#0f380f",
    "--accent-text": "#9bbc0f",
    "--border": "#306230",
    "--select-bg": "#0f380f",
    "--select-fg": "#9bbc0f",
    "--danger": "#8b0000",
    "--ok": "#0f380f",
    "--warn": "#306230",
    "--font-ui": "'Courier New', monospace",
    "--font-display": "'Courier New', monospace",
    "--font-mono": "'Courier New', monospace",
    "--font-size-base": "12px",
    "--font-smoothing": "none",
    "--space-1": "4px",
    "--space-2": "8px",
    "--space-3": "12px",
    "--space-4": "16px",
    "--space-5": "24px",
    "--row-height": "28px",
    "--control-height": "24px",
    "--pixel-scale": "1",
    "--radius-window": "0px",
    "--radius-control": "0px",
    "--radius-chip": "0px",
    "--avatar-shape": "0%",
    "--cut-tl": "0px",
    "--cut-tr": "0px",
    "--cut-br": "0px",
    "--cut-bl": "0px",
    "--bevel-light": "transparent",
    "--bevel-dark": "transparent",
    "--bevel-width": "0px",
    "--shadow-raised": "none",
    "--shadow-pressed": "none",
    "--shadow-hard": "none",
    "--gradient-title": "none",
    "--gradient-button": "none",
    "--grain": "none",
    "--dither-pattern": "none",
    "--focus-ring": "0 0 0 2px #0f380f",
    "--default-button-ring": "0 0 0 1px #0f380f"
  }
}
```

### File 2: `theme.css`
```css
/* Scoped strictly to your theme ID */
[data-theme="curio-theme-gameboy"] {
  background-color: var(--bg) !important;
  color: var(--text) !important;
}

[data-theme="curio-theme-gameboy"] .top-bar {
  background: var(--surface);
  border-bottom: 2px solid var(--border);
}

[data-theme="curio-theme-gameboy"] .sidebar {
  background: var(--surface-2);
  border-right: 2px solid var(--border);
}

[data-theme="curio-theme-gameboy"] .btn-primary {
  background: var(--accent);
  color: var(--accent-text);
  border: 1px solid var(--border);
  border-radius: 0;
}
```

---

## 4. How to Install Your New Theme

You have two simple ways to install your new theme:

### Option A: In-App ZIP Import (Recommended — 100% No Terminal)
1. On your computer, create a new folder named `my-theme`.
2. Save `manifest.json` and `theme.css` inside that folder.
3. Right-click the folder and compress it to a `.zip` file (e.g. `curio-theme-gameboy.zip`).
4. In your browser or desktop app, open Curio (`app.html`).
5. Click **Settings (⚙️)** in the sidebar, then scroll to **Plugin Hub**.
6. Click **📦 Import Theme (.zip)** and select your `.zip` file.
7. Curio unpacks and activates your new theme immediately!

### Option B: Folder Drop-In (For Developers)
1. Create a folder inside the `plugins/` directory:
   ```
   plugins/curio-theme-<your-id>/
   ├── manifest.json
   └── theme.css
   ```
2. Open PowerShell in the project root and run:
   ```powershell
   powershell tools/update-plugin-index.ps1
   ```
3. Refresh `app.html` in your browser. Your theme will appear in the Settings theme picker!

---

## 5. Inspiration Ideas to Prompt the AI

Here are prompt ideas you can copy directly into the template:

- **1970s Dieter Rams / Braun Calculator**:
  *"Cream white matte surfaces (#f4f1ea), dark slate buttons (#2b2d2f), bright orange accent button (#ff5500), Helvetica font, ultra clean minimalism."*
- **Cyberpunk Neo-Tokyo 2077**:
  *"Pitch black OLED background (#050508), acid yellow high-contrast highlights (#fcee0a), cyan electric borders (#00f0ff), chamfered tech corners."*
- **Vintage Parchment & Leather**:
  *"Warm aged paper textures (#f5e6c8), dark sepia ink typography (#2c1d11), antique brass accents (#b58d3d), typewriter font."*
- **Dracula / Vampire Night**:
  *"Deep purple-navy canvas (#282a36), pastel pink accents (#ff79c6), cyan secondary (#8be9fd), soft dark mode contrast."*

---

## 6. Safety & Troubleshooting

- **Text is hard to read?** Make sure `--text` has high contrast against `--bg` and `--surface`.
- **Button text unreadable?** Set `--accent-text` to either `#ffffff` or `#000000` depending on whether `--accent` is dark or light.
- **Rules not applying?** Ensure every rule in `theme.css` starts with `[data-theme="curio-theme-<your-id>"]`.
