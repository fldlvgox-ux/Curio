# Curio Data Extension Plugin — Cross-Agent Handoff Specification

> **Instructions for the AI Assistant / Remote Model:**
> You are tasked with generating a custom **Data Extension plugin** for the **Curio** web and desktop application.
> Read the contract specification below and output **two code blocks**:
> 1. `manifest.json` (metadata, supported formats, file extensions, and file references)
> 2. `adapter.js` (an ES6 object implementing `parse(raw, api, options)` and `serialize(items, catalog, api, options)`)

---

## 1. What is a Data Extension?

A Data Extension allows Curio to import from and export to external data formats (e.g. CSV, Markdown tables, YAML, Notion, Obsidian, JSON-LD, BibTeX) without modifying Curio's core `app.html` code.

---

## 2. The `DataExtensionAPI` Sandbox

Your `parse()` and `serialize()` methods receive an instance of `DataExtensionAPI` with these capabilities:

### `api.createItem(data)`
Creates a normalized Curio item with all required schema fields guaranteed:
```javascript
const item = api.createItem({
  title: 'Item Title',            // string (required)
  drawer: 'Category',             // string (optional, defaults to first drawer)
  status: 'Idea',                 // 'Idea' | 'In Progress' | 'Completed' | 'Archived'
  tags: ['retro', 'vintage'],     // array of strings
  rating: 4,                      // number 0 - 5
  notes: 'Item description...',   // string
  link: 'https://...',            // string
  logo: '',                       // base64 image or empty string
  gallery: []                     // array of image IDs or empty
});
```

### `api.getActiveCatalog()`
Returns active catalog metadata:
```javascript
const catalog = api.getActiveCatalog();
// { id: 'catalog-1', name: 'Synthesizers', drawers: ['Mono', 'Poly', 'Modular'], items: [...] }
```

### `api.getDrawers()`
Returns an array of drawer names in the active catalog (e.g. `['Inbox', 'Active', 'Archive']`).

### `api.getDefaultDrawer()`
Returns the first drawer name in the active catalog or `'Inbox'` if none exist.

### `api.showToast(message, type)`
Displays a notification toast (`'info'`, `'success'`, `'warn'`, `'danger'`).

### `api.sanitizeText(text)`
Encodes `&`, `<`, `>`, `"`, and `'` to prevent HTML/script injection in parsed content.

---

## 3. The `CurioDataAdapter` Interface

Your `adapter.js` must export a default object with `parse` and/or `serialize`:

```javascript
export default {
  /**
   * Parse raw text into an array of Curio Item objects.
   * @param {string} raw - Raw file string content
   * @param {DataExtensionAPI} api - Sandbox API
   * @param {Object} options - Custom options (e.g. { defaultDrawer: 'Inbox' })
   * @returns {Array<Object>|Promise<Array<Object>>} Array of Curio items
   */
  async parse(raw, api, options = {}) {
    const items = [];
    // ... parse input ...
    // items.push(api.createItem({ title: '...', drawer: '...' }));
    return items;
  },

  /**
   * Serialize Curio items into external text format.
   * @param {Array<Object>} items - Array of Curio items
   * @param {Object} catalog - Active catalog metadata
   * @param {DataExtensionAPI} api - Sandbox API
   * @param {Object} options - Custom serialization options
   * @returns {string|Promise<string>} Text representation
   */
  async serialize(items = [], catalog = {}, api, options = {}) {
    let output = '';
    // ... format items ...
    return output;
  }
};
```

---

## 4. Manifest Specification (`manifest.json`)

```json
{
  "id": "curio-data-my-format",
  "name": "My Format Adapter",
  "version": "1.0.0",
  "type": "data-extension",
  "contract": "1.0.0",
  "author": "Your Name",
  "description": "Imports and exports Curio items to My Custom Format.",
  "family": "data-format",
  "preview": null,
  "mountPoint": null,
  "files": {
    "adapter": "adapter.js"
  },
  "dataExtension": {
    "displayName": "My Custom Format (*.fmt)",
    "formats": ["myformat", "fmt"],
    "fileExtensions": [".fmt", ".txt"],
    "mimeType": "text/plain",
    "modes": ["import", "export"]
  }
}
```

---

## 5. Security & Verification Checklist

- [ ] **No external network calls**: Must run zero-build in local/sandbox environments without external CDN scripts.
- [ ] **Input Sanitization**: Use `api.sanitizeText()` on unvetted strings.
- [ ] **Drawer Safety**: Always fallback to `api.getDefaultDrawer()` when rows lack a drawer name.
- [ ] **Robust Parsing**: Tolerate empty lines, missing columns, or trailing commas gracefully.
