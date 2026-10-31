# Curio Development Guidelines & Standards

## Theme Design & Art Direction Standard

In Curio, themes **must never be bland, shallow, or swappable color palettes**, nor should they follow a **formulaic cookie-cutter checklist**. Every theme must have its own **unique design, physical form-factor, tactile materials, and authentic personality**—faithfully capturing the visual reference as an immersive artifact.

When authoring, reviewing, or debugging themes in this repository, always enforce these principles:

### 0. Authentic Visual Reference Fidelity & Anti-Conflation
- **Visual Reference First**: Always inspect and calibrate against the actual visual reference sheets in `research and references on the THEMES UI/` (e.g. `Theme System Atlas.zip` images such as `winamp.jpg`, `kit.jpg`, `kit-inv.jpg`, `kit-hud.jpg`, or images in `Screenshot refs/`).
- **Faithful Canvas & Palette**: Never force every theme into a dark-mode web dashboard. If the reference is a light brushed-steel chassis on a periwinkle desktop (like Winamp), a warm cream paper document (like TVA), or a crisp ivory System 7 window, the theme must faithfully reflect that lightness, depth, and material finish.
- **Radical Diversity (Anti-Conflation)**: Each theme must look completely distinct in color, silhouette, density, and layout feel. Themes share only the 46-token contract, never visual habits or identical dark layouts.

### 1. Organic Immersion Over Formulaic Checklists
Avoid mechanically pasting decorative SVG pseudo-elements onto generic web blocks. Instead, transform the actual interface components to match the physical artifact:
1. **Tokens**: Full 46-token contract compliance with intentional palette discipline.
2. **Parts**: Deep component-level styling across windows, cards, sidebars, buttons, inputs, and inspectors.
3. **Shapes & Silhouettes**: Intentional forms (beveled brushed metal slabs, chamfered HUD blocks, notebook spiral binding, or 9-slice pixel frames).
4. **Materials & Finish**: Authentic tactile textures (brushed aluminium, cream laminate, leather grain, warm paper, or CRT glass).
5. **Open Breathing Room**: Allow the canvas and content to breathe. Avoid overcrowding every surface with decals or dark borders.
6. **Icons & Custom Logos**: Themed vector stand-in icons and brand emblems appropriate for that specific universe.

### 2. Component & Layout Anatomy Transformation
Morph the interactive components into the physical form factor of the source artifact:
- **Audio / Instrument Panel (e.g. Winamp)**: Brushed steel-blue chassis, convex circular metallic transport keys, horizontal fader rails, angled trapezoid tabs, and recessed dark navy LCD display screens.
- **Game / Inventory (e.g. Pixel Fantasy)**: Recessed inventory slot cells, studded 9-slice frames, swallowtail ribbon headers, and RPG stat gems.
- **Bureaucracy / Office (e.g. TVA)**: Cream paper laminate blocks, ruled form fields, hard offset drop shadows, and tilted rubber stamps.
- **Retro OS (e.g. Mac OS 8 / Win95)**: Crisp 3D beveled chrome, pinstriped titlebars, raised tactile buttons, and classic dialog styling.

### 3. Contrast Discipline & Accessibility
- **Intentional Contrast**:
  - Dark surfaces (LCD screens, terminal readouts, dark panels) MUST have bright, high-contrast text (electric-cyan, phosphor green, glowing amber, or pure white).
  - Light surfaces (brushed steel, paper, ivory, beige) MUST have dark, crisp text (deep obsidian, navy, or rich charcoal) with subtle relief text-shadows where appropriate.
- Never allow elements to inherit unreadable low-contrast text (e.g. light gray on light gray, or dark blue on black).

### 4. Zero-Build Security Constraint
- All vector logos, textures, and ornaments must be procedural (CSS gradients, SVG data URIs).
- Never use external network URLs or `@import`.
- Keep plugins fully self-contained within their respective `plugins/` directories.
