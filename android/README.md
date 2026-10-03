# CURIO — Android Application

Native Android implementation of **CURIO — The Curator**, maintaining 100% functional parity with desktop and web, combined with touch-first mobile UI/UX and native Android platform integration.

---

## 🌟 Key Features on Android

- **100% Offline Single-APK**: All 15 pre-loaded encyclopedias (1,366+ items), 16 nostalgic themes, and JSZip archiver run locally via `WebViewAssetLoader`. Zero network needed.
- **Mobile Bottom Navigation Bar**: Quick-thumb navigation for **Vaults**, **Views**, **+ New Item**, **Search**, and **Themes**.
- **Tactile Haptic Feedback**: Native vibration patterns on card clicks, ratings, and view toggles via `CurioAndroidBridge`.
- **System Theme Synchronization**: Status bar and navigation bar automatically tint to match the active Curio theme (Windows 95 teal, XP royal blue, Terminal black, etc.).
- **Android "Share to CURIO" Target**: Select any text or link in Chrome, Twitter, Reddit, or YouTube and tap **Share → CURIO** to instantly curate it.
- **Native File Chooser**: WebChromeClient integration for camera photos, screenshot galleries, and logo uploads.
- **Android Back Gesture**: Gracefully closes active bottom sheets, search modals, and lightboxes before exiting.

---

## 🚀 Quick Start (Building the APK)

### Method 1: Android Studio (Recommended, 1-Click)
1. Open **Android Studio**.
2. Select **File → Open...** and choose the `android` folder:
   ```
   c:\Users\Gulam Mustafa\Games\GDD\android
   ```
3. Let Gradle sync dependencies.
4. Click the green **Run (▶)** button or press `Shift + F10` to deploy directly to your connected Android phone or emulator.

---

### Method 2: Command Line (Gradle)
From this directory:

```bash
# Build Debug APK
./gradlew assembleDebug

# Output APK path:
# app/build/outputs/apk/debug/app-debug.apk

# Install to connected device via ADB
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

---

### Method 3: Instant Zero-Install PWA (No Build Required)
If you need CURIO on your Android device **immediately without compiling code**:
1. Open Chrome on your Android phone.
2. Navigate to: [https://fldlvgox-ux.github.io/Curio/app.html](https://fldlvgox-ux.github.io/Curio/app.html)
3. Tap the **⋮ (three dots)** menu in Chrome.
4. Tap **"Install App"** (or **"Add to Home Screen"**).
5. CURIO installs as a standalone, fullscreen Android app with its custom cyan icon, offline cache, and full IndexedDB storage!

---

## 📁 Project Structure

```
android/
├── app/
│   ├── build.gradle
│   ├── proguard-rules.pro
│   └── src/main/
│       ├── AndroidManifest.xml
│       ├── java/com/curio/thecurator/
│       │   ├── MainActivity.kt          # WebView setup, asset loader, intent ingestion
│       │   └── CurioAndroidBridge.kt     # Haptics, toasts, sharing, zip downloads
│       ├── res/
│       │   ├── layout/activity_main.xml
│       │   ├── values/ (colors, strings, themes)
│       │   ├── drawable/ (vector launcher icons)
│       │   └── mipmap-anydpi-v26/
│       └── assets/www/
│           ├── index.html
│           ├── app.html                  # Full Curio app with mobile bottom nav
│           ├── jszip.min.js
│           ├── logo.svg
│           └── manifest.json
├── build.gradle
├── gradle.properties
├── settings.gradle
└── README.md
```
