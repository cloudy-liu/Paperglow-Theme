param(
    [string]$ThemePath = "$PSScriptRoot\claude.css",
    [string]$ReadmePath = "$PSScriptRoot\README.md"
)

$css = Get-Content -Raw -Path $ThemePath
$readme = Get-Content -Raw -Path $ReadmePath

$missing = New-Object System.Collections.Generic.List[string]

$requiredCssTokens = @(
    "#top-titlebar",
    ".megamenu-opened header",
    ".toolbar-icon.btn",
    ".ty-app-title"
)

foreach ($token in $requiredCssTokens) {
    if (-not $css.Contains($token)) {
        $missing.Add("CSS token missing: $token")
    }
}

if (-not $readme.Contains("Unibody")) {
    $missing.Add("README is missing Windows Unibody guidance")
}

if ($missing.Count -gt 0) {
    Write-Error ($missing -join [Environment]::NewLine)
    exit 1
}

Write-Host "Windows Unibody theme coverage checks passed."
