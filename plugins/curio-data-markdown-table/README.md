# Curio Data Adapter: Markdown Table

A modular drop-in **Data Extension plugin** for Curio that provides bidirectional import and export between Curio catalog items and GitHub Flavored Markdown (GFM) tables.

---

## Capabilities

1. **Table Import**: Automatically parses column headers like `Title`, `Drawer`, `Status`, `Tags`, `Rating`, `Notes`, and `Link`.
2. **List Import (Fallback)**: Can parse standard markdown task lists (`- [x] Item title #tag (Drawer)`).
3. **Table Export**: Exports full catalog data with escaped pipes and clean formatting.

---

## File Structure

```
curio-data-markdown-table/
├── manifest.json       # Plugin metadata and supported format configuration
├── adapter.js          # ES6 Data Adapter with parse() and serialize()
└── README.md           # Documentation
```

---

## Usage in Curio

Import markdown files directly via Curio's **Settings > Data Extensions > Import File** or through the JavaScript API:

```javascript
// Import
const markdownText = `
| Title | Drawer | Status | Tags | Notes |
|---|---|---|---|---|
| Korg MS-20 | Synthesizers | In Progress | analog, vintage | Classic semi-modular mono synth |
`;

await CurioData.importData(markdownText, 'markdown');

// Export
const exportedMd = await CurioData.exportData('markdown');
console.log(exportedMd);
```
