# Curio Plugin Indexer
# Scans the plugins/ directory and regenerates plugins/plugin-index.json

$pluginsDir = Join-Path $PSScriptRoot "..\plugins"
$outputFile = Join-Path $pluginsDir "plugin-index.json"

Write-Host "Scanning plugin directory: $pluginsDir" -ForegroundColor Cyan

$pluginList = @()

$subDirs = Get-ChildItem -Path $pluginsDir -Directory | Where-Object { $_.Name -notmatch "^_" }

foreach ($dir in $subDirs) {
    $manifestPath = Join-Path $dir.FullName "manifest.json"
    if (Test-Path $manifestPath) {
        try {
            $manifestContent = Get-Content -Path $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
            $relativeDir = "./plugins/" + $dir.Name
            
            $entry = [ordered]@{
                id = $manifestContent.id
                name = $manifestContent.name
                version = $manifestContent.version
                type = $manifestContent.type
                author = if ($manifestContent.author) { $manifestContent.author } else { "Unknown" }
                description = if ($manifestContent.description) { $manifestContent.description } else { "" }
                family = if ($manifestContent.family) { $manifestContent.family } else { "custom" }
                preview = if ($manifestContent.preview) { $manifestContent.preview } else { "preview.png" }
                path = $relativeDir
            }
            $pluginList += $entry
            Write-Host "  [+] Registered: $($entry.name) ($($entry.id))" -ForegroundColor Green
        } catch {
            Write-Host "  [!] Error parsing manifest in $($dir.Name): $_" -ForegroundColor Red
        }
    }
}

$indexObject = [ordered]@{
    version = "1.0.0"
    updatedAt = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    plugins = $pluginList
}

$jsonOutput = $indexObject | ConvertTo-Json -Depth 4
[System.IO.File]::WriteAllText($outputFile, $jsonOutput, [System.Text.Encoding]::UTF8)

Write-Host "`nPlugin index updated with $($pluginList.Count) plugin(s) at: $outputFile" -ForegroundColor Cyan
