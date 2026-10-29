# Curio Component Plugin — Cross-Agent Handoff Specification

> **Instructions for the AI Assistant / Remote Model:**
> You are tasked with generating an interactive UI component plugin for the **Curio** web and desktop application.
> Read the contract specification below and output **four code blocks**:
> 1. `manifest.json` (metadata, mount point, and file references)
> 2. `template.html` (the HTML markup of your widget)
> 3. `script.js` (an ES6 class or object with `init(api)` and `destroy()` lifecycle methods)
> 4. `styles.css` (custom CSS scoped strictly under `.curio-comp-<id>`)

---

## 1. Mount Points Available

Choose one of these valid mount points in `manifest.json`:
* `"toolbar-actions"`: Renders inline buttons or compact controls in the top toolbar.
* `"sidebar-top"`: Placed above catalog drawer lists (ideal for fast search or catalog switchers).
* `"sidebar-bottom"`: Placed above the storage bar in the sidebar (ideal for gauges, mini-status).
* `"floating-widget"`: Docked at the bottom-right of the viewport (ideal for audio players, inspect HUDs).

---

## 2. The `ComponentAPI` Sandbox

Your `init(api)` function receives an instance of `ComponentAPI` with these capabilities:

### `api.container`
The root DOM element (`HTMLElement`) for your widget. Your `template.html` is automatically placed inside it. You can query elements using:
```js
const btn = api.container.querySelector('.my-action-btn');
```

### `api.state` (Safe Read-Only State Getters)
* `api.state.getActiveCatalog()`: Returns `{ id, name, icon, items: [], drawers: [] }`
* `api.state.getCatalogs()`: Returns array of all loaded catalogs
* `api.state.getItems()`: Returns items in the currently active catalog
* `api.state.getDrawers()`: Returns drawer categories in the currently active catalog
* `api.state.getActiveView()`: Returns current view mode (`'grid'`, `'detailed'`, `'list'`, `'kanban'`, `'grouped'`)

### `api.storage` (Isolated Key-Value Storage)
* `api.storage.get(key, defaultValue)`: Retrieve a saved setting
* `api.storage.set(key, value)`: Save a setting (persisted across sessions)
* `api.storage.remove(key)`: Clear a setting

### `api.showToast(message, type)`
Display a notification toast in Curio (`type`: `'info'`, `'success'`, `'warn'`, `'danger'`).

### `api.on(event, handler)` & `api.off(event, handler)`
Listen to Curio lifecycle events:
* `'catalog-changed'`: Detail `{ catalogId }`
* `'item-selected'`: Detail `{ item }`
* `'theme-changed'`: Detail `{ themeId }`

---

## 3. Security & Design Constraints

1. **Strict CSS Scoping**: All CSS rules must begin with `.curio-comp-<your-id>`.
2. **Use Curio CSS Variables**: Style using `var(--bg)`, `var(--surface)`, `var(--text)`, `var(--accent)`, `var(--border)`, `var(--radius-control)`, etc. This ensures your widget automatically adapts to all 17 themes!
3. **Clean Teardown**: Always remove intervals, timers, and event listeners inside `destroy()`.
4. **No External Network Calls**: Everything must function 100% offline.

---

## 4. Expected Output Format

### Block 1: `manifest.json`
```json
{
  "id": "curio-component-<name>",
  "name": "<Display Name>",
  "version": "1.0.0",
  "type": "component",
  "contract": "1.0.0",
  "author": "<Author or Model>",
  "description": "<One sentence purpose>",
  "mountPoint": "floating-widget",
  "files": {
    "template": "template.html",
    "script": "script.js",
    "css": "styles.css"
  }
}
```

### Block 2: `template.html`
```html
<div class="my-widget-card">
  <div class="my-widget-title">Widget Title</div>
  <div class="my-widget-body">Content goes here</div>
</div>
```

### Block 3: `script.js`
```js
export default {
  async init(api) {
    this.api = api;
    // Bind buttons, subscribe to events
    api.on('catalog-changed', (detail) => {
      // update widget
    });
  },
  destroy() {
    // cleanup
  }
};
```

### Block 4: `styles.css`
```css
.curio-comp-<name> .my-widget-card {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  border-radius: var(--radius-control);
  padding: var(--space-2);
}
```
