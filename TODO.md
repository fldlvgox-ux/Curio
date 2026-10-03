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
- [x] PWA install support
- [x] Image galleries with lightbox
- [x] Filter bar with tag cloud, rating, status, media filters
- [x] Monogram avatars for items without images

---

## 🔲 In Progress

### 🎮 Easter Eggs & UI Tweaks — PLANNED (Approved Design)
> **Plan:** [`EASTER_EGGS_PLAN.md`](EASTER_EGGS_PLAN.md)  
> **Status:** Design complete, awaiting build approval  
> **Stages:** 2 commits

| # | Egg | Discovery Method | Status |
|---|-----|-----------------|--------|
| 1 | Logo multi-click Star Wars credits | 5 rapid clicks on CURIO title | 🔲 |
| 2 | Spotlight magic queries (barrel roll, confetti, hello world) | Type phrase in Ctrl+K | 🔲 |
| 3 | Win95 Clippy idle assistant (6 snarky messages) | 60s idle on Win95 theme | 🔲 |
| 4 | Jarvis boot sequence banner | 60s idle on Jarvis theme | 🔲 |
| 5 | Empty-state Pong mini-game (survival mode) | Click hint when 0 items | 🔲 |
| — | Settings toggle to disable Easter eggs | About tab in Settings | 🔲 |
| — | Guide tab `🔮 ???` teaser card | Bottom of Guide tab | 🔲 |

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
