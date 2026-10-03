# 🗄️ CURIO — Database Features Implementation Plan

> **Status:** Drafted & Queued for Development  
> **Architecture:** 100% Offline-First • Zero Dependency • Standalone HTML5 (`app.html`)  
> **Source Inspirations:** AlternativeTo, Google Play Store, Raycast, and Are.na

---

## 📑 Overview & Build Roadmap

This document outlines the finalized 8-stage roadmap for expanding CURIO's database, curation, and workbench capabilities. Each stage is designed to be built, tested, and committed independently.

| Stage | Feature Area | Primary Inspiration | Complexity | Estimated Build |
|:---:|:---|:---|:---:|:---:|
| **1** | **Bidirectional Alternatives & Cross-References** | AlternativeTo | Medium | ~5 mins |
| **2** | **Structured Pros & Cons + 1-Click Code Snippets** | Raycast / DevDocs | Low-Med | ~4 mins |
| **3** | **Multi-Select & Floating Batch Operations Bar** | Desktop File Managers | Medium | ~6 mins |
| **4** | **Saved Filter Presets (Smart Views)** | Notion / Airtable | Low-Med | ~4 mins |
| **5** | **Trash Bin & Soft-Delete Safety Net** | macOS / Windows Recycle Bin | Low | ~4 mins |
| **6** | **"Similar Items" Recommendation Engine** | Google Play Store | Medium | ~4 mins |
| **7** | **CSV Spreadsheet Import with Column Mapper** | Modern Data Tables | High | ~6 mins |
| **8** | **Sortable List Columns & Multi-Drawer Filing** | Are.na / Spreadsheets | Low-Med | ~4 mins |

---

## 🛠️ Stage-by-Stage Specifications

### Stage 1: Bidirectional Alternatives & Cross-References
* **Inspiration:** *AlternativeTo*
* **What it does:**
  * Allows any item card (e.g., *Photoshop*) to link to other items as designated alternatives or related companions (e.g., *Affinity Photo, Krita, Photopea*).
  * Bidirectional: Linking Item A ➔ Item B automatically reflects on Item B ➔ Item A.
  * Includes an optional relationship qualifier: `Alternative To`, `Related Companion`, `Predecessor / Successor`.
* **Data Model:**
  * `item.relations = [{ id: "target-item-id", type: "alternative" | "related" | "successor" }]`
* **UI Representation:**
  * **Edit Modal:** Searchable typeahead dropdown to pick and attach related items.
  * **Card & Quick-Look:** Dedicated clickable chip sub-rail:
    ```
    ⇄ Alternatives: [Krita] [Photopea] [Affinity Photo]
    ```
  * Clicking an alternative chip instantly jumps and focuses that card.

---

### Stage 2: Structured Pros & Cons Matrix + 1-Click Code Snippets
* **Inspiration:** *Raycast & DevDocs*
* **What it does:**
  * **Pros & Cons:** Adds dedicated structured bullet lists for rapid evaluation of tools and assets:
    * 🟢 **Pros:** Fast, lightweight, zero telemetry, open-source.
    * 🔴 **Cons:** Steep learning curve, limited plugin ecosystem.
  * **Code / Command Snippet Box:** A dedicated monospace snippet slot on cards (e.g. `npm install ...`, `git clone ...`, `#include <shader.h>`).
    * Includes an instant 1-click **Copy Snippet** button right on the card face.
* **Data Model:**
  * `item.pros = string[]`
  * `item.cons = string[]`
  * `item.snippet = string`
* **UI Representation:**
  * Rendered cleanly inside the Quick-Look modal and Detailed View.
  * Snippet box displayed as a high-contrast terminal badge with copy confirmation toast.

---

### Stage 3: Multi-Select & Floating Batch Operations Bar
* **Inspiration:** *Professional Desktop Data Managers*
* **What it does:**
  * Enables selection checkboxes on all cards across all 5 view modes (Grid, Detailed, List, Kanban, Grouped).
  * Supports `Shift + Click` range selection and <kbd>Ctrl+A</kbd> select-all.
  * When 1 or more items are selected, a floating glassmorphic action bar slides up from the bottom of the screen.
* **Batch Actions:**
  * 📂 **Batch Move:** Reassign all selected items to a different Drawer.
  * 🏷️ **Batch Tag:** Add or remove tags across all selected items simultaneously.
  * 📊 **Batch Status:** Change workflow status (`To Explore` ➔ `Curated`).
  * 📌 **Batch Pin:** Pin or unpin group to the top.
  * 🗑️ **Batch Delete:** Soft-delete all selected items to Trash with confirmation.
  * 📦 **Batch Export:** Download selected items as a standalone JSON catalog.

---

### Stage 4: Saved Filter Presets (Smart Views)
* **Inspiration:** *Notion & Airtable*
* **What it does:**
  * Lets users save complex filter and search combinations into named one-click presets.
  * Example presets: *"5-Star Shaders"*, *"Unreviewed Backlog"*, *"Free 2D Engines"*.
* **UI Representation:**
  * New **"💾 Save View"** button in the tag/filter bar.
  * Saved presets appear in a collapsible **"Smart Views"** section in the left sidebar under the Drawer list.
  * Includes a dynamic count pill showing current matching items.
  * One-click to apply; hover to rename or delete.
* **Data Model:**
  * Stored per-catalog in IndexedDB:
    `{ id, name, tags: [], status, minRating, mediaOnly, linksOnly, query, viewMode }`

---

### Stage 5: Trash Bin & Soft-Delete Safety Net
* **Inspiration:** *macOS Trash / Windows Recycle Bin*
* **What it does:**
  * Deleting an item moves it to a recoverable **Trash Drawer** instead of permanently erasing it.
  * Adds a `deletedAt` timestamp to the item.
  * Trashed items are automatically hidden from global search, drawers, and active counts.
* **UI Representation:**
  * Distinct system drawer at the bottom of the sidebar: `🗑️ Trash (3)`.
  * Trashed items view provides **Restore** and **Permanently Delete** buttons on each card.
  * **"Empty Trash"** master button in sidebar/header to purge all deleted records permanently.

---

### Stage 6: "Similar Items" Recommendation Engine
* **Inspiration:** *Google Play Store*
* **What it does:**
  * A 100% client-side similarity scoring engine that suggests related tools within the catalog.
* **Scoring Formula:**
  $$\text{Score}(A, B) = 3 \times |\text{Shared Tags}| + 2 \times [\text{Same Drawer}] + [|\text{Rating}_A - \text{Rating}_B| \le 1]$$
* **UI Representation:**
  * Rendered as a horizontal scrolling thumbnail carousel at the bottom of the **Spacebar Quick-Look modal** and **Detailed View**.
  * Shows thumbnail monogram, title, rating, and shared tags.
  * Clicking any recommendation instantly switches the Quick-Look modal to inspect that item.

---

### Stage 7: CSV Spreadsheet Import with Column Mapper
* **Inspiration:** *Airtable & Modern SaaS Importers*
* **What it does:**
  * Allows users to import arbitrary CSV or TSV spreadsheet files directly into CURIO.
  * Includes a visual step-by-step modal:
    1. **File Drop:** Auto-detects comma, semicolon, or tab delimiters.
    2. **Column Mapper:** Shows preview of first 5 rows with dropdowns to map columns:
       `CSV Column ➔ CURIO Field (Title, Drawer, Status, Tags, Rating, Notes, Link, Snippet)`.
    3. **Preview & Confirm:** Validates records, creates missing drawers automatically, and confirms batch import.
* **Zero Dependency:** Uses a lightweight regex-based RFC 4180 CSV parser embedded directly in `app.html`.

---

### Stage 8: Sortable List Columns & Multi-Drawer Item Filing
* **Inspiration:** *Are.na & Spreadsheets*
* **What it does:**
  * **Sortable Columns:** List View table headers (`Title`, `Drawer`, `Status`, `Rating`, `Tags`, `Date`) become interactive. Click to sort ascending (▲), click again for descending (▼).
  * **Multi-Drawer Filing:** Allows a single item to belong to multiple Drawers simultaneously (e.g. *Blender* lives in both `3D Modeling` and `Video Editing`) without duplicating the record in IndexedDB.
* **Data Model:**
  * `item.drawers = ["3D Modeling", "Video Editing"]` (with backward compatibility fallback for `item.drawer`).

---

## 🔒 Verification & Architecture Checklist
* [x] **Zero External Runtime Dependencies:** Everything implemented in pure vanilla JS and CSS.
* [x] **IndexedDB Persistence:** All new schema fields (`relations`, `pros`, `cons`, `snippet`, `smartViews`) persist across page reloads.
* [x] **Export / Import Integrity:** JSON and ZIP backup extractors updated to serialize and restore all new fields without loss.
* [x] **Single-File Portability:** All features bundled directly inside `app.html`.
