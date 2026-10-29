# Curio Plugin & Theme Kit

Welcome to the Curio Plugin Directory.

## How to Add a New Theme

### Option 1: Drop-in Folder (Desktop or Local Dev)
1. Create a folder here named `curio-theme-<name>` (e.g. `plugins/curio-theme-neon/`).
2. Add your `manifest.json` and `theme.css`.
3. Add a `preview.png` (optional, 320x200px recommended).
4. Run `powershell ./tools/update-plugin-index.ps1` to refresh `plugin-index.json`.
5. Launch Curio — your new theme will appear instantly in the Settings theme picker!

### Option 2: Upload via Settings Modal (Web / PWA / Desktop)
1. In Curio, open **Settings -> Themes**.
2. Click **"Import Theme (.zip)"**.
3. Select any packaged theme `.zip` file containing `manifest.json` and `theme.css`.
4. Curio will unpack and register the theme immediately without reloading.

### Option 3: Cross-Agent AI Generation
1. Open `HANDOFF.md` in this directory.
2. Copy the entire file content.
3. Open any AI model (Claude, GPT, Gemini, or a local LLM).
4. Paste `HANDOFF.md` and attach your `BRIEF_TEMPLATE.md` or screenshot ideas.
5. Save the generated `manifest.json` and `theme.css` directly into a new folder here.
