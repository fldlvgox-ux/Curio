# Curio Component Plugin Starter

This directory contains the starter template for building an interactive UI component for Curio.

## Structure
* `manifest.json`: Declares the plugin ID, name, mount point (`toolbar-actions`, `sidebar-top`, `sidebar-bottom`, `floating-widget`), and file references.
* `template.html`: The HTML markup for the widget.
* `script.js`: ES6 module exporting `{ init(api), destroy() }`.
* `styles.css`: Scoped CSS styles using Curio standard theme tokens (`var(--surface)`, `var(--text)`, etc.).

## How to Test
1. Copy this folder to `plugins/curio-component-<name>/`.
2. Edit `manifest.json`, `template.html`, and `script.js`.
3. In PowerShell, run: `powershell -File tools/update-plugin-index.ps1`.
