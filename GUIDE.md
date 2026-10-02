# 📖 CURIO — Complete User Guide & Manual

**CURIO** is a high-capacity, offline-first visual catalog, asset organizer, and curation workbench designed for game developers, artists, writers, and researchers.

---

## 📑 Table of Contents
1. [Core Philosophy & Architecture](#1-core-philosophy--architecture)
2. [Interface Overview](#2-interface-overview)
3. [Managing Catalogs & Drawers](#3-managing-catalogs--drawers)
4. [Creating & Editing Items](#4-creating--editing-items)
5. [The 5 Dynamic Views](#5-the-5-dynamic-views)
6. [Filtering, Sorting & Spotlight Search](#6-filtering-sorting--spotlight-search)
7. [Automated Discord Curation & AI Tagging](#7-automated-discord-curation--ai-tagging)
8. [Syncing Mobile & Desktop](#8-syncing-mobile--desktop)
9. [Offline Storage, Backups & Restores](#9-offline-storage-backups--restores)
10. [Keyboard Shortcuts](#10-keyboard-shortcuts)

---

## 1. Core Philosophy & Architecture
* **Offline-First**: All your data lives inside your device's browser **IndexedDB** engine. You do not need an active internet connection to browse, search, or edit.
* **Zero Lock-In**: Everything is exportable into standard JSON and full `.zip` archives containing your images.
* **High Capacity**: Capable of storing thousands of assets, cheat sheets, and images without bogging down.

---

## 2. Interface Overview
* **Left Sidebar**: 
  * **Catalog Selector**: Switch between libraries or create new ones.
  * **Drawers List**: Categorized shelves with live item counters.
  * **Sync & Backup Tools**: One-click **Sync Inbox**, **Export (.zip / .json)**, and **Import**.
* **Top Bar**:
  * **Search Bar**: Instant real-time filtering across titles, notes, and tags.
  * **View Switcher**: Toggle between Grid, Detailed, List, Kanban, and Grouped.
  * **🧭 Realms**: Browse discovery collections.
  * **📖 Guide**: Opens interactive in-app tutorial.
  * **⚙️ Settings**: Color themes (Cyber Cyan, Synthwave, Matrix, Amber, Paper), database metrics, and statistics.
  * **＋ New Item**: Manual card creation.

---

## 3. Managing Catalogs & Drawers
* **Switch Catalogs**: Use the dropdown at the top of the sidebar. Curio comes pre-loaded with encyclopedias covering Game Design, Creative Tools, OS Lineages, Mythologies, and more.
* **Create a Catalog**: Click the **＋** icon next to the catalog dropdown.
* **Drawers (Categories)**:
  * Click **"＋ New Drawer"** at the bottom of the drawer list to add a category.
  * Right-click or use the settings icon next to a drawer to rename or delete it.

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
* **Link**: External URL to website, GitHub repo, or tutorial.
* **Images**:
  * **Logo / Thumbnail**: Upload an icon or image banner.
  * **Gallery**: Upload multiple screenshots or diagrams stored locally in IndexedDB.

---

## 5. The 5 Dynamic Views
Switch between views from the top header:
1. **Grid View**: Visual card matrix displaying logos, badges, star ratings, and tags.
2. **Detailed View**: Two-column layout showcasing large screenshot carousels and full notes side-by-side.
3. **List View**: Dense spreadsheet table optimized for rapid scanning and comparing ratings/tags.
4. **Kanban View**: Drag-and-drop workflow board columns organized by status (`To Explore` ➔ `In Progress` ➔ `Curated` ➔ `Archived`).
5. **Grouped View**: Accordion layout grouped by Drawer, Status, Rating, or Alphabetical order.

---

## 6. Filtering, Sorting & Spotlight Search
* **Multi-Tag Filter**: Select one or multiple tags with an **AND / OR** matching toggle.
* **Rating Filter**: Filter by star thresholds (e.g. "4★ and up").
* **Media & Link Filters**: Show only cards with photos, or only cards with external links.
* **Spotlight Global Search (`Ctrl + K` or `Cmd + K`)**:
  * Press `Ctrl + K` anywhere.
  * Searches across **all catalogs simultaneously**.
  * Press `Enter` on any search result to jump straight to that catalog and illuminate the card.

---

## 7. Automated Discord Curation & AI Tagging
You can curate links directly from your phone, tablet, or PC without manual data entry:

1. **Send Link to Discord**:
   * Post any URL (GitHub, YouTube, ArtStation, Shadertoy, Tool site) in `#curio-inbox`.
2. **AI Processing**:
   * The companion bot extracts the title, preview image, and description.
   * **Gemini AI** classifies the link into the right **Drawer**, generates 3–5 clean tags, and writes a 2-sentence summary.
3. **Automatic Queue**:
   * The item is formatted into CURIO's schema and saved to `curio_inbox.json`.
   * It automatically commits and pushes the update to your GitHub repository.
4. **Discord Commands**:
   * Type `export` in `#curio-inbox`: Bot sends the `curio_inbox.json` file directly into Discord for mobile download.
   * Type `sync` in `#curio-inbox`: Manually triggers a push to GitHub.

---

## 8. Syncing Mobile & Desktop
* **Desktop (PC)**:
  * Click **Sync Inbox** in the sidebar.
  * CURIO pulls directly from the local bot on `localhost:8765` in milliseconds.
* **Mobile (Phone / Tablet)**:
  * Open CURIO on your phone browser or PWA.
  * Click **Sync Inbox** in the sidebar.
  * CURIO automatically fetches newly curated items from your GitHub repository.
* **Smart De-duplication**: CURIO checks existing IDs and URLs to ensure items are never duplicated.

---

## 9. Offline Storage, Backups & Restores
CURIO never traps your data in the cloud:
* **Export (.zip Archive)**: Downloads your complete database JSON along with actual image files extracted from IndexedDB.
* **Export (.json)**: Downloads a clean JSON file of your active catalog.
* **Import**: Click **Import** in the sidebar to load any `.json` or `.zip` backup into CURIO.
* **Zero-Internet Operation**: You can use CURIO completely offline on an airplane, laptop, or remote location.

---

## 10. Keyboard Shortcuts
| Shortcut | Action |
| :--- | :--- |
| **`Ctrl + K` / `Cmd + K`** | Open Spotlight Global Search (All Catalogs) |
| **`/`** | Focus Search Box |
| **`Esc`** | Close Modals / Clear Search |
| **`⭐` (on card)** | Pin card to top of drawer |
| **`📋` (on card)** | Copy formatted Markdown link to clipboard |

---

*CURIO — The Curator • 100% Offline-First • Designed for Creators*
