# Curio Development Guidelines & Standards

## Theme Design & Art Direction Standard

In Curio, themes must **never be shallow color palette swaps**. Every theme is an immersive artifact designed to transport the user into another machine, era, or reality.

When authoring, reviewing, or debugging themes in this repository, always enforce these principles:

### 1. The 6-Channel Immersion Rule
Every theme must engage the complete design channels:
1. **Tokens**: Full 46-token contract compliance with intentional palette discipline.
2. **Parts**: Deep component-level styling across windows, cards, sidebars, buttons, inputs, and inspectors.
3. **Shapes**: Intentional silhouettes (0px brutalist blocks, 45° chamfers, 9-slice pixel corners, or curved CRT housings).
4. **Materials**: Tactile finishes (leather grain, cream laminate, brushed steel, warm timber, or parchment).
5. **Ornaments & Atmospheric Overlays**:
   - Use `body::after` or root pseudo-elements with `pointer-events: none` for atmospheric environmental textures (CRT scanlines, tungsten vignettes, CAD blueprint grids, tactile dither).
   - Add period signature details (tilted rubber stamps, dashed sewn stitching, sci-fi corner brackets, inventory slot recesses).
6. **Icons & Custom Logos**:
   - Swap the default folder icon in `.brand-title svg` with a theme-specific inline vector SVG emblem (`data:image/svg+xml`) via `.brand-title::before`.
   - Use CSS `mask-image` or themed glyph stand-ins for theme-specific UI icons.

### 2. Contrast Discipline & Accessibility
- **Dark Sidebar & Panels**: When styling dark surfaces (e.g. `.sidebar`, `.filter-panel`, `#catalog-selector`, `.select-custom`, `.tag-search-input`), explicitly set text and labels to high-contrast colors (cream `#EDE0C4`, gold `#FCE28A`, glowing amber `#FFA63D`, white `#FFFFFF`, or bright accent).
- Never allow elements to inherit dark text on dark surfaces. Always audit `.brand-title`, `.catalog-select-dropdown`, `.filter-label`, and search inputs.

### 3. Zero-Build Security Constraint
- All vector logos, textures, and ornaments must be procedural (CSS gradients, SVG data URIs).
- Never use external network URLs or `@import`.
- Keep plugins fully self-contained within their respective `plugins/` directories.
