# Curio Development Guidelines & Standards

## Theme Design & Art Direction Standard

In Curio, themes **must never be bland, shallow, or swappable color palettes**. Every theme must have its own **unique design, art style, and personality**—acting as an immersive artifact designed to transport the user into another machine, era, or reality.

When authoring, reviewing, or debugging themes in this repository, always enforce these principles:

### 0. Mandatory Visual Reference Calibration & Anti-Conflation
- **Visual Sheet Extraction**: Always unpack, inspect, and calibrate against the actual visual reference sheets in `research and references on the THEMES UI/` (e.g. `Theme System Atlas.zip` images such as `kit.jpg`, `kit-inv.jpg`, `kit-hud.jpg`, or images in `Screenshot refs/`) before writing CSS. Never invent a color scheme from text prompts alone.
- **Anti-Conflation Rule**: Contrast each new theme against existing themes in Curio. Never allow a new theme to borrow default colors or layout habits that blur its identity into another theme (e.g. Pixel Fantasy must use its authentic Slate-Blue `#3B4A66` & Warm Peach `#F3C9A5` palette rather than warm office browns that resemble TVA).

### 1. The 6-Channel Immersion Rule
Every theme must engage the complete design channels:
1. **Tokens**: Full 46-token contract compliance with intentional palette discipline.
2. **Parts**: Deep component-level styling across windows, cards, sidebars, buttons, inputs, and inspectors.
3. **Shapes**: Intentional silhouettes (0px brutalist blocks, 45° chamfers, 9-slice pixel corners, or curved CRT housings).
4. **Materials**: Tactile finishes (leather grain, cream laminate, brushed steel, warm timber, or parchment).
5. **Ornaments & Atmospheric Overlays**:
   - Use `body::after` or root pseudo-elements with `pointer-events: none` for atmospheric environmental textures (procedural 16-bit dungeon stone bricks, CRT scanlines, tungsten vignettes, CAD blueprint grids, tactile dither).
   - Add period signature details (tilted rubber stamps, dashed sewn stitching, sci-fi corner brackets, inventory slot recesses).
6. **Icons & Custom Logos**:
   - Swap the default folder icon in `.brand-title svg` with a theme-specific inline vector SVG emblem (`data:image/svg+xml`) via `.brand-title::before`.
   - Use CSS `mask-image` or themed glyph stand-ins for theme-specific UI icons.

### 2. Card & Component Anatomy Transformation
Cards and interactive controls must **never remain generic web components with recolored fills**. Their physical anatomy must morph to match the source artifact:
- **Game / Inventory**: 9-slice studded frames with 4-corner drop-shadowed rivets, sunken inventory slot cells (`box-shadow: inset 3px 3px 0 #000, inset -3px -3px 0 ...`), swallowtail quest ribbon title headers, and RPG stat gems (Ruby HP, Sapphire Mana, Emerald Clear).
- **Bureaucracy / Office**: Cream paper laminate blocks with hard offset shadows, ruled formfields, and tilted rubber stamps.
- **Glass / Aero**: Translucent frosted panels with white inner glare and glossy orb controls.
- **Tactile Keycaps**: Buttons must have 3D pixel or beveled depth and physically depress into the canvas on click (`transform: translate(2px, 3px)`).

### 3. Contrast Discipline & Accessibility
- **Dark Sidebar & Panels**: When styling dark surfaces (e.g. `.sidebar`, `.filter-panel`, `#catalog-selector`, `.select-custom`, `.tag-search-input`), explicitly set text and labels to high-contrast colors (cream `#EDE0C4`, gold `#FCE28A`, glowing amber `#FFA63D`, white `#FFFFFF`, or bright accent).
- Never allow elements to inherit dark text on dark surfaces. Always audit `.brand-title`, `.catalog-select-dropdown`, `.filter-label`, and search inputs.

### 4. Zero-Build Security Constraint
- All vector logos, textures, and ornaments must be procedural (CSS gradients, SVG data URIs).
- Never use external network URLs or `@import`.
- Keep plugins fully self-contained within their respective `plugins/` directories.
