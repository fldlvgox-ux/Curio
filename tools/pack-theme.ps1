# Curio Theme Packaging Tool
# Usage: powershell ./tools/pack-theme.ps1 -ThemeId "curio-theme-macos8"

param (
    [Parameter(Mandatory=$true)]
    [string]$ThemeId,

    [Parameter(Mandatory=$false)]
    [string]$OutFile = ""
)

if (-not $ThemeId.StartsWith("curio-theme-")) {
    $ThemeId = "curio-theme-" + $ThemeId
}

$pluginsDir = Join-Path $PSScriptRoot "..\plugins"
$themeDir = Join-Path $pluginsDir $ThemeId

if (-not (Test-Path $themeDir)) {
    Write-Host "[!] Error: Theme directory '$themeDir' does not exist!" -ForegroundColor Red
    exit 1
}

$manifestPath = Join-Path $themeDir "manifest.json"
$cssPath = Join-Path $themeDir "theme.css"
$previewPath = Join-Path $themeDir "preview.png"

if (-not (Test-Path $manifestPath)) {
    Write-Host "[!] Error: manifest.json missing in $themeDir" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path $cssPath)) {
    Write-Host "[!] Error: theme.css missing in $themeDir" -ForegroundColor Red
    exit 1
}

# 1. Validate against contract
$contractPath = Join-Path $PSScriptRoot "..\src\plugins\contract.json"
if (Test-Path $contractPath) {
    Write-Host "Validating tokens against contract..." -ForegroundColor Cyan
    $contract = Get-Content -Path $contractPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $manifest = Get-Content -Path $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
    
    $requiredTokens = @()
    foreach ($category in $contract.tokens.PSObject.Properties) {
        foreach ($token in $category.Value.PSObject.Properties) {
            $requiredTokens += $token.Name
        }
    }
    
    $missingTokens = @()
    foreach ($req in $requiredTokens) {
        if (-not $manifest.tokens.PSObject.Properties[$req]) {
            $missingTokens += $req
        }
    }
    
    if ($missingTokens.Count -gt 0) {
        Write-Host "  [!] Warning: Missing $($missingTokens.Count) token(s):" -ForegroundColor Yellow
        $missingTokens | ForEach-Object { Write-Host "      - $_" -ForegroundColor Yellow }
    } else {
        Write-Host "  [+] All 46 required tokens verified!" -ForegroundColor Green
    }
}

# 2. Output ZIP Destination
if ([string]::IsNullOrWhiteSpace($OutFile)) {
    $OutFile = Join-Path $pluginsDir "$ThemeId.zip"
}

if (Test-Path $OutFile) {
    Remove-Item -Path $OutFile -Force
}

# 3. Create ZIP using .NET ZipArchive to ensure relative paths
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::Open($OutFile, [System.IO.Compression.ZipArchiveMode]::Create)

try {
    [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $manifestPath, "manifest.json") | Out-Null
    Write-Host "  [+] Packed: manifest.json" -ForegroundColor Cyan

    [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $cssPath, "theme.css") | Out-Null
    Write-Host "  [+] Packed: theme.css" -ForegroundColor Cyan

    if (Test-Path $previewPath) {
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $previewPath, "preview.png") | Out-Null
        Write-Host "  [+] Packed: preview.png" -ForegroundColor Cyan
    }
} finally {
    $zip.Dispose()
}

$zipSize = (Get-Item $OutFile).Length / 1KB
Write-Host "`nTheme package created successfully ($([Math]::Round($zipSize, 1)) KB):" -ForegroundColor Green
Write-Host "$OutFile" -ForegroundColor Yellow
Write-Host "You can import this .zip into Curio via Settings -> Themes -> Import Theme (.zip)!" -ForegroundColor Cyan
