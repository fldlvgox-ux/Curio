# 📋 CURIO — Master TODO & Roadmap

> **Last Updated:** 2026-10-03  
> **Current Version:** 3.2.0  
> **Total Themes:** 16 ✅ | **Total Catalogs:** 15 | **Total Items:** 1,366+

---

## ✅ Completed

### Themes (Stages 1–14) — ALL COMPLETE
- [x] ⚡ Cyberpunk Obsidian (Default)
- [x] 🪟 Windows 95
- [x] 📟 Phosphor CRT Terminal
- [x] 🍎 Mac OS Classic (System 7)
- [x] 🗃️ Library Card Catalog
- [x] 💧 Frutiger Aero
- [x] 📱 Palm OS / PDA
- [x] 🟠 Amiga Workbench 3.1
- [x] 🪟 Windows XP Luna
- [x] 📌 Polaroid / Corkboard
- [x] 🌺 Vaporwave / A E S T H E T I C
- [x] 📐 Blueprint / Technical Drawing
- [x] 🤖 Iron Man Jarvis / Holographic HUD
- [x] 🌅 Synthwave Sunset (palette)
- [x] ❄️ Nord Frost (palette)
- [x] 🟢 Matrix Terminal (palette)
- [x] 🌌 Midnight Gold (palette)

### Core Features — COMPLETE
- [x] Multi-catalog system (15 encyclopedias)
- [x] 6 view modes (Grid, Detailed, List, Kanban, Grouped + density toggle)
- [x] Spotlight Command Palette (Ctrl+K) with cross-catalog search
- [x] Keyboard navigation (J/K/arrows, Space quick-look, E edit, etc.)
- [x] Pinning, tagging, status management
- [x] IndexedDB offline storage with ZIP/JSON export/import
- [x] Discord bot integration + Sync Inbox
- [x] PWA install support & standalone Android APK project
- [x] Mobile bottom navigation bar & bottom-sheet modals
- [x] Tactile haptic feedback on touch & theme synchronization
- [x] Remote CDN master catalog auto-seed on empty first launch
- [x] Image galleries with lightbox
- [x] Filter bar with tag cloud, rating, status, media filters
- [x] Monogram avatars for items without images

---

## 🔲 Universal Cloud Sync (Phone ↔ PC Multi-Device Sync)

> **Goal:** Seamlessly sync catalogs, items, and edits between Android Phone and PC without running heavy servers.  
> **Status:** Tasked / Backlogged for implementation  
> **Priority:** High

| # | Sub-task | Details | Status |
|---|----------|---------|:------:|
| 1 | **Cloud Sync Provider Architecture** | Support private GitHub Gist (free, zero-server) or Cloudflare KV Sync Key | 🔲 |
| 2 | **Settings UI "Cloud Sync" Panel** | Dedicated tab in Settings modal to enter Gist ID / Access Token or Sync Code | 🔲 |
| 3 | **Two-Way Pull & Push Engine** | Auto-push on item add/edit; auto-pull latest changes on app start with diff merge | 🔲 |
| 4 | **Manual "Sync Now" Trigger** | Instant 1-tap sync button in header and mobile bottom nav with status indicators | 🔲 |
| 5 | **Conflict Resolution Strategy** | Last-write-wins per item using `item.updatedAt` timestamp to prevent data clobbering | 🔲 |

---

## 🎮 Easter Eggs & Nostalgic Interactions — LIVE ✅

> **Guide:** Documented inside the app (Settings ➔ **Guide & Tutorial** ➔ Section 11)  
> **Toggle:** Configurable in Settings ➔ **About** tab (persistent via `localStorage`)

| # | Easter Egg | Trigger / Command | Visual & Interaction | Status |
|---|---|---|---|:---:|
| 1 | **🎬 Star Wars 3D Cinematic Credits** | Click top-left **`CURIO`** brand logo **5× rapidly** | Full-screen 3D perspective dark overlay crawling item counts & credits | ✅ Live |
| 2 | **🌀 Do a Barrel Roll** | Type `do a barrel roll` in <kbd>Ctrl</kbd>+<kbd>K</kbd> Spotlight | Viewport executes a smooth 360° hardware-accelerated spin | ✅ Live |
| 3 | **🎉 Confetti Party** | Type `party` or `celebrate` in <kbd>Ctrl</kbd>+<kbd>K</kbd> Spotlight | Cascade of 45 colorful celebratory emojis with randomized spin physics | ✅ Live |
| 4 | **📟 Retro Terminal Greeting** | Type `hello world` in <kbd>Ctrl</kbd>+<kbd>K</kbd> Spotlight | Phosphor green CRT terminal output with glowing text & blinking block cursor | ✅ Live |
| 5 | **📎 Win95 Clippy Assistant** | 60s idle on **Windows 95** theme | Animated paperclip with speech bubble & 6 rotating snarky quips | ✅ Live |
| — | **⚙️ Master Easter Egg Switch** | Settings ➔ **About** tab | Slide toggle to turn all Easter eggs on/off instantly | ✅ Live |
| — | **📖 In-App Easter Egg Guide** | Settings ➔ **Guide & Tutorial** | Section 11 listing all triggers clearly for users | ✅ Live |

---

## 🧠 PKM Evolution: Bi-Directional Linking & Dynamic Custom Properties — SPECIFIED ✅

> **Source:** PKM Design Interview (`/grill-me`)  
> **Status:** Architecture fully specified & approved, ready for implementation  
> **Philosophy:** Lightweight, zero-bloat, 100% offline & backward-compatible with existing IndexedDB schema

### 1. 🔗 Bi-directional Linking (`[[Wikilinks]]` & Backlinks)
| Sub-Task | Details | Status |
|---|---|:---:|
| **Inline Autocomplete (`[[`)** | Typing `[[` inside Notes pops up an inline fuzzy-search dropdown to easily pick and insert item titles | 🔲 |
| **Pill Link Renderer** | Parses `[[Item Title]]` into styled, clickable accent pills inside Notes, Detailed View, and Quick-Look | 🔲 |
| **Instant Navigation** | Clicking any `[[link]]` immediately jumps to that item or opens its Quick-Look inspector | 🔲 |
| **Backlinks Section ("Referenced By")** | Detailed View & Quick-Look automatically show an incoming backlinks list of all items referencing the current one | 🔲 |

### 2. 🏷️ Dynamic Custom Properties (Hybrid Drawers + Items)
| Sub-Task | Details | Status |
|---|---|:---:|
| **Hybrid Structuring** | Drawers define default property schemas; individual items can also add custom one-off fields on the fly | 🔲 |
| **Rich Field Types** | 🔤 Text, 🔢 Number, 📋 Select Dropdown, 🔗 URL link, and ☑️ Checkbox (Boolean) | 🔲 |
| **Card & View Integration** | Properties render as sleek metadata badges in Detailed View and as dedicated columns in List View | 🔲 |
| **Search Indexing** | All custom property keys and values are automatically indexed in Spotlight (<kbd>Ctrl</kbd>+<kbd>K</kbd>) and quick filter (`/`) | 🔲 |
| **Lossless Export/Import** | JSON/ZIP backup & restore handles property templates and per-item property dictionaries seamlessly | 🔲 |

---

## 🐾 Quirky & Nostalgic Expansion: Cyber-Pet & Synthesized Retro Audio — SPECIFIED ✅

> **Source:** Design Brainstorm & Quirky Interview (`/grill-me`)  
> **Status:** Architecture fully specified & approved, ready for implementation  
> **Philosophy:** Zero external dependencies (native Web Audio API + CSS sprites), 100% offline, delightful & unobtrusive

### 1. 🐱 Theme-Morphing Cyber-Pet (Tamagotchi Curation Companion)
| Sub-Task | Details | Status |
|---|---|:---:|
| **Sidebar Footer Docking** | Sits comfortably in the sidebar footer above the storage meter; toggleable in Settings | 🔲 |
| **Theme-Morphing Sprites** | Adapts appearance to active theme (Cyber-cat, Win95 dog, Matrix rabbit, CRT robot, Frutiger penguin, Palm PDA) | 🔲 |
| **Feeding & XP Leveling** | New/curated items send a flying particle into the pet with chomp animation & XP leveling (Hatchling ➔ Archon) | 🔲 |
| **Idle & Poke Interactions** | Bounces when active, sleeps with `zZz` when idle (2m+); clicking pokes it for quips & stats | 🔲 |

### 2. 🔊 Synthesized Retro Audio Engine (Web Audio API)
| Sub-Task | Details | Status |
|---|---|:---:|
| **Zero-Asset Synth Core** | Native browser `AudioContext` frequency oscillator sweeps — 0 KB external MP3s, instant & offline | 🔲 |
| **Star Rating Arpeggios** | Ascending musical chimes as user hovers/clicks 1★ through 5★ | 🔲 |
| **Tactile Keyboard Thocks** | Satisfying mechanical switch click during keyboard navigation (<kbd>J</kbd>, <kbd>K</kbd>, <kbd>/</kbd>, <kbd>Space</kbd>) | 🔲 |
| **Dial-Up Modem Chirp** | Nostalgic 1.5s handshake chirps when clicking "Sync Inbox" | 🔲 |
| **Pet SFX & UI Ticks** | 8-bit chomp on feeding, level-up fanfare, and crisp drawer switch relay ticks | 🔲 |
| **Audio Controls** | Quick-mute toggle button (`🔊 / 🔇`) in header and next to pet; volume slider in Settings (default 20%) | 🔲 |

---

## 🔲 Upcoming — Database Features

> **Plan:** [`DATABASE_FEATURES_PLAN.md`](DATABASE_FEATURES_PLAN.md)  
> **Status:** Planned, not yet started  
> **Stages:** 9 commits (Stages 8–16)

### Phase 1: Core Relationships & Utility
| Stage | Feature | Complexity | Status |
|:-----:|---------|:----------:|:------:|
| 8 | Cross-References & Related Items (bidirectional linking) | Medium | 🔲 |
| 9 | Custom Fields Per Catalog (text, number, select, date, etc.) | High | 🔲 |
| 10 | Multi-Select & Batch Operations (move, tag, delete in bulk) | Medium | 🔲 |
| 11 | Saved Filter Presets / Smart Views (sidebar quick-views) | Low-Med | 🔲 |

### Phase 2: Safety & Discovery
| Stage | Feature | Complexity | Status |
|:-----:|---------|:----------:|:------:|
| 12 | Trash Bin / Soft Delete (recoverable 30-day trash) | Low | 🔲 |
| 13 | CSV Import with Visual Column Mapper | Medium | 🔲 |
| 14 | Item Templates Per Drawer (auto-fill defaults) | Low | 🔲 |
| 15 | Duplicate Detection & Smart Merge (URL + fuzzy title) | Medium | 🔲 |
| 16 | Sortable List View Columns (click headers to sort) | Low | 🔲 |

---

## 🔲 Upcoming — Database Inspirations (Extended Features)

> **Source:** Design interview & platform research  
> **Status:** Approved concepts, not yet planned in detail

| Feature | Inspired By | Status |
|---------|------------|:------:|
| "Alternatives To" bidirectional grouping | AlternativeTo.net | 🔲 |
| Feature checklist pills ("Has: Offline", "Has: Self-hosted") | AlternativeTo.net | 🔲 |
| "Similar Items" recommendation engine (tag similarity) | Play Store | 🔲 |
| 🎲 Random Item Jumper (press R for random pick) | Discogs / MusicBrainz | 🔲 |
| Multi-Drawer membership (1 item in multiple drawers) | Are.na / Pinterest | 🔲 |
| Flashcard / Quiz study mode | Anki / SuperMemo | 🔲 |
| 1-click code snippet box on cards | Raycast / DevDocs | 🔲 |
| Interactive Obsidian-style knowledge graph | Obsidian.md | 🔲 |

---

## 🔲 Backlog — Polish & Quality of Life

> Not yet discussed in detail. Ideas to revisit.

| Feature | Category | Status |
|---------|----------|:------:|
| Mobile responsive layout improvements | UI/UX | 🔲 |
| Drag-and-drop card reordering | UI/UX | 🔲 |
| Undo/Redo system (Ctrl+Z) | Core | 🔲 |
| Dark/Light mode toggle per theme | Themes | 🔲 |
| Notification/toast queue system improvements | UI/UX | 🔲 |
| Performance optimization for 5,000+ items | Core | 🔲 |
| Accessibility audit (ARIA, screen readers) | A11Y | 🔲 |
| Offline docs / help system improvements | Docs | 🔲 |

---

## 📐 Build Protocol (Rules)

1. **Build in stages.** Break between every build so the user can verify.
2. **GitHub sync before each stage.** Push each stage commit immediately to `origin/main`.
3. **Plan exclusions:** `new_themes_plan.md` stays in local artifacts only — NOT committed to Git.
4. **Pure CSS themes only.** No image generation, no external network requests.
5. **Single-file architecture.** Everything lives in `app.html` (~38,000+ lines).
6. **Syntax check before every commit:**
   ```powershell
   node -e "const fs=require('fs');const h=fs.readFileSync('app.html','utf8');const m=[...h.matchAll(/<script[\s\S]*?>([\s\S]*?)<\/script>/gi)];m.forEach((s,i)=>{try{new Function(s[1]);console.log('Script '+(i+1)+' OK')}catch(e){console.error('Script '+(i+1)+' FAIL:',e.message);process.exit(1)}})"
   ```

---

## 🗓️ Suggested Execution Order

```
Current ──► Easter Eggs (2 stages)
         ──► Database Phase 1 (Stages 8–11)
         ──► Database Phase 2 (Stages 12–16)
         ──► Extended Inspirations features
         ──► Polish & QoL backlog
```

> Each phase is independent. Easter Eggs can ship before database work begins.
