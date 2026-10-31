# Curio Theme Scaffolding Tool
# Usage: powershell ./tools/scaffold-theme.ps1 -ThemeId "curio-theme-mytheme" -ThemeName "My Theme" -Family "custom"

param (
    [Parameter(Mandatory=$true)]
    [string]$ThemeId,

    [Parameter(Mandatory=$true)]
    [string]$ThemeName,

    [Parameter(Mandatory=$false)]
    [string]$Family = "custom",

    [Parameter(Mandatory=$false)]
    [string]$Author = "Curio Community",

    [Parameter(Mandatory=$false)]
    [string]$Description = "Immersive custom theme for Curio."
)

if (-not $ThemeId.StartsWith("curio-theme-")) {
    $ThemeId = "curio-theme-" + $ThemeId
}

$pluginsDir = Join-Path $PSScriptRoot "..\plugins"
$targetDir = Join-Path $pluginsDir $ThemeId

if (Test-Path $targetDir) {
    Write-Host "[!] Error: Theme directory '$targetDir' already exists!" -ForegroundColor Red
    exit 1
}

New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
Write-Host "[+] Created theme folder: $targetDir" -ForegroundColor Green

# 1. Generate manifest.json with all 46 required tokens
$manifest = [ordered]@{
    id = $ThemeId
    name = $ThemeName
    version = "1.0.0"
    type = "theme"
    author = $Author
    description = $Description
    family = $Family
    entry = "theme.css"
    tokens = [ordered]@{
        "--bg" = "#090d16"
        "--surface" = "#111726"
        "--surface-2" = "#182238"
        "--text" = "#f1f5f9"
        "--text-dim" = "#94a3b8"
        "--accent" = "#06b6d4"
        "--accent-text" = "#ffffff"
        "--border" = "#1e293b"
        "--select-bg" = "#3b82f6"
        "--select-fg" = "#ffffff"
        "--danger" = "#f43f5e"
        "--ok" = "#10b981"
        "--warn" = "#f59e0b"
        "--font-ui" = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
        "--font-display" = "inherit"
        "--font-mono" = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
        "--font-size-base" = "14px"
        "--font-smoothing" = "antialiased"
        "--space-1" = "4px"
        "--space-2" = "8px"
        "--space-3" = "12px"
        "--space-4" = "16px"
        "--space-5" = "24px"
        "--row-height" = "36px"
        "--control-height" = "32px"
        "--pixel-scale" = "1"
        "--radius-window" = "8px"
        "--radius-control" = "4px"
        "--radius-chip" = "999px"
        "--avatar-shape" = "50%"
        "--cut-tl" = "0px"
        "--cut-tr" = "0px"
        "--cut-br" = "0px"
        "--cut-bl" = "0px"
        "--bevel-light" = "transparent"
        "--bevel-dark" = "transparent"
        "--bevel-width" = "0px"
        "--shadow-raised" = "0 2px 8px rgba(0,0,0,0.3)"
        "--shadow-pressed" = "inset 0 2px 4px rgba(0,0,0,0.3)"
        "--shadow-hard" = "none"
        "--gradient-title" = "none"
        "--gradient-button" = "none"
        "--grain" = "none"
        "--dither-pattern" = "none"
        "--focus-ring" = "0 0 0 2px #06b6d4"
        "--default-button-ring" = "none"
    }
}

$manifestJson = $manifest | ConvertTo-Json -Depth 5
$manifestFile = Join-Path $targetDir "manifest.json"
[System.IO.File]::WriteAllText($manifestFile, $manifestJson, (New-Object System.Text.UTF8Encoding $false))
Write-Host "  [+] Wrote: manifest.json" -ForegroundColor Cyan

# 2. Generate theme.css boilerplate with the 7 custom artwork slots
$shortId = $ThemeId.Replace("curio-theme-", "")
$themeCss = @"
/* ==========================================================================
   Curio Theme Plugin: $ThemeName
   ID: $ThemeId / $shortId
   Author: $Author
   Generated via Curio Scaffolding Tool
   ========================================================================== */

/* 1. ROOT VARIABLES & PALETTE OVERRIDES */
[data-theme="$ThemeId"],
[data-theme="$shortId"] {
  --bg: #090d16;
  --surface: #111726;
  --surface-2: #182238;
  --text: #f1f5f9;
  --text-dim: #94a3b8;
  --accent: #06b6d4;
  --accent-text: #ffffff;
  --border: #1e293b;
  --select-bg: #3b82f6;
  --select-fg: #ffffff;
}

/* 2. GLOBAL ATMOSPHERIC TEXTURE (ARTWORK SLOT 7) */
[data-theme="$ThemeId"] body::after,
[data-theme="$shortId"] body::after {
  content: "" !important;
  position: fixed !important;
  inset: 0 !important;
  pointer-events: none !important;
  z-index: 0 !important;
  opacity: 0.15 !important;
  background-image: linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px) !important;
  background-size: 24px 24px !important;
}

[data-theme="$ThemeId"] .app-shell,
[data-theme="$shortId"] .app-shell {
  position: relative !important;
  z-index: 1 !important;
}

/* 3. BRAND HEADER & CUSTOM LOGO EMBLEM (ARTWORK SLOT 1) */
[data-theme="$ThemeId"] .brand-title svg,
[data-theme="$shortId"] .brand-title svg {
  display: none !important;
}

[data-theme="$ThemeId"] .brand-title::before,
[data-theme="$shortId"] .brand-title::before {
  content: "" !important;
  display: inline-block !important;
  width: 24px !important;
  height: 24px !important;
  margin-right: 0.5rem !important;
  background-size: contain !important;
  background-repeat: no-repeat !important;
  background-position: center !important;
  /* Replace with your procedural SVG data: URI */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2306b6d4'%3E%3Cpolygon points='12 2 2 22 22 22'/%3E%3C/svg%3E") !important;
}

[data-theme="$ThemeId"] .brand-title,
[data-theme="$shortId"] .brand-title {
  color: var(--text) !important;
  display: inline-flex !important;
  align-items: center !important;
}

/* 4. SIDEBAR LORE MOTIF / BOTTOM CREST (ARTWORK SLOT 2) */
[data-theme="$ThemeId"] .sidebar::after,
[data-theme="$shortId"] .sidebar::after {
  content: "" !important;
  position: absolute !important;
  bottom: 16px !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  width: 80% !important;
  height: 36px !important;
  pointer-events: none !important;
  opacity: 0.25 !important;
  background-size: contain !important;
  background-repeat: no-repeat !important;
  background-position: center !important;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 24'%3E%3Cpath d='M10 12 L50 2 L90 12 L50 22 Z' fill='none' stroke='%2306b6d4' stroke-width='1.5'/%3E%3C/svg%3E") !important;
}

/* 5. TOP BAR TELEMETRY STRIPE / ORNAMENT (ARTWORK SLOT 3) */
[data-theme="$ThemeId"] .top-bar::after,
[data-theme="$shortId"] .top-bar::after {
  content: "" !important;
  position: absolute !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  height: 2px !important;
  background: linear-gradient(90deg, var(--accent) 0%, transparent 80%) !important;
}

/* 6. FILTER PANEL SEPARATOR / DIVIDER (ARTWORK SLOT 4) */
[data-theme="$ThemeId"] .filter-panel::before,
[data-theme="$shortId"] .filter-panel::before {
  content: "" !important;
  display: block !important;
  height: 4px !important;
  margin-bottom: 8px !important;
  background: radial-gradient(circle, var(--accent) 1px, transparent 1px) !important;
  background-size: 8px 4px !important;
  opacity: 0.4 !important;
}

/* 7. ITEM CARDS ANATOMY & FRAMES (ARTWORK SLOT 5) */
[data-theme="$ThemeId"] .item-card,
[data-theme="$shortId"] .item-card,
[data-theme="$ThemeId"] .detail-card,
[data-theme="$shortId"] .detail-card {
  position: relative !important;
  border: 1px solid var(--border) !important;
  background: var(--surface) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
  transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}

[data-theme="$ThemeId"] .item-card:hover,
[data-theme="$shortId"] .item-card:hover {
  transform: translateY(-2px) !important;
  border-color: var(--accent) !important;
}

/* 8. MODALS & DIALOG ENDCAPS (ARTWORK SLOT 6) */
[data-theme="$ThemeId"] .modal-content,
[data-theme="$shortId"] .modal-content {
  border: 1px solid var(--border) !important;
  background: var(--surface) !important;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6) !important;
}

[data-theme="$ThemeId"] .modal-header,
[data-theme="$shortId"] .modal-header {
  border-bottom: 1px solid var(--border) !important;
  background: var(--surface-2) !important;
}

/* 9. TACTILE KEYCAP BUTTONS */
[data-theme="$ThemeId"] .btn-primary,
[data-theme="$shortId"] .btn-primary {
  background: var(--accent) !important;
  color: var(--accent-text) !important;
  border: none !important;
  border-radius: var(--radius-control) !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  transition: filter 0.12s ease, transform 0.08s ease !important;
}

[data-theme="$ThemeId"] .btn-primary:active,
[data-theme="$shortId"] .btn-primary:active {
  transform: translateY(1px) scale(0.98) !important;
}
"@

$cssFile = Join-Path $targetDir "theme.css"
[System.IO.File]::WriteAllText($cssFile, $themeCss, (New-Object System.Text.UTF8Encoding $false))
Write-Host "  [+] Wrote: theme.css" -ForegroundColor Cyan

# 3. Update plugin index
$updateScript = Join-Path $PSScriptRoot "update-plugin-index.ps1"
if (Test-Path $updateScript) {
    & $updateScript
}

Write-Host "`nTheme '$ThemeName' ($ThemeId) successfully scaffolded in: plugins/$ThemeId" -ForegroundColor Green
Write-Host "You can now edit 'plugins/$ThemeId/theme.css' and reload Curio!" -ForegroundColor Cyan
