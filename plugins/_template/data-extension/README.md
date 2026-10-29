# Curio Data Adapter Starter Template

This folder provides a complete boilerplate template for creating a **Data Extension plugin** for Curio.

---

## Files

- `manifest.json`: Defines the extension ID, target file extensions, and format metadata.
- `adapter.js`: Implements the `parse(raw, api, options)` and `serialize(items, catalog, api, options)` lifecycle methods.

---

## How to Create Your Own Adapter

1. Copy this folder into `plugins/<your-plugin-id>/` (e.g. `plugins/curio-data-csv`).
2. Update `manifest.json` with your plugin's unique `id`, `name`, and supported `fileExtensions`.
3. In `adapter.js`, replace the parsing and serialization logic with your custom parser.
4. Run `powershell tools/update-plugin-index.ps1` to register your adapter.
5. Your adapter is now active in Curio!
