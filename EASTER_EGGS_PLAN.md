# 🎮 Easter Eggs & UI Tweaks — Implementation Plan

## Goal
Add 5 carefully crafted Easter eggs to CURIO that reward curious users with delightful hidden interactions. Each egg uses a different discovery method — creating a layered "secrets" system that feels alive.

## User Review Required

> [!IMPORTANT]
> **Settings toggle**: A new "Enable Easter Eggs" toggle will be added to the **About** tab in Settings. This persists via `localStorage` key `curio_easter_eggs` (default: `"true"` / enabled). When disabled, ALL eggs are suppressed — no idle timers, no magic queries, no mini-games.

> [!IMPORTANT]
> **Guide teaser**: A new `🔮 Secrets` card will be added at the bottom of the Guide tab with the text: *"CURIO has hidden surprises. Some respond to curiosity, some reward patience, some appear when you least expect them. Can you find them all?"* — no specifics revealed.

---

## Proposed Changes

### Commit 1: Visual Effects & Discoverability System
*Logo credits, Spotlight magic queries, Settings toggle, Guide teaser*

---

#### Overview of Egg #1: Logo Multi-Click Credits

| Property | Value |
|----------|-------|
| **Trigger** | 5 rapid clicks on `.brand-title` element (line 6446) |
| **Effect** | Full-page cinematic takeover with Star Wars-style scrolling credits |
| **Theme-aware** | Yes — uses CSS variables for colors |
| **Dismiss** | Escape key, click anywhere, or auto-dismiss after scroll completes (~15s) |
| **Content** | Funny cinematic credits with visual flair |

**Credits content (scrolling text):**
```
CURIO — THE CURATOR
Version 3.2.0

━━━━━━━━━━━━━━━━━━

A Film by Your Browser's IndexedDB

⭐ STARRING ⭐

1,366 Lovingly Curated Items
as "The Collection"

15 Encyclopedias of Knowledge
as "The Catalogs"

16 Visual Themes
as "The Wardrobe Department"

━━━━━━━━━━━━━━━━━━

🎬 CREW

Director of Databases .......... IndexedDB
Chief Pixel Officer ............ CSS
Lead Architect ................. One Very Large HTML File
Stunt Coordinator .............. Ctrl+K
Coffee Budget .................. ∞

━━━━━━━━━━━━━━━━━━

🏆 SPECIAL THANKS

To everyone who clicks things
just to see what happens.

You found this. You're one of us.

━━━━━━━━━━━━━━━━━━

No databases were harmed
in the making of this application.

© 2024-2026 CURIO
"Curate everything. Forget nothing."
```

**Implementation:**

##### CSS (~60 lines) — Add before `/* Settings Modal Styles */` (line 5464)
```css
/* Easter Egg: Credits Overlay */
.credits-overlay {
  position: fixed; inset: 0; z-index: 100000;
  background: rgba(0,0,0,0.95);
  display: flex; align-items: flex-end; justify-content: center;
  opacity: 0; pointer-events: none;
  transition: opacity 0.6s ease;
  perspective: 400px;
  overflow: hidden;
}
.credits-overlay.active {
  opacity: 1; pointer-events: all;
}
.credits-scroll {
  width: 70%; max-width: 500px;
  text-align: center;
  color: var(--accent-cyan, #06b6d4);
  font-size: 1.05rem; line-height: 2;
  white-space: pre-line;
  transform: rotateX(25deg);
  transform-origin: 50% 100%;
  animation: creditsRoll 18s linear forwards;
}
@keyframes creditsRoll {
  0%   { transform: rotateX(25deg) translateY(100vh); }
  100% { transform: rotateX(25deg) translateY(-250%); }
}
.credits-scroll .credits-title {
  font-size: 2rem; font-weight: 900;
  letter-spacing: 0.3em;
  color: var(--text-main, #e2e8f0);
  text-shadow: 0 0 30px var(--accent-cyan, #06b6d4);
  margin-bottom: 0.5rem;
}
.credits-scroll .credits-sub {
  font-size: 0.9rem;
  color: var(--text-dim, #94a3b8);
}
.credits-scroll .credits-divider {
  color: var(--border-medium, #334155);
  letter-spacing: 0.5em;
}
.credits-scroll .credits-section {
  color: var(--accent-emerald, #10b981);
  font-weight: 700; font-size: 1.1rem;
  margin-top: 1rem;
}
```

##### HTML (~1 line) — Add after the command palette modal (after line 7539 closing `</div>`)
```html
<div class="credits-overlay" id="credits-overlay"><div class="credits-scroll" id="credits-scroll"></div></div>
```

##### JavaScript (~40 lines) — Add in the Easter Eggs section
```javascript
// --- EASTER EGGS SYSTEM ---
function easterEggsEnabled() {
  return localStorage.getItem("curio_easter_eggs") !== "false";
}

// Egg #1: Logo Multi-Click Credits
(function initLogoCredits() {
  const brandTitle = document.querySelector(".brand-title");
  if (!brandTitle) return;
  let clickCount = 0, clickTimer = null;
  brandTitle.style.cursor = "pointer";
  brandTitle.addEventListener("click", () => {
    if (!easterEggsEnabled()) return;
    clickCount++;
    clearTimeout(clickTimer);
    clickTimer = setTimeout(() => { clickCount = 0; }, 800);
    if (clickCount >= 5) {
      clickCount = 0;
      showCredits();
    }
  });
})();

function showCredits() {
  const overlay = document.getElementById("credits-overlay");
  const scroll = document.getElementById("credits-scroll");
  if (!overlay || !scroll) return;
  scroll.innerHTML = `[credits HTML content here]`;
  overlay.classList.add("active");
  // Auto-dismiss after animation
  const autoDismiss = setTimeout(() => hideCredits(), 19000);
  overlay._autoDismiss = autoDismiss;
  overlay.addEventListener("click", hideCredits, { once: true });
  const escHandler = (e) => { if (e.key === "Escape") { hideCredits(); window.removeEventListener("keydown", escHandler); }};
  window.addEventListener("keydown", escHandler);
}

function hideCredits() {
  const overlay = document.getElementById("credits-overlay");
  if (!overlay) return;
  clearTimeout(overlay._autoDismiss);
  overlay.classList.remove("active");
}
```

---

#### Overview of Egg #2: Spotlight Magic Queries

| Query | Type | Effect |
|-------|------|--------|
| `"do a barrel roll"` | Full-screen | Entire page rotates 360° over 1.2s (Google classic) |
| `"hello world"` | Inline result | Special result item with retro terminal greeting + blinking cursor |
| `"party"` or `"celebrate"` | Full-screen | Confetti emoji explosion — 40 emojis (🎉🎊✨🥳🎈) rain down from top |

**Implementation — Intercept in `renderPaletteResults()`** (line 35616):

```javascript
// Inside renderPaletteResults, before the "no results" check:
const magicResult = checkMagicQuery(q);
if (magicResult) {
  if (magicResult.type === "fullscreen") {
    magicResult.execute();
    closeCommandPalette();
    return;
  }
  if (magicResult.type === "inline") {
    resultsContainer.innerHTML = magicResult.html;
    return;
  }
}
```

**Magic query handlers:**
```javascript
function checkMagicQuery(q) {
  if (!easterEggsEnabled()) return null;
  if (q === "do a barrel roll") {
    return { type: "fullscreen", execute: () => {
      document.body.style.transition = "transform 1.2s ease";
      document.body.style.transform = "rotate(360deg)";
      setTimeout(() => { document.body.style.transition = ""; document.body.style.transform = ""; }, 1300);
    }};
  }
  if (q === "party" || q === "celebrate") {
    return { type: "fullscreen", execute: () => launchConfetti() };
  }
  if (q === "hello world") {
    return { type: "inline", html: `<div style="padding:1.5rem; text-align:center; font-family:monospace; color:var(--accent-emerald);">
      <div style="font-size:1.5rem; margin-bottom:0.5rem;">></span> HELLO, WORLD<span class="blink-cursor">█</span></div>
      <div style="color:var(--text-dim); font-size:0.8rem;">CURIO TERMINAL v3.2.0 — READY.</div>
    </div>` };
  }
  return null;
}

function launchConfetti() {
  const emojis = ["🎉","🎊","✨","🥳","🎈","🎆","⭐","💫"];
  for (let i = 0; i < 40; i++) {
    const el = document.createElement("div");
    el.textContent = emojis[Math.floor(Math.random() * emojis.length)];
    el.style.cssText = `position:fixed; top:-40px; left:${Math.random()*100}vw; font-size:${1.5+Math.random()*1.5}rem; z-index:100001; pointer-events:none; animation:confettiFall ${2+Math.random()*2}s linear forwards; animation-delay:${Math.random()*0.8}s;`;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 5000);
  }
}
```

**CSS for confetti & blink cursor:**
```css
@keyframes confettiFall {
  0%   { transform: translateY(0) rotate(0deg); opacity: 1; }
  100% { transform: translateY(110vh) rotate(720deg); opacity: 0; }
}
.blink-cursor { animation: blinkCursor 1s step-end infinite; }
@keyframes blinkCursor { 0%,50% { opacity:1; } 51%,100% { opacity:0; } }
```

---

#### Settings Toggle (About Tab)

Add to the **About tab** (`#tab-about`, after line 7532):

```html
<div style="margin-top:0.75rem; padding-top:0.75rem; border-top:1px solid var(--border-subtle); display:flex; justify-content:space-between; align-items:center;">
  <div>
    <span style="font-size:0.82rem;">🔮 Easter Eggs</span>
    <div style="font-size:0.72rem; color:var(--text-dim);">Hidden surprises & delightful interactions</div>
  </div>
  <label style="position:relative; width:36px; height:20px; cursor:pointer;">
    <input type="checkbox" id="chk-easter-eggs" checked style="opacity:0; width:0; height:0;">
    <span class="toggle-slider"></span>
  </label>
</div>
```

**JS handler:**
```javascript
const eggToggle = document.getElementById("chk-easter-eggs");
if (eggToggle) {
  eggToggle.checked = localStorage.getItem("curio_easter_eggs") !== "false";
  eggToggle.addEventListener("change", () => {
    localStorage.setItem("curio_easter_eggs", eggToggle.checked ? "true" : "false");
  });
}
```

> [!NOTE]
> Need to check if a `.toggle-slider` CSS class already exists in the app. If not, we'll need a small inline CSS toggle switch — or style it as a simple checkbox.

---

#### Guide Tab Teaser

Add at the bottom of the Guide tab (before line 7128 closing `</div>`):

```html
<div style="background:var(--bg-surface-raised); border:1px solid var(--border-subtle); border-radius:var(--radius-md); padding:1rem; opacity:0.7;">
  <div style="font-weight:700; color:var(--accent-purple, #a855f7); font-size:0.95rem; margin-bottom:0.35rem; display:flex; align-items:center; gap:0.4rem;">
    <span>🔮 ???</span>
  </div>
  <p style="font-size:0.83rem; color:var(--text-muted); line-height:1.5; font-style:italic;">
    CURIO has hidden surprises. Some respond to curiosity, some reward patience, some appear when you least expect them. Can you find them all?
  </p>
</div>
```

---

### Commit 2: Interactive Features & Theme Gags
*Win95 Clippy, Jarvis boot sequence, Pong mini-game*

---

#### Overview of Egg #3: Win95 Clippy

| Property | Value |
|----------|-------|
| **Trigger** | 60 seconds of idle time while `win95` theme is active |
| **Visual** | CSS-drawn Clippy character (paperclip shape) in bottom-right corner with speech bubble |
| **Messages** | 6 rotating snarky messages, random pick |
| **Dismiss** | Click the speech bubble or Clippy, or it auto-dismisses after 8 seconds |
| **Repeat** | Re-appears after another 120s of idle |

**Clippy messages pool:**
1. "It looks like you're organizing things. Would you like help? (Just kidding, I can't actually help.)"
2. "Did you know this app has 16 themes? I liked it better when we only had 256 colors."
3. "I see you haven't added any items in a while. Writer's block? Or just procrastinating?"
4. "Fun fact: I was fired from Microsoft Office in 2007. This is my side gig now."
5. "You've been staring at this screen for a while. Blink. Please."
6. "Psst... try clicking the CURIO logo 5 times. 👀"

**CSS (~55 lines):**
```css
/* Easter Egg: Clippy Assistant */
.clippy-container {
  position: fixed; bottom: 1.5rem; right: 1.5rem;
  z-index: 99999; display: flex; align-items: flex-end; gap: 0.5rem;
  opacity: 0; transform: translateY(20px);
  transition: opacity 0.4s, transform 0.4s;
  pointer-events: none;
}
.clippy-container.visible {
  opacity: 1; transform: translateY(0); pointer-events: all;
}
.clippy-bubble {
  background: #ffffcc; border: 2px solid #000; border-radius: 8px;
  padding: 0.65rem 0.85rem; max-width: 240px;
  font-family: Tahoma, "MS Sans Serif", sans-serif;
  font-size: 0.78rem; color: #000; line-height: 1.4;
  box-shadow: 2px 2px 0 #000;
  position: relative; cursor: pointer;
}
.clippy-bubble::after {
  content: ""; position: absolute; bottom: 8px; right: -10px;
  border: 5px solid transparent; border-left-color: #000;
}
.clippy-char {
  width: 36px; height: 52px; cursor: pointer;
  /* Pure CSS paperclip character */
  border: 3px solid #808080; border-radius: 0 50% 50% 0;
  position: relative;
  background: linear-gradient(to right, transparent 40%, #c0c0c0 40%, #c0c0c0 60%, transparent 60%);
}
.clippy-char::before {
  content: "📎"; font-size: 2.2rem; position: absolute;
  top: -8px; left: -6px;
}
.clippy-char::after {
  content: "👀"; font-size: 0.7rem;
  position: absolute; top: 4px; left: 8px;
}
```

**JS (~40 lines):**
```javascript
// Egg #3: Win95 Clippy
let clippyIdleTimer = null;
const CLIPPY_MESSAGES = [ /* ... 6 messages ... */ ];

function initClippyWatcher() {
  // Called when theme changes. Clear existing timer, restart if win95.
  clearTimeout(clippyIdleTimer);
  if (document.documentElement.getAttribute("data-theme") !== "win95") return;
  if (!easterEggsEnabled()) return;
  resetClippyTimer();
}

function resetClippyTimer() {
  clearTimeout(clippyIdleTimer);
  clippyIdleTimer = setTimeout(showClippy, 60000);
  // Reset on any user interaction
  ["click","keydown","mousemove","scroll"].forEach(evt =>
    window.addEventListener(evt, () => { /* debounced reset */ }, { once: true, passive: true })
  );
}

function showClippy() {
  // Create clippy DOM, add .visible class, set auto-dismiss, attach click-to-dismiss
}
```

**Hook into `setTheme()`** (line 36903) — add `initClippyWatcher()` call at end of function.

---

#### Overview of Egg #4: Jarvis Boot Sequence

| Property | Value |
|----------|-------|
| **Trigger** | 60 seconds of idle time while `jarvis` theme is active |
| **Visual** | Translucent banner slides in from top with sequential boot lines |
| **Content** | 5-line system boot sequence appearing one-by-one with typewriter effect |
| **Dismiss** | Auto-dismisses after sequence completes (~6 seconds), click to dismiss early |
| **Repeat** | Re-appears after another 180s of idle |

**Boot sequence lines:**
```
> STARK INDUSTRIES — CURIO INTERFACE v3.2.0
> INITIALIZING ARC REACTOR CORE............ [OK]
> SCANNING DATABASE: 1,366 ITEMS INDEXED... [OK]
> THREAT ASSESSMENT: ALL CLEAR
> ALL SYSTEMS NOMINAL. WELCOME BACK, DIRECTOR.
```

**CSS (~35 lines):**
```css
/* Easter Egg: Jarvis Boot Sequence */
.jarvis-boot-banner {
  position: fixed; top: 0; left: 0; right: 0;
  z-index: 99999;
  background: linear-gradient(180deg, rgba(0,20,40,0.95), rgba(0,20,40,0.7));
  border-bottom: 1px solid #00f0ff;
  padding: 1rem 1.5rem;
  font-family: "Consolas", "Courier New", monospace;
  font-size: 0.8rem; color: #00f0ff;
  transform: translateY(-100%);
  transition: transform 0.5s ease;
  box-shadow: 0 4px 30px rgba(0,240,255,0.3);
  cursor: pointer;
}
.jarvis-boot-banner.active {
  transform: translateY(0);
}
.jarvis-boot-line {
  opacity: 0; margin: 0.25rem 0;
  animation: jarvisLineIn 0.3s ease forwards;
}
.jarvis-boot-line .status-ok {
  color: #ffd000; font-weight: 700;
}
@keyframes jarvisLineIn {
  from { opacity: 0; transform: translateX(-10px); }
  to   { opacity: 1; transform: translateX(0); }
}
```

**JS (~35 lines):** Similar idle-timer pattern as Clippy, hooked into `setTheme()`.

---

#### Overview of Egg #5: Empty-State Pong

| Property | Value |
|----------|-------|
| **Trigger** | Click "Feeling bored?" hint in empty state (0 items in current view) |
| **Visual** | Fixed retro arcade look — black bg, white elements, scanline overlay |
| **Gameplay** | Player vs Wall survival — paddle at bottom, ball bounces off 3 walls |
| **Controls** | Arrow keys/A-D AND mouse/touch |
| **Score** | Current round only (time survived in seconds), no persistence |
| **Dismiss** | Press Escape to exit back to empty state |

**Implementation:**

Modify the empty-state render (line 35944-35956) to add a "Feeling bored?" hint:

```javascript
if (items.length === 0) {
  container.innerHTML = `
    <div class="empty-state">
      <div class="empty-icon">🗄️</div>
      <h3>No matching items found</h3>
      <p>Try adjusting your search query, clearing filters, or adding a new item to this drawer.</p>
      <button class="btn-primary" id="btn-empty-new-item" style="margin-top:0.5rem;">+ Create Item</button>
      ${easterEggsEnabled() ? '<div class="pong-hint" id="pong-hint" style="margin-top:1.5rem; font-size:0.75rem; color:var(--text-dim); cursor:pointer; opacity:0.5; transition:opacity 0.3s;" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.5">🎮 Feeling bored?</div>' : ''}
    </div>
  `;
  // ... existing btn handler ...
  const pongHint = document.getElementById("pong-hint");
  if (pongHint) pongHint.addEventListener("click", startPong);
}
```

**Pong game engine (~120 lines JS + ~40 lines CSS):**
- Canvas-less: uses a container `<div>` with absolutely positioned ball and paddle `<div>` elements
- `requestAnimationFrame` game loop
- Ball physics: constant velocity, angle reflection off walls and paddle
- Paddle: CSS div following mouse X or keyboard A/D/arrow keys
- Score display: seconds survived, top-center
- Escape key exits, removes game container, re-renders items
- Retro styling: black background, white 2px elements, dashed center line, CRT scanline pseudo-overlay

```css
/* Easter Egg: Pong Game */
.pong-arena {
  position: fixed; inset: 0; z-index: 99998;
  background: #000; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
}
.pong-arena::before {
  content: ""; position: absolute; inset: 0;
  background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.03) 2px, rgba(255,255,255,0.03) 4px);
  pointer-events: none;
}
.pong-field {
  width: 600px; height: 400px; max-width: 90vw; max-height: 70vh;
  border: 2px solid #fff; position: relative;
  background: #000;
}
.pong-ball {
  width: 10px; height: 10px; background: #fff; border-radius: 50%;
  position: absolute; box-shadow: 0 0 8px #fff;
}
.pong-paddle {
  width: 80px; height: 10px; background: #fff;
  position: absolute; bottom: 10px; border-radius: 2px;
  box-shadow: 0 0 6px #fff;
}
.pong-score {
  font-family: monospace; color: #fff; font-size: 1.5rem;
  margin-bottom: 0.75rem; letter-spacing: 0.1em;
}
.pong-hint-text {
  font-family: monospace; color: #666; font-size: 0.75rem;
  margin-top: 0.5rem;
}
```

---

## Integration Points Summary

| File | Section | Line(s) | Change |
|------|---------|---------|--------|
| `app.html` | CSS (before Settings Modal) | ~5464 | Add ~190 lines CSS for credits, confetti, clippy, jarvis boot, pong |
| `app.html` | HTML (after settings modal) | ~7539 | Add credits overlay `<div>` |
| `app.html` | HTML (Guide tab) | ~7127 | Add `🔮 ???` secrets teaser card |
| `app.html` | HTML (About tab) | ~7532 | Add Easter Eggs toggle |
| `app.html` | JS (palette input handler) | ~37285 | Intercept magic queries before `renderPaletteResults` |
| `app.html` | JS (`renderPaletteResults`) | ~35616 | Add magic query check at start |
| `app.html` | JS (`setTheme`) | ~36920 | Add idle timer hooks for Clippy/Jarvis |
| `app.html` | JS (empty state render) | ~35944 | Add Pong hint link |
| `app.html` | JS (new section) | ~37320+ | Add full Easter Eggs system (~300 lines) |
| `GUIDE.md` | Section 7 or new section | ~100+ | Add teaser mention |
| `README.md` | Feature list | ~100 | Add Easter Eggs bullet |

---

## Staging Plan

### Stage 1 (Commit 1): Visual Effects & System
- Easter Eggs CSS block
- Credits overlay HTML + JS
- Spotlight magic queries (barrel roll, confetti, hello world)
- Settings toggle (About tab)
- Guide tab teaser card
- `easterEggsEnabled()` gate function
- **Test**: Verify logo 5-click credits, all 3 magic queries, toggle disable/re-enable
- **Push to GitHub**

### Stage 2 (Commit 2): Interactive Features
- Win95 Clippy (CSS + idle timer + messages)
- Jarvis boot sequence (CSS + idle timer + typewriter)
- Empty-state Pong game (CSS + game engine + escape exit)
- Hook idle timers into `setTheme()`
- Update `GUIDE.md` and `README.md`
- **Test**: Verify Clippy on Win95 (can fast-forward idle for testing), Jarvis boot, Pong gameplay
- **Push to GitHub**

---

## Verification Plan

### Automated Tests
```powershell
node -e "const fs=require('fs');const h=fs.readFileSync('app.html','utf8');const m=[...h.matchAll(/<script[\s\S]*?>([\s\S]*?)<\/script>/gi)];m.forEach((s,i)=>{try{new Function(s[1]);console.log('Script '+(i+1)+' OK')}catch(e){console.error('Script '+(i+1)+' FAIL:',e.message);process.exit(1)}})"
```

### Manual Verification — Stage 1
1. Open `app.html` in browser
2. Click the CURIO logo/title 5 times rapidly → credits should appear with Star Wars scroll
3. Press Escape or click → credits dismiss
4. Open Ctrl+K, type "do a barrel roll" → page rotates 360°
5. Open Ctrl+K, type "hello world" → retro terminal greeting appears inline
6. Open Ctrl+K, type "party" → confetti emoji explosion
7. Open Settings → About → verify Easter Eggs toggle exists, default ON
8. Toggle OFF → verify none of the above eggs work
9. Toggle ON → verify eggs work again
10. Open Settings → Guide → verify `🔮 ???` teaser card at bottom

### Manual Verification — Stage 2
1. Switch to **Win95** theme → wait 60 seconds idle → Clippy should appear bottom-right with a random message
2. Click Clippy → should dismiss
3. Switch to **Jarvis** theme → wait 60 seconds idle → boot sequence banner slides in from top
4. Verify boot lines appear sequentially with typewriter effect
5. Create a test drawer with 0 items → verify "🎮 Feeling bored?" hint appears
6. Click hint → Pong game launches, full-screen retro arcade
7. Test keyboard controls (arrows/A-D) and mouse paddle control
8. Press Escape → game exits, returns to empty state
9. Disable Easter Eggs in settings → verify Clippy, Jarvis, and Pong hint all suppressed

## Open Questions

> [!NOTE]
> **Toggle switch CSS**: Does the app already have a `.toggle-slider` CSS class? If yes, reuse it. If not, should we build a proper iOS-style toggle or use a simple styled checkbox?

> [!NOTE]
> **Clippy idle reset**: Should mouse movement reset the 60-second idle timer? (Recommended: yes, but debounced to avoid performance overhead — only reset on `click`, `keydown`, and throttled `mousemove`)
