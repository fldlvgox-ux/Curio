Pluggable UI themes · working reference

# Theme System Atlas

Every reference you collected, matched to its theme, plus the shared contract, build order, the TVA appendix and the Terminal/TUI plan. Open a card for the full breakdown.

[Themes](#themes)[Contract](#contract)[Build plan](#plan)[TVA](#tva)[Terminal / TUI](#tui)[Next categories](#next)[Briefs & handoff](#handoff)

## The 19 themes

Each reference is its own theme and is never blended with another. Themes share only the contract: parts, tokens and six channels. Colors on the dots mark the family.

Search themes

## The contract

What every theme must provide so any app can load it. Apps reference part names only, never a theme.

### Ground rules

- **One reference, one theme.** Never blend. A deliberate hybrid is a new theme.
- **Surface vs content.** User media (photos, art, thumbnails) is never recolored. The surface it sits on is part of the theme.
- **Original icons and stand-in text.** No logos, mascots, brand art or copyrighted wallpapers.
- **Procedural only.** CSS, SVG and JSON. No bitmaps, no JS, no network.
- **Screenshots calibrate** any provisional value. If one disagrees with a brief, the screenshot wins and the agent reports the change.
- **Instructions only.** No mockup step; the agent builds directly.

### Six channels

| Tokens | Color, type, spacing, density, radii. CSS variables. |
| --- | --- |
| Parts | Styling per \[data-part\] component. |
| Shape | Chamfers, radii, silhouettes via clip-path and masks. |
| Material | Bevel, gloss, grain, shadow, gradient, glow. |
| Ornament | Brackets, stitching, ticks, stickers. Sanitized SVG. |
| Icons | SVG symbol sprite, swappable per theme. |

### Required tokens

Color

--bg --surface --surface-2 --text --text-dim --accent --accent-text --border --select-bg --select-fg --danger --ok --warn

Type

--font-ui --font-display --font-mono --font-size-base --font-smoothing

Space and density

--space-1..5 --row-height --control-height --pixel-scale

Shape

--radius-window --radius-control --radius-chip --avatar-shape --cut-tl --cut-tr --cut-br --cut-bl

Material

--bevel-light --bevel-dark --bevel-width --shadow-raised --shadow-pressed --shadow-hard --gradient-title --gradient-button --grain --dither-pattern

Focus and state

--focus-ring --default-button-ringUnused tokens are set to a harmless value (none, 0), never omitted.

### Parts and states

Containers

window titlebar menubar toolbar panel header banner tabstrip tab statusbar group sidebar

Actions

button (primary, secondary, icon, transport, split) toggle switch chip

Inputs

slider (H/V: track, fill, thumb, ticks) checkbox radio textfield dropdown

Display

readout list listrow propertyrow statblock badge progress segmentmap visualizer avatar datagrid tree scrollbar

Overlays and optional

dialog alert note · taskbar taskbar-item (shell-like apps only)

States

idle hover pressed disabled focus selectedDriven by data-state, :hover, :active, :focus-visible.

### Theme package

One JSON file: contract version, id, family, layers, palettes, tokens, css, icons, ornaments.

- Palettes change color tokens only, never structure (Winamp color themes are the model).
- The loader scopes all theme CSS under \[data-theme="id"\] and rejects anything that escapes.
- On any failure it falls back to the default theme.

### Security for remote themes

- **Allowed:** CSS, SVG, JSON, system fonts, data: URIs.
- **Forbidden:** JavaScript, @import, url() to anything but data:, iframe, object, foreignObject, external fonts, network requests, CSS targeting outside its scope.
- A sandboxed plugin layer for structural themes is deferred.

### What each theme added to the contract

Built from the theme cards. Reuse before adding, and report any contract change before continuing.

## Build plan

Phase 0 builds the foundation. Round one tests the five biggest mechanisms. Later rounds must pass without changing the contract; if one forces a change, stop, say why, and re-verify the earlier themes.

PHASE 0

### Foundation

Contract spec, manifest JSON schema, loader and validator, neutral default theme, and two acceptance pages.

#### Test page A (generic)

Window with titlebar and menubar, alert, dialog, primary, secondary, icon and split buttons, toggle and switch, checkbox and radio, textfield, H and V sliders, readout, progress, three chips, three-row icon list, tab strip, avatar.

#### Test page B (data)

Tree sidebar, datagrid (header, normal, alternate, selected, status-colored text), two-level tabs, icon toolbar, segmentmap, three-segment statusbar, scrollbar.

### Per-theme checklist

- All required tokens defined
- All parts and all six states styled
- Passes test pages A and B with no theme-specific app code
- No forbidden constructs (validator clean)
- Signature detail present
- Looks like only its own reference, with no traits from other themes

## TVA theme · retro-futurist bureaucracy

Theme #16. Heavy blocky frames and flat signage around rounded, glowing monochrome screens. Friendly on the surface, a little oppressive underneath. Private use, but every name and emblem is still an original stand-in.

Awaiting your screenshots · hex values are provisional

### Decisions from the Q&A

| Accuracy source | Your screenshots plus written research |
| --- | --- |
| Surfaces | CRT/monitor screens, architecture and signage |
| Realism | Hybrid: flat graphic frames, skeuomorphic screens |
| Palette | One: Warm office |
| Supergraphics | Switchable --supergraphic: on \| off |
| CRT effects | Switchable --crt-level: off \| light \| full |
| Shape | Blocky frames, rounded screens |
| Type | Geometric sans plus mono for screens |
| Motion | Subtle, off under reduced-motion |
| Naming | Original stand-ins only |

### Warm office palette provisional

**--bg**#2A1D14

**--surface**#EDE0C4

**--surface-2**#D9C7A0

**--accent**#D9822B

**--accent-2**#E0A82E

**--danger**#9A3B26

**--ok**#7C8A3A

#### Screen: three tokens only

**--screen-bg**#16100A

**--screen-ink**#FFA63D

**--screen-ink-dim**#8A5320

No green, no purple, no blue. Selected and inverted states swap screen background and ink.

### New parts

- **timelinechart**: branching timeline on a screen, one ink, pruned branches dashed, current-position marker. Works as any history or flow chart.
- **deptheader**: department code, uppercase title, optional supergraphic block. Variants: block, stripe, poster.
- **stamp**: rubber-stamp status label, rotated 2 to 4 degrees. Approved, pending, denied, void.
- **formfield**: ruled underline, field code, mono entry. Idle, focus, error, disabled.
- **screen**: rounded recessed display in a heavy bezel.

### Signature details

- Heavy stepped or blocky flat frame
- Oversized geometric supergraphic behind content when on
- Rounded monochrome screen, scanlines and glow scaled by --crt-level
- Uppercase geometric-sans signage with a department code
- A stamped status label

### Never

- Gloss, glass, bevels, soft shadows on chrome. The hard offset shadow is the depth model.
- The show's emblem, mascot, characters, title lettering or poster art
- Calling any font "the" original; say "geometric sans in the style of mid-century signage"

### Research confidence

| Claim | Confidence | Used for |
| --- | --- | --- |
| "Mad Men meets Blade Runner" brief | High | Overall mood |
| Brutalist forms against mid-century surfaces and patterns | High | Shape and material split |
| Warm brown, red, gold; orange plastic | High / medium | Palette |
| Roadside-station style signage, oversized supergraphics | High | Signage, supergraphic mode |
| CRT playback mostly green with amber variants, 8-bit monochrome handheld look | High | Screen layer |
| Monitors were built props with rounded housings | High | Screen housing shape |
| Grey and sickly-green overall palette | Low (conflicts with the designer) | Not used |
| Exact typeface | Unverified | Described in style only |

**Open items.** Calibrate every provisional hex from your screenshots. Confirm the three supergraphic presets (stepped-blocks, stripe-pair, arc-quarter) against them. A second palette, such as a green or amber screen, would be a palette addition with no structural change. Full text is in the TVA brief below.

## Terminal / TUI · collecting references

The first theme that may constrain layout, not just skin it: a character grid, borders drawn as characters, spacing in whole cells. Click any term to copy it, then search for screenshots.

Next step: you send 3 to 5 screenshots that disagree with each other

### What to capture

- A menu bar or tab strip
- A bordered panel or dialog, noting the border style: single, double or rounded
- A table or list with a selected row
- A form field, checkbox or button
- A progress bar or gauge
- A status bar with key hints such as F1 Help F10 Quit
- A scrollbar

Aim for contrast: one classic blue DOS screen, one modern dashboard, one monochrome phosphor screen. Note anything that depends on the grid.

### Questions I'll ask once screenshots arrive

- Where does "a theme only skins" end and "a theme constrains layout" begin?
- Borders as real box-drawing characters, or CSS borders aligned to a cell grid?
- Is monospace mandatory for the whole UI, or only inside panels?
- Do controls need visible keyboard hints and focus by key?
- Palette as the 16 ANSI slots, or a free token set?
- Does the theme share Test pages A and B, or get a grid-based variant?

You asked me to ignore the amber radar screenshot earlier in the chat, so it isn't used here. The amber and green phosphor looks are still listed as a sub-style in case you want them.

## Categories not yet explored

Grouped by what each would test in the contract. The first three change the contract more than another style would; if they pass without edits, the system is solid.

| Gap | Examples | What it tests |
| --- | --- | --- |

### Axes, not styles

- **High contrast / accessibility.** Large type, strong contrast, color-blind-safe palettes. The best test of the contract with decoration removed.
- **Script coverage.** Pixel, geometric and mono fonts have no glyphs for non-Latin scripts. Add a --font-fallback stack and forbid hiding text when a glyph is missing.
- **Light and dark.** Each theme states whether it has both or is inherently one.
- **Print and e-ink.** A monochrome, no-animation fallback every theme can degrade to.

### Suggested order

1. **Modern baseline**: default and control group
2. **Terminal / TUI**: first to force layout rules in progress
3. **High-contrast accessibility**: strictest test
4. **Soft / clay**: the shadow and radius range
5. **Editorial / Swiss**: almost no ornament
6. **LCARS-style panels**: hardest shape layer

## Briefs and handoff

Copy these straight into an agent or a new chat. The main brief covers themes 1 to 10 and the contract; themes 11 to 19 and their contract additions live in the cards above, and consolidating them into one brief is still open.

### Handoff prompt for a new chat

Attach the two briefs and any reference images you want refined.

### theme-system-brief.md

Contract, loader and security rules, test pages, ten theme briefs, theme-maker prompt spec.

Show full text

```

```

### tva-theme-brief.md

Theme #16 appendix: research basis, decisions, tokens, parts, rules, checklist, sources.

Show full text

```

```