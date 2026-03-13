param(
    [ValidateSet("smoke", "single", "app")]
    [string]$Mode = "app",
    [string]$Source = "0",
    [string]$OutputDir = ".\\008_outputs\\smoke",
    [string]$ImagePath = ""
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$appRoot = Join-Path $repoRoot "screen_analyzer_v1"
$activateScript = Join-Path $appRoot ".venv\Scripts\Activate.ps1"

if (-not (Test-Path $activateScript)) {
    throw "Virtual environment not found. Run .\setup.ps1 first."
}

Set-Location $appRoot
& $activateScript

switch ($Mode) {
    "smoke" {
        python .\005_scripts\005.002_smoke_capture.py --source $Source --output-dir $OutputDir
    }
    "single" {
        if ([string]::IsNullOrWhiteSpace($ImagePath)) {
            throw "-ImagePath is required when -Mode single"
        }
        python .\005_scripts\005.001_single_frame_analysis.py --image $ImagePath
    }
    "app" {
        python .\001_app\002_app_entrypoint.py
    }
}
