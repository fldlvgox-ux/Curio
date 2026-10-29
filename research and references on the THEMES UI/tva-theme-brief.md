# Appendix: Theme `tva` (Theme #16): Retro-futurist bureaucracy

Companion to `theme-system-brief.md`. Uses the same contract (channels, tokens, parts, states, loader, security rules). Nothing here changes the contract except the additions listed in section 9.

**Private use only, but original stand-ins are still required** (decision from Q&A). Never reproduce the show's emblem, mascot, characters, artwork, or title lettering.

**Reference images:** I will attach screenshots of the show's sets, screens, and signage. Use them to calibrate every provisional value marked `(provisional)` below. If a screenshot contradicts this brief, the screenshot wins, and you tell me what changed. Do not mix traits from any other theme.

---

## 1. Research basis and confidence

| Claim | Confidence | Where it shows up |
|---|---|---|
| Creative brief: "Mad Men meets Blade Runner" | High (production designer and creator interviews) | Overall mood |
| Intentional **paradox**: huge stoic brutalist forms vs. mid-century-modern surfaces, palette, and playful patterns | High | Shape and material split |
| Warm palette of brown, red, gold; whimsical patterns; orange plastic fixtures; orange with brown and grey with chartreuse as era pairings | High / medium | Palette |
| Yellow tungsten lighting, sepia-tinted saturated look, 1950s-style public-info posters | Medium | Screen tint overlay, poster styling |
| Signage branding described by the designer as roadside-station style: bold type and color combinations | High | Signage |
| Oversized mid-century "supergraphics" | High | Supergraphic mode |
| Stepped, blocky, ziggurat-like building language | Medium | Frame shape |
| CRT-style screens are mostly green with amber variants, handheld video is digitized to monochrome 8-bit, orange tint echoes 1970s SELF-SCAN displays | High | Screen layer |
| Monitors were built props, not real CRTs, with graphics added in post. Chronomonitors have rounded, organic housings | High | Screen housing shape |
| Graphics blend 1960s aesthetics with 1980s tone | Medium | Type and screen mix |
| A "muted grey, brown, sickly green" palette | **Low** (low-quality sources, conflicts with the designer) | **Not used.** At most, a possible screen-only effect |
| Exact typeface | **Unverified.** Never claim a font is "the" TVA font | Use "geometric sans in the style of" |

## 2. Decisions locked in Q&A

| Question | Decision |
|---|---|
| Surfaces | **CRT and monitor screens** + **architecture and signage**. No full office-paperwork surface, apart from the stamp and field parts below |
| Realism | **Hybrid**: flat graphic signage and frames around skeuomorphic screens |
| Palettes | **One palette: Warm office**. No green or amber screen palette |
| Supergraphic signage | **Both, switchable** via `--supergraphic: on/off` |
| CRT effects | **Both, switchable** via `--crt-level: off | light | full` |
| Shape | **Blocky frames, rounded screens** |
| Type | **Geometric sans + mono for screens** |
| Extra parts | Timeline visualizer, department header, stamp + form field |
| Motion | **Subtle**, all disabled under reduced-motion |
| Naming | **Original stand-ins** |

Note: with only one palette, screens use the **warm orange-amber ink on dark brown-black**, a monochrome screen ink derived from the same palette (described in the sources as an orange tint). Do not add green.

## 3. Style summary

A bureaucracy built from mid-century office design and Cold-War brutalism. Heavy blocky frames and flat, bold signage, with warm brown, orange, and gold surfaces, wrapped around rounded, glowing monochrome screens. It should feel friendly on the surface and a little oppressive underneath. No gloss, no glass, no gradients on chrome.

**Signature details** (must be present):
1. Heavy stepped or blocky frame with flat, matte color blocks
2. Oversized geometric supergraphic shape behind content when `--supergraphic: on`
3. Rounded monochrome screen with an orange-amber ink, scanline and glow effects scaled by `--crt-level`
4. Uppercase geometric-sans signage with a department code
5. A stamped status label

## 4. Tokens (all values provisional; calibrate from screenshots)

**Color (Warm office):**

| Token | Starting value | Role |
|---|---|---|
| `--bg` | `#2A1D14` | Deep brown, page background |
| `--surface` | `#EDE0C4` | Cream paper and laminate |
| `--surface-2` | `#D9C7A0` | Darker cream, secondary panels |
| `--text` | `#2B1A10` | Dark brown ink |
| `--text-dim` | `#6B5338` | Secondary text |
| `--accent` | `#D9822B` | Orange, main brand block |
| `--accent-2` | `#E0A82E` | Gold, highlights and signage blocks |
| `--danger` | `#9A3B26` | Red-brown, stamps and warnings |
| `--ok` | `#7C8A3A` | Muted chartreuse (era pairing), used sparingly |
| `--screen-bg` | `#16100A` | Near-black brown screen |
| `--screen-ink` | `#FFA63D` | Orange-amber screen ink |
| `--screen-ink-dim` | `#8A5320` | Dim screen ink |
| `--tint-tungsten` | `rgba(255,190,90,.08)` | Optional warm sepia overlay |

Screens use only `--screen-bg`, `--screen-ink`, `--screen-ink-dim`. Selected and inverted states swap bg and ink. No other colors on a screen.

**Type:**

| Token | Value |
|---|---|
| `--font-ui` | System geometric-sans stack (e.g. `"Jost", "Century Gothic", "Futura", "Avenir Next", system-ui, sans-serif`). Never claim it is the show's font. |
| `--font-display` | Same family, bold, uppercase, wide tracking |
| `--font-mono` | System monospace for screens (`ui-monospace, "Courier New", monospace`) |
| `--font-screen` | Monospace or a data-URI pixel face for CRT text |

**Shape:**

| Token | Value |
|---|---|
| `--radius-window`, `--radius-control`, `--radius-chip` | `0` (frames and controls are blocky) |
| `--radius-screen` | `14px` to `28px` (rounded screens, provisional) |
| `--cut-*` | Stepped corner via `clip-path`, 2 to 3 steps (ziggurat feel), optional |
| `--bevel-width` | `0` (no bevels) |

**Material:** `--shadow-hard: 4px 4px 0 var(--bg)` for flat layering. No soft shadows, no gradients on chrome. Optional subtle `--grain` (paper) as an SVG `feTurbulence` at very low opacity.

**New tokens:**
`--supergraphic` (on/off), `--supergraphic-shape` (preset name), `--crt-level` (off/light/full), `--scanline-opacity`, `--phosphor-glow`, `--screen-curve`, `--tint-tungsten`.

## 5. Part styling

| Part | Treatment |
|---|---|
| `window`, `panel` | Heavy flat cream block, thick dark-brown outline, stepped or blocky silhouette, hard offset shadow |
| `titlebar`, `header` | Solid orange block, uppercase geometric sans, a small code tag on the right |
| `sidebar` | Dark brown block with gold index markers |
| `tabstrip`, `tab` | Flat folder-style tabs, selected = filled orange, idle = cream |
| `button` primary | Solid orange block, uppercase, dark text, pressed = shift 2px into its shadow |
| `button` secondary | Cream block, thick outline |
| `button` icon/transport | Square with a thick outline. No round gel or glass |
| `toggle`, `switch` | Chunky rocker or slab, orange = on |
| `checkbox`, `radio` | Square and circle, thick outline, filled mark |
| `slider` | Flat track, blocky thumb, tick marks |
| `list`, `listrow` | Flat rows with a code column and a colored status block |
| `datagrid` | Cream rows, dark header, selected row = orange |
| `badge`, `chip` | Flat labels, uppercase |
| `alert`, `dialog` | Block frame with a hazard-free header bar, **stamp** for status |
| `statusbar` | Dark brown strip, gold text |
| `scrollbar` | Block thumb, flat arrows |
| **`screen`** | Rounded recessed display inside a heavy bezel. Contains `readout`, `visualizer`, and the timeline. Uses the screen palette only |
| `readout` | Monospace, orange-amber on dark, blinking cursor, optional glow |
| `visualizer` | Text-glyph or block bars in screen ink |

Content (photos, thumbnails) is never recolored. The surface it sits on is part of the theme.

## 6. New parts (add to the contract, see section 9)

**`timelinechart`**
- A branching timeline drawn on a `screen`: a horizontal main line, side branches, node markers, labeled ticks.
- Inline SVG, one ink. Branch nodes, a "pruned" branch style (dashed), and a current-position marker.
- Must work as a generic history, version, or flow chart for any app.

**`deptheader`**
- Signage-style header: department code (e.g. `DEPT. 04`), uppercase title, and an optional supergraphic block.
- Three variants: `block` (solid color), `stripe` (title on a stripe), `poster` (large type over a supergraphic).

**`stamp`**
- Rubber-stamp status label: uppercase, thick outline, rotated 2 to 4 degrees, slight ink-texture mask via SVG filter.
- Variants: `approved`, `pending`, `denied`, `void`. Colors from `--ok`, `--accent`, `--danger`, `--text-dim`.

**`formfield`**
- Paperwork-style input: label above, ruled underline, a small field code on the left, mono entered text.
- States: idle, focus (thick underline plus code highlight), error (red stamp-style marker), disabled.

## 7. Supergraphic mode

When `--supergraphic: on`:
- Oversized geometric shapes (stepped blocks, large arcs, bold stripes) sit behind content at 10 to 30% opacity or as flat blocks in `--accent` and `--accent-2`.
- Large uppercase geometric-sans type may run across a panel edge, cropped.
- Content layers stay readable: **body text needs enough contrast over any supergraphic** (check this).

When `off`: all supergraphics are removed, spacing tightens, and the theme remains complete. Required for dense apps.

Supergraphics are original SVG presets (`stepped-blocks`, `stripe-pair`, `arc-quarter`). Do not trace any set photo.

## 8. Screen and motion rules

**`--crt-level`:**

| Level | Effect |
|---|---|
| `off` | Flat monochrome pixel/mono text, no overlays |
| `light` | Faint scanlines (`--scanline-opacity` low), slight glow on ink |
| `full` | Scanlines, glow, subtle curvature (`--screen-curve`), slight vignette |

All effects use CSS gradients, `text-shadow`, `filter`, and SVG only. No bitmap images. A `prefers-reduced-motion` or low-power flag forces `off` for animated parts and caps glow layers.

**Motion (subtle, all disabled under reduced-motion):**
- Screen boot-in: a brief fade or line-expand on first render
- Blinking cursor in `readout` and `formfield`
- A gentle flicker at `full` only, amplitude very low
- Button press: 2px translate, 80ms
- Tab and state changes: 120ms ease
- No pulsing glows, no scrolling tickers, no looping decoration

## 9. Contract additions needed

| Addition | Detail |
|---|---|
| Tokens | `--supergraphic`, `--supergraphic-shape`, `--crt-level`, `--scanline-opacity`, `--phosphor-glow`, `--screen-curve`, `--tint-tungsten`, `--radius-screen`, `--font-screen` |
| Parts | `screen`, `timelinechart`, `deptheader`, `stamp`, `formfield` |
| Ornament presets | `stepped-blocks`, `stripe-pair`, `arc-quarter` |
| Checks | Supergraphic contrast check, screen-palette check (only the three screen tokens appear inside `screen`) |

Reuse before adding: `screen` and `readout` should reuse the screen and readout logic from the other CRT and LCD themes where possible. Report any contract change before continuing, as in the main brief.

## 10. Rules for the agent

1. **Original everything.** Original emblem, organization name, department names, mascot-free. No show logo, no mascot, no characters, no title lettering, no poster art, no recognizable set graphics.
2. **No show-specific terms** in sample text. Use neutral stand-ins such as "Department of Records," "Case file 0417," "Status: Pending."
3. **Do not claim a font is the real one.** Describe the type as "geometric sans in the style of mid-century signage."
4. **Palette discipline.** Warm office palette only. No green, no purple, no blues, and nothing added for "variety."
5. **No gloss, no glass, no bevels, no soft shadows** on chrome. The hard offset shadow is the depth model.
6. **Screens use only the three screen tokens.**
7. **Hardware is blocky and screens are rounded**, never the reverse.
8. **Ignore photos and set details** in screenshots that are not UI (actors, props, backgrounds).
9. **Calibrate colors from the attached screenshots**, then report the final hex values and any that differ materially from section 4.

## 11. Acceptance checklist

- [ ] All required tokens plus the section 4 additions defined
- [ ] All parts and all six states styled, including `screen`, `timelinechart`, `deptheader`, `stamp`, `formfield`
- [ ] Passes Test Page A and Test Page B, plus a TVA test card (`deptheader` + `screen` with `timelinechart` + `formfield` + `stamp` + `datagrid`)
- [ ] `--supergraphic` on and off both look complete, with readable text in both
- [ ] `--crt-level` off, light, and full all work, and reduced-motion forces `off`
- [ ] Screen contains only the three screen tokens
- [ ] No forbidden constructs (validator clean)
- [ ] No show marks, characters, or lettering anywhere
- [ ] Looks like only itself, with no traits from the coral HUD, neon grid, or any CRT/LCD theme

**Difficulty:** medium-high. The usual failures: adding gloss, softening the shadows, leaving a green tint on the screens, making the supergraphic too busy to read over, and over-applying scanlines.

## 12. Open items

- Calibrate all `(provisional)` hex values from my screenshots
- Confirm the supergraphic shape presets against the screenshots, since they are originals inspired by the genre
- If a second palette is wanted later (screen-only green or amber), it is a palette addition and requires no structural change

## Sources (research)

- The Art Newspaper, production designer interview: https://www.theartnewspaper.com/2021/07/10/lokis-production-designer-on-the-modernist-inspiration-behind-the-shows-stunning-visuals
- IndieWire summary of the "Mad Men meets Blade Runner" brief and Brazil reference: https://s.media-imdb.com/news/ni63368858/
- Yahoo Entertainment, signage and palette breakdown: https://www.yahoo.com/entertainment/look-loki-influenced-mad-men-185834234.html
- Yahoo Entertainment, brown/red/gold palette and carpet patterns: https://www.yahoo.com/entertainment/loki-brazil-blade-runner-influenced-213023224.html
- Collider, production design interview (supergraphics, built monitors): https://collider.com/loki-production-design-cat-kasra-farahani-interview/
- What to Watch, aesthetic breakdown (orange plastic, era palette): https://whattowatch.com/features/loki-breaking-down-the-aesthetic-of-the-tva
- Retro hardware interview coverage (CRT colors, 8-bit handheld look): https://techyes.pages.dev/2021/7/13/22574400/loki-retro-hardware-tempad-kasra-farahani-interview-marvel-disney-plus
- Cantina Creative, screen graphics studio: https://cantinacreative.com/series/loki and https://digitalmediaworld.tv/in-depth/395-rodeo-fx-takes-lucy-on-a-collision-course
- Before & Afters, screen graphics process (60s/80s mix): https://beforesandafters.com/2021/08/10/designing-the-sacred-timeline-in-loki/
- Typeface discussion (unverified, low confidence): https://madegooddesigns.com/?p=10831
- Low-confidence palette claim, not used: https://discourse.weareopen.coop/news/lokis-tva-unpacking-its-unique
