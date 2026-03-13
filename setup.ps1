param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$appRoot = Join-Path $repoRoot "screen_analyzer_v1"

if (-not (Test-Path $appRoot)) {
    throw "screen_analyzer_v1 directory not found. Run this script from the repository root."
}

Set-Location $appRoot

Write-Host "[setup] Creating virtual environment..."
& $Python -m venv .venv

$activateScript = Join-Path $appRoot ".venv\Scripts\Activate.ps1"
if (-not (Test-Path $activateScript)) {
    throw "Activation script not found at $activateScript"
}

Write-Host "[setup] Installing dependencies..."
& $activateScript
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "[setup] Complete."
Write-Host "Next steps:"
Write-Host "  1) Set API key: `$env:OPENAI_API_KEY = 'your_key_here'"
Write-Host "  2) Run app:    .\run.ps1 -Mode app"
