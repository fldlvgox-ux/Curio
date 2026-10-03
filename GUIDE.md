# 📖 CURIO — Complete User Guide & Manual

**CURIO** is a high-capacity, offline-first visual catalog, asset organizer, and curation workbench designed for game developers, artists, writers, researchers, and digital collectors.

---

## 📑 Table of Contents
1. [Core Philosophy & Architecture](#1-core-philosophy--architecture)
2. [Interface Overview](#2-interface-overview)
3. [Managing Catalogs & Drawers](#3-managing-catalogs--drawers)
4. [Creating & Editing Items](#4-creating--editing-items)
5. [The 5 Dynamic Views & Density Toggle](#5-the-5-dynamic-views--density-toggle)
6. [Spacebar Quick-Look Inspection](#6-spacebar-quick-look-inspection)
7. [Visual Themes & Nostalgic Interfaces](#7-visual-themes--nostalgic-interfaces)
8. [Filtering, Sorting & Spotlight Search](#8-filtering-sorting--spotlight-search)
9. [Automated Discord Curation & AI Tagging](#9-automated-discord-curation--ai-tagging)
10. [Syncing Mobile & Desktop](#10-syncing-mobile--desktop)
11. [Offline Storage, Backups & Restores](#11-offline-storage-backups--restores)
12. [Keyboard Shortcuts](#12-keyboard-shortcuts)

---

## 1. Core Philosophy & Architecture
* **100% Offline-First**: All your data lives inside your device's browser **IndexedDB (`CyberDB`)** engine. You never need an internet connection to browse, search, or curate.
* **Single-File Zero Dependency**: The complete application is bundled in a single standalone HTML file (`app.html`) with zero external runtime dependencies, npm packages, or server frameworks.
* **Zero Lock-In**: Everything is exportable into standard JSON and full `.zip` archives containing your images extracted into standard files.
* **Gigabyte Scale**: Capable of storing thousands of high-res assets, screenshots, and rich notes without memory bottlenecks or cloud throttling.

---

## 2. Interface Overview
* **Left Sidebar**: 
  * **Catalog Selector**: Switch between 15 pre-loaded encyclopedias or create your own custom catalogs.
  * **Drawers List**: Categorized shelves with live item counters and drawer management.
  * **Sync & Backup Tools**: One-click **Sync Inbox**, **Export (.zip / .json)**, and **Import**.
* **Top Bar**:
  * **Global Search Box**: Real-time multi-field search across titles, notes, links, and tags.
  * **View Switcher**: Seamlessly toggle between Grid, Detailed, List, Kanban, and Grouped layouts.
  * **View Density Switcher**: Toggle between **Comfortable** and **Compact** layout densities.
  * **🧭 Realms**: Browse curated discovery collections across creative domains.
  * **📖 Guide**: Interactive in-app tutorial and reference hub.
  * **⚙️ Settings**: Appearance themes, live database storage metrics, shortcuts, and about info.
  * **＋ New Item**: Open the comprehensive card creation dialog.

---

## 3. Managing Catalogs & Drawers
* **Switch Catalogs**: Use the dropdown at the top of the sidebar. Curio comes pre-loaded with 15 encyclopedias covering Game Design, Creative Tools, OS Lineages, Mythologies, Biology, and more.
* **Create a Catalog**: Click the **＋** icon next to the catalog dropdown. Choose a blank slate or starter template.
* **Drawers (Categories)**:
  * Click **"＋ New Drawer"** at the bottom of the drawer list to add a category.
  * Hover over any drawer to access settings (rename or delete drawer).

---

## 4. Creating & Editing Items
Each item card supports rich metadata:
* **Title**: Name of the tool, asset, or document.
* **Drawer**: The assigned category.
* **Status**: 
  * `To Explore` (Backlog)
  * `In Progress` (Currently learning/testing)
  * `Curated` (Reviewed & finalized)
  * `Archived` (Preserved reference)
* **Tags**: Comma-separated labels (e.g. `shader, godot, 3d, open-source`).
* **Rating**: 1 to 5 stars.
* **Notes**: Markdown description, key features, syntax snippets, or research notes.
* **Link**: External URL to website, GitHub repo, or tutorial (with a quick-test launch button).
* **Images**:
  * **Logo / Thumbnail**: Upload an icon or monogram badge with instant client-side compression.
  * **Gallery**: Upload multiple screenshots or diagrams stored locally in IndexedDB with full Lightbox gallery support.

---

## 5. The 5 Dynamic Views & Density Toggle
Switch views on the fly from the top-right toolbar:
1. **Grid View**: Visual card matrix displaying logos, badges, star ratings, and tags.
2. **Detailed View**: Two-column layout showcasing large screenshot carousels and full notes side-by-side.
3. **List View**: Dense spreadsheet table optimized for rapid scanning and comparing ratings/tags.
4. **Kanban View**: Workflow pipeline columns organized by status (`To Explore` ➔ `In Progress` ➔ `Curated` ➔ `Archived`).
5. **Grouped View**: Accordion layout grouped by Drawer, Status, Rating, or Alphabetical order.

### View Density Switcher (Comfortable vs. Compact)
Click the **Density** button in the top bar to toggle:
* **Comfortable**: Generous breathing room, large media previews, and multi-line notes.
* **Compact**: Tightened grid columns, compact thumbnail heights, single-line notes clamp, and condensed table rows to maximize information density on screen.
* Persisted automatically to `localStorage` with zero-flicker bootstrap on page reload.

---

## 6. Spacebar Quick-Look Inspection
Inspired by macOS Finder and professional digital asset managers:
* **Instant Preview**: Tap <kbd>Space</kbd> on any focused card or **double-click** any card to pop open the floating Quick-Look modal.
* **Rich Inspection**: Inspect full-resolution imagery, direct link buttons, tags, star ratings, and full scrollable notes without entering edit mode.
* **Live Cycling**: Use <kbd>←</kbd> and <kbd>→</kbd> or <kbd>J</kbd> and <kbd>K</kbd> to cycle through cards in real-time while Quick-Look remains open.
* **Quick Actions**: Pin (<kbd>P</kbd>), Copy Markdown (<kbd>C</kbd>), Edit (<kbd>E</kbd>), or Dismiss (<kbd>Space</kbd> / <kbd>Esc</kbd>).

---

## 7. Visual Themes & Nostalgic Interfaces
CURIO features a modular theme engine with 16 handcrafted visual appearances:

### 🕰️ Heritage & Nostalgic Systems
* **🪟 Windows 95 ("Chicago Classic")**: 3D beveled inset/outset chrome, `#008080` teal desktop wallpaper, navy titlebars on cards (`#000080` ➔ `#1084d0`), indented inputs, and sunken status panels.
* **📟 Phosphor CRT Terminal**: Deep cathode black (`#060503`), repeating scanline raster overlay, luminous amber phosphor glow, strict monospace typography, and ASCII wireframes.
* **🍎 Mac OS System 7 / Platinum**: Classic Apple platinum stipple desktop, 6-line speed pinstripes on card headers, 1-bit solid black outlines with hard drop shadows, and inverted capsule buttons.
* **🗃️ Library Card Catalog**: Manila index cardstock (`#fdfbf7`), terracotta top margin cloth rule (`#8c4322`), typewriter typography, mahogany cabinet sidebar (`#2b1f17`), brass pulls (`#c89658`), and rubber-stamp status tags.
* **💧 Frutiger Aero / Aqua Glass**: Vibrant aquatic sky gradients, high-translucency frosted acrylic cards (`backdrop-filter: blur(16px)`), specular gloss reflections, liquid jelly capsule buttons, and liquid tube storage meter.
* **📱 Palm OS / Early PDA**: 4-shade grayscale handheld LCD aesthetic, 1px solid borders, inverted black header bars, hardware-style buttons, and dotted memo dividers.
* **🟠 Amiga Workbench 3.1**: The iconic 1992 Commodore 4-color palette (`#0055aa`, `#ffffff`, `#ff8800`, `#000000`), orange-and-white checkered titlebars, beveled depth gadgets, and Topaz bitmap typography.
* **🪟 Windows XP ("Luna Blue")**: Royal blue gradient titlebars, silver body chrome (`#ece9d8`), olive-green Start buttons, Task Pane navigation, and Bliss sky horizon backdrops.
* **📌 Polaroid / Corkboard**: Tactile bulletin pinboard canvas, white Polaroid photo frames with slight organic tilt, 3D red pushpins, scotch tape details, and handwritten cursive typography.
* **🌺 Vaporwave / A E S T H E T I C**: Dreamy pastel retrowave wash (hot pink → lavender → teal), perspective neon grid floor, frosted glass cards, VHS tracking glitch on hover, and fullwidth katakana-style text.
* **📐 Blueprint / Technical Drawing**: Prussian blue drafting paper (`#0b2545`), white/cyan 100px major and 20px minor architectural CAD grid lines, crisp wireframe schematics with corner crosshairs (`+`), and monospace drafting typography.
* **🤖 Iron Man Jarvis / Holographic HUD**: Stark Industries holographic heads-up display with arc-reactor concentric cyan radial glow (`#00f0ff`), deep telemetry scanline canvas, glowing HUD glass cards with corner status diagnostics (`SYS.OK`), and Stark gold power accents (`#ffd000`).

### 🎨 Dark Studio Palettes
* **Cyber Cyan (Default)**: High-contrast dark cyberpunk palette with radiant cyan neon accents.
* **Synthwave Sunset**: Deep violet and hot neon pink sunset aesthetic.
* **Nord Frost**: Arctic blue and cool slate tones for serene, distraction-free curation.
* **Matrix Terminal**: Phosphor green monochrome hacker interface.

*Switch themes instantly via **Settings ➔ Themes** or through the <kbd>Ctrl+K</kbd> command palette.*

---

## 8. Filtering, Sorting & Spotlight Search
* **Multi-Tag Filter**: Select one or multiple tags with an **AND / OR** matching toggle.
* **Modernized Reset Filters Pill**: Always accessible in the tag bar, displaying a dynamic badge with the exact number of active filters. Click to clear all filters in one click.
* **Rating Filter**: Filter by star thresholds (e.g. "4★ and up").
* **Media & Link Filters**: Filter to show only items with photos, or only items with external links.
* **Spotlight Global Search (<kbd>Ctrl+K</kbd> or <kbd>Cmd+K</kbd>)**:
  * Press <kbd>Ctrl+K</kbd> from anywhere in the app.
  * Searches across **all 15 catalogs simultaneously** and supports direct theme switching.
  * Press <kbd>Enter</kbd> on any search result to jump straight to that catalog and illuminate the card with a glowing pulse.

---

## 9. Automated Discord Curation & AI Tagging
Curate links directly from your smartphone, tablet, or secondary PC:
1. **Send Link to Discord**: Post any URL (GitHub, YouTube, ArtStation, Shadertoy, Tool site) in your private `#curio-inbox` channel.
2. **AI Processing**: The companion bot extracts the title, preview image, and description. **Gemini AI** classifies the link into the right **Drawer**, generates 3–5 clean tags, and writes a 2-sentence summary.
3. **Automatic Queue**: The item is formatted into CURIO's schema, committed, and pushed to your GitHub repository.
4. **Discord Commands**:
   * `export`: Bot sends the `curio_inbox.json` file directly into Discord for mobile download.
   * `sync`: Manually triggers a push to GitHub.

---

## 10. Syncing Mobile & Desktop
* **Desktop (PC)**:
  * Click **Sync Inbox** in the sidebar.
  * CURIO pulls directly from the local bot on `localhost:8765` in milliseconds.
* **Mobile (Phone / Tablet)**:
  * Open CURIO on your phone browser or PWA.
  * Click **Sync Inbox** in the sidebar.
  * CURIO automatically fetches newly curated items from your GitHub repository.
* **Smart De-duplication**: CURIO checks existing IDs and URLs to ensure items are never duplicated.

---

## 11. Offline Storage, Backups & Restores
* **Export (.zip Archive)**: Downloads your complete database JSON along with actual image files extracted from IndexedDB.
* **Export (.json)**: Downloads a clean JSON file of your active catalog.
* **Import**: Click **Import** in the sidebar to load any `.json` or `.zip` backup into CURIO.
* **Zero-Internet Operation**: Complete offline autonomy on airplanes, laptops, or field research locations.

---

## 12. Keyboard Shortcuts

| Shortcut | Action | Scope |
| :--- | :--- | :--- |
| <kbd>↑</kbd> <kbd>↓</kbd> <kbd>←</kbd> <kbd>→</kbd> or <kbd>J</kbd> / <kbd>K</kbd> | Navigate and highlight items with glowing focus ring | Catalog Views |
| <kbd>Space</kbd> | Open / Close Quick-Look preview modal | Catalog Views |
| <kbd>E</kbd> | Edit the currently focused item | Catalog Views & Quick-Look |
| <kbd>L</kbd> | Open external link of focused item in new tab | Catalog Views & Quick-Look |
| <kbd>P</kbd> or <kbd>*</kbd> | Toggle pin to top on focused item | Catalog Views & Quick-Look |
| <kbd>C</kbd> | Copy formatted Markdown link to clipboard | Catalog Views & Quick-Look |
| <kbd>Home</kbd> / <kbd>End</kbd> | Jump to first / last item in active view | Catalog Views |
| <kbd>Ctrl+K</kbd> / <kbd>Cmd+K</kbd> | Open Spotlight Search & Theme Switcher | Global |
| <kbd>/</kbd> | Focus global search box | Global |
| <kbd>N</kbd> or <kbd>Ctrl+N</kbd> | Open New Item curation modal | Global |
| <kbd>Escape</kbd> | Close active dialog, Quick-Look, or Lightbox | Global |
| <kbd>◀</kbd> / <kbd>▶</kbd> | Navigate Lightbox gallery images or Quick-Look cards | Lightbox & Quick-Look |

---

*CURIO — The Curator • 100% Offline-First • Designed for Creators*
