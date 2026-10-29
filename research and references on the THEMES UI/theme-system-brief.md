# Brief: Pluggable Theme System + 10 Reference Themes

## 0. Goal

Build a theme/plugin system for my app so that **any theme** (made by me, by other AI models, or loaded remotely) can restyle **any app** (calculator, database, dashboard, media player, profile page, etc.) without the app knowing which theme is active.

Then build 10 themes from the attached reference images to prove the contract works.

Hard rule: **each reference is its own theme. Never blend them.** Themes share only the contract (parts, tokens, channels), never visual traits.

I will attach the reference images. They are numbered below (Ref 1 to Ref 10). If an image is missing, ask for it. Do not guess.

---

## 1. Working method

1. **Phase 0 (foundation):** write the contract, manifest schema, loader, a neutral default theme, and two test pages (see section 6). Stop and summarize in under 10 lines.
2. **Phase 1 (round one, 5 themes):** Win98, QuickTime Aqua, HUD, Leather, Free Download Manager. Each must pass both test pages.
3. **Phase 2 (remaining 5):** Mac OS 8 / System 7, XP Luna, Winamp, Pixel Retro, QuickTime dark metal. These must work **without changing the contract**. If a theme forces a contract change, stop, say what changed and why, then re-verify earlier themes.
4. No mockup step. Build directly. Keep updates short and scannable.

Stack: single-file HTML friendly, no build step, no external requests. Vue 3 via CDN is fine for the demo shell. The theme system itself must be framework-agnostic (plain CSS + a small JS loader).

---

## 2. The contract

A theme styles **named parts** using **tokens**. Apps never reference theme details.

### 2.1 Six channels

| Channel | What it controls | Delivered as |
|---|---|---|
| **Tokens** | color, type, spacing, density, radii | CSS variables |
| **Parts** | styling of each named component | CSS scoped by `[data-part]` |
| **Shape** | chamfers, radii, window silhouette | `clip-path`, `border-radius`, SVG masks |
| **Material** | bevel, gloss, grain, shadow, gradient | CSS gradients, layered shadows, inline SVG filters (`feTurbulence`) |
| **Ornament** | brackets, stitching, ticks, tape, decorative text | Sanitized inline SVG snippets, CSS pseudo-elements |
| **Icons** | the icon set | SVG `<symbol>` sprite, swappable per theme |

### 2.2 Required tokens (every theme defines all of them)

- Color: `--bg`, `--surface`, `--surface-2`, `--text`, `--text-dim`, `--accent`, `--accent-text`, `--border`, `--select-bg`, `--select-fg`, `--danger`, `--ok`, `--warn`
- Type: `--font-ui`, `--font-display`, `--font-mono`, `--font-size-base`, `--font-smoothing`
- Space/density: `--space-1..5`, `--row-height`, `--control-height`, `--pixel-scale`
- Shape: `--radius-window`, `--radius-control`, `--radius-chip`, `--avatar-shape`, `--cut-tl`, `--cut-tr`, `--cut-br`, `--cut-bl`
- Material: `--bevel-light`, `--bevel-dark`, `--bevel-width`, `--shadow-raised`, `--shadow-pressed`, `--shadow-hard`, `--gradient-title`, `--gradient-button`, `--grain` (SVG filter id or `none`), `--dither-pattern`
- Focus/state: `--focus-ring`, `--default-button-ring`

Unused tokens are set to a harmless value (`none`, `0`), never omitted.

### 2.3 Parts list (`data-part="..."`)

| Group | Parts |
|---|---|
| Containers | `window`, `titlebar`, `menubar`, `toolbar`, `panel`, `header`, `banner`, `tabstrip`, `tab`, `statusbar`, `group` (collapsible), `sidebar` |
| Actions | `button` (variants: primary, secondary, icon, transport, split), `toggle`, `switch`, `chip` |
| Inputs | `slider` (H/V: track, fill, thumb, ticks), `checkbox`, `radio`, `textfield`, `dropdown` |
| Display | `readout` (LCD/timecode/KPI), `list`, `listrow`, `propertyrow` (icon, label, value), `statblock`, `badge`, `progress`, `segmentmap`, `visualizer`, `avatar`, `datagrid`, `tree`, `scrollbar` |
| Overlays/feedback | `dialog`, `alert`, `note` (sticky/notification) |
| Optional (shell-like apps) | `taskbar`, `taskbar-item` |

### 2.4 States

Every interactive part must style: `idle`, `hover`, `pressed`, `disabled`, `focus`, `selected`. Use `data-state` and `:hover`/`:active`/`:focus-visible`.

### 2.5 Content is not themed

Photos, album art, thumbnails, user media, and wallpapers are content. A theme frames them and never recolors them.

---

## 3. Theme package format

One theme = one JSON file (or JSON plus separate assets for remote loading):

```json
{
  "contract": "1.0",
  "id": "win98",
  "name": "Windows 98 Gray Bevel",
  "family": "bevel-os",
  "author": "model-or-person",
  "layers": ["tokens", "parts", "shape", "material", "icons"],
  "palettes": { "default": { "--bg": "#C0C0C0" } },
  "tokens": { "--font-ui": "Tahoma, 'MS Sans Serif', sans-serif" },
  "css": "[data-theme='win98'] [data-part='button'] { ... }",
  "icons": "<svg>...<symbol id='icon-close'>...</symbol></svg>",
  "ornaments": { "corner-bracket": "<svg>...</svg>" }
}
```

Notes:
- A theme may ship several `palettes` (like Winamp's Color Themes). Palettes change only color tokens, never structure.
- `family` groups skins that share a layout (for example QuickTime Aqua and dark metal).
- The loader scopes all theme CSS under `[data-theme="<id>"]` automatically and rejects CSS that escapes the scope.

---

## 4. Loader requirements

1. Read the manifest, validate against the schema, check `contract` version.
2. Check that all required tokens exist. Fill gaps from the default theme.
3. Inject tokens and scoped CSS, register the icon sprite, and sanitize ornament SVG (strip `<script>`, event handlers, `<foreignObject>`, external hrefs).
4. Switch themes at runtime with no reload (`data-theme` on the root).
5. On any failure, fall back to the default theme and show a short error. Never leave the app unstyled.
6. Support loading from: pasted JSON, file, URL.

### Security (remote themes are untrusted)

- **Allowed:** CSS, SVG, JSON, system fonts, `data:` URIs.
- **Forbidden:** JavaScript, `@import`, `url()` to anything except `data:`, `<iframe>`, `<object>`, `<foreignObject>`, `expression()`, external fonts, network requests, CSS that targets outside the theme scope.
- Optional later (not now): a sandboxed plugin layer (iframe or Shadow DOM plus limited API) for themes that change layout structure. Do not build it yet.

---

## 5. Rules for the reference themes

- Reproduce the **style**, not logos, brand marks, wordmarks, app icons, copyrighted wallpaper, or character art. Use original icons and neutral stand-in text.
- Placeholder or garbled text in a reference (e.g. "Fatch uissum") is not a requirement. Ignore it.
- Use only the references' own restraint: do not add accent colors or effects that the reference does not show.
- Textures are procedural (CSS gradients or inline SVG filters). No bitmap images.

---

## 6. Acceptance tests (required)

Build two test pages. Every theme must render both correctly with no theme-specific app code.

**Test page A, generic:** window with titlebar and menubar, alert, dialog, primary + secondary + icon + split button, toggle and switch, checkbox and radio, textfield, H slider and V slider, readout, progress bar, three chips, three-row list with icons, tab strip, avatar.

**Test page B, data:** tree sidebar, datagrid (header, normal row, alternate row, selected row, colored status text), two-level tabs, icon toolbar, segmentmap, statusbar with three segments, scrollbar.

Per theme checklist, which you report as a short table:
- [ ] All required tokens defined
- [ ] All parts and all six states styled
- [ ] Passes Page A and Page B
- [ ] No forbidden constructs (run the validator)
- [ ] Signature detail present (listed per theme below)
- [ ] Looks like **only** its own reference, with no traits from other themes

---

## 7. Theme briefs

Use only the matching reference for each.

### Ref 1 / Theme `macos8`: Mac OS 8 Appearance sheet (start with the **System 7** variant, then Ice and Onyx as palettes or sub-themes)
- Style: 1-bit-like bevel skin. Black/white (System 7), pale blue (Ice), black with yellow (Onyx).
- Material: 1-px bevels, flat fills, thin black outlines. Onyx adds hazard-stripe title bars.
- Shape: square corners.
- Signature: title bar with horizontal pinstripes and small square zoom/collapse boxes; default button has a heavy outer ring; On/Off segmented toggle.
- Difficulty: low.

### Ref 2 / Theme `hud`: Coral cyberpunk HUD
- Style: shape language. **One hue** (coral `#F2685F`-ish) plus near-black plum background and dark teal-slate secondary fills. Do not add other accent colors.
- Shape: **chamfered corners via `clip-path: polygon()` driven by `--cut-*` tokens. No border-radius anywhere.**
- Parts: primary button (solid coral, icon left, label right, tiny caption under it), secondary button (teal fill, coral text, corner-flag triangle), list row (flat slab, clipped edge), progress (segmented ticks in a bracket frame), alert (triangle icon plus boxed status tag), badge (number square), vertical side tab.
- Ornament (separate swappable SVG, theme must still work with ornament off): corner brackets, edge ruler ticks, binary text columns, barcode footer, terminal prompt line.
- Signature: **every button and panel has an optional caption line** in tiny uppercase.
- Type: uppercase condensed sans plus tiny mono captions.
- Difficulty: medium.

### Ref 3 / Theme `leather`: Leather, paper, brass
- Style: physical objects. 2 browns, 2 creams, 1 brass. Serif title, humanist sans body, handwriting font only for the `note` part (system-font fallback is fine).
- Material: leather grain on the frame (SVG `feTurbulence`), **stitched seam** (dashed inset border, orange thread), brushed-metal sidebar, **paper with torn/deckled edges** (SVG mask preset), glossy brass pill button.
- Depth rules: paper sits **raised** on leather, toggles are **pressed** into metal. Declare raised or pressed for every part.
- Signature: stitching, a taped and slightly rotated sticky `note`, brass primary button.
- Difficulty: high (texture).

### Ref 4 / Theme `winamp`: Winamp-style steel-blue instrument panel
- Style: dense instrument panel. Brushed silver, glowing LCD blue on dark navy.
- Parts to nail: **`readout`** (glow, monospace/pixel digits, scrolling marquee, small bitrate labels), round icon-only **transport buttons**, **sliders** (track, fill, thumb, tick marks, dB labels), angled **folder tabs**, toggle pills (ON/AUTO/PRESETS), `visualizer` bars.
- Density: compact (`--row-height` and `--control-height` small).
- Palettes: ship at least 2 color palettes (e.g. steel-blue default, a green variant) to prove palettes work.
- Difficulty: high (sliders).

### Ref 5 / Theme `pixel`: Pixel-art periwinkle retro
- Style: flat pixel grid. Periwinkle panels, deeper indigo title bars/chips, near-white fields, navy text. One hue family.
- Rules: **pixel/bitmap font** (system or data-URI), `image-rendering: pixelated`, no anti-aliasing tricks, **hard offset shadow with no blur** (`--shadow-hard: 4px 4px 0`), 1-px dark outlines, everything snaps to `--pixel-scale`.
- Parts: pill chips, title bar with X box, modal dialog with icon and two buttons, `propertyrow` (icon, tiny caps label, bold value), scrollbar with arrow boxes, numbered-medal list rows.
- Composition: overlapping, slightly offset windows. Floating translucent squares as background ornament.
- Icons: a pixel icon set (original, not copied).
- Difficulty: lowest.

### Ref 6 / Theme `win98`: Windows 98 gray bevel
- Style: strict bevel. `#C0C0C0` surfaces, `#000080` title bar, black text, white and dark-gray bevel colors.
- Material: **2-px raised bevel (white top-left, dark gray bottom-right). Pressed or selected flips to inset. Dither (checkerboard) fill marks the selected tab or nav item.** Etched dividers (dark line plus white line).
- Shape: all square, except `avatar` which stays round (token `--avatar-shape`).
- Parts: title bar with min/max/close boxes, menu bar, `statblock`, `button` split variant, icon tabstrip, bottom icon nav bar, scrollbar with arrow boxes.
- Restraint: one gray, one navy, black text. Nothing else.
- Difficulty: low.

### Ref 7 / Theme `xp`: Windows XP Luna
- Style: gradient gloss plus rounded frame. Blue gradient title bars, cream-beige `#ECE9D8` window bodies, white content areas. Green accent for go/start actions, orange accent line under dialog banners. Tahoma-like type at 8 to 11px.
- Material: **title bar gradient is most of the look** (lighter at top, highlight band). Glossy buttons, soft window shadow.
- Shape: **rounded top corners (about 8px), square bottom**. Controls about 3px radius. Close button is red and distinct.
- Parts: collapsible `group` (task pane: header, chevron, link list), `banner` (gradient strip with title and art slot), default-button **blue inner ring**, address-bar style `dropdown` plus green go button, optional `taskbar`.
- Do not use the Bliss wallpaper or Microsoft artwork. Use a neutral gradient background token.
- Difficulty: medium.

### Ref 8 / Theme `aqua-metal`: QuickTime-style brushed metal (family `media-metal`)
- Style: brushed metal and gloss. Silver-gray, pale yellow-green readout strip, black text, three colored window lights (red/yellow/green).
- Material: **horizontal brushed grain via SVG `feTurbulence`** (low x frequency, high y frequency), glossy round glass buttons with highlights, soft drop shadow.
- Shape: rounded window, curved "wing" lower panel, corner resize grip.
- Parts: `readout` (recessed pale-green timecode field with scrubber track and diamond marker), `transport` buttons with a **larger primary (play)**, volume slider with speaker icon.
- Difficulty: medium-high.

### Ref 9 / Theme `dark-metal`: same family as Ref 8, different skin
- Same layout and parts as `aqua-metal`. Only material and palette differ: charcoal matte metal, **embossed/pressed-in** round buttons instead of glossy ones, squarer corners, no colored lights, volume-bars glyph.
- Must reuse the family's shared parts map. Do not duplicate structure.
- No brand marks (ignore the logo in the reference).
- Difficulty: medium.

### Ref 10 / Theme `datautil`: Free Download Manager-style dense utility
- Style: standard Windows 7-era chrome. Light gray-blue surfaces, white data areas, **blue selection row**, green and red status text, about 11px system sans.
- Parts: icon toolbar with large colorful glossy icons (original icons), `tree` (expand/collapse glyphs, indent), `datagrid` (sortable header, row selection, status-colored text), two-level `tabstrip`, three-segment `statusbar`, `segmentmap` (grid of cells: empty/partial/full).
- Density: compact, the personality comes from the icon set, not the chrome.
- This theme is the main test for Page B.
- Difficulty: medium.

---

## 8. The "theme-maker prompt" deliverable

After the system works, produce **one reusable prompt** I can paste into other AI models so they generate compatible themes. It must be self-contained and include:

1. The contract (channels, required tokens, parts list, states).
2. The manifest schema and one complete small example theme.
3. The security rules (allowed/forbidden list).
4. A slot for **one** theme brief (describe the style, list material, shape, signature detail, palette limit).
5. Hard rules: output only the theme JSON, no commentary; no JS; no external requests; no logos or brand marks; ignore placeholder text in references; do not add colors the reference does not show.
6. Instruction to self-check against the Page A and Page B part list before replying.

Also produce a short **per-theme brief template** (style type, palette limit, material per part, raised vs pressed, shape rule, ornament, icons, signature detail, what to ignore) so I can write new briefs in the same format.

---

## 9. Final deliverables

1. Contract spec (this document's section 2, cleaned up) plus manifest JSON schema
2. Loader and validator
3. Default theme
4. Test Page A and Test Page B
5. The 10 themes, in the phases above
6. The theme-maker prompt and per-theme brief template
7. A short report table: theme × checklist results, plus any contract changes made and why
