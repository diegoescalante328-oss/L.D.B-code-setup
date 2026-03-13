$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$appRoot = Join-Path $repoRoot "screen_analyzer_v1"
$activateScript = Join-Path $appRoot ".venv\Scripts\Activate.ps1"

if (-not (Test-Path $activateScript)) {
    throw "Virtual environment not found. Run .\setup.ps1 first."
}

Set-Location $appRoot
& $activateScript
python -m pytest .\006_tests -q
