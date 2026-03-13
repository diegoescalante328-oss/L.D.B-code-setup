# Screen Analyzer V1 (Windows PowerShell-first workspace)

This repository is structured for **Windows 10/11 + PowerShell** as the primary development environment.

The runnable application lives in `screen_analyzer_v1/`.

## Windows PowerShell Quick Start

```powershell
# From the repository root
Set-Location .\screen_analyzer_v1

# Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Set required API key for this PowerShell session
$env:OPENAI_API_KEY = "your_key_here"

# Validate camera connectivity
python .\005_scripts\005.002_smoke_capture.py --source 0 --output-dir .\008_outputs\smoke

# Run the desktop app
python .\001_app\002_app_entrypoint.py
```

If script execution is blocked, run this once in PowerShell:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## Canonical docs
- Primary runtime README: `screen_analyzer_v1/README.md`
- Setup and run details: `screen_analyzer_v1/007_docs/007.004_setup_and_run.md`
- Environment setup: `screen_analyzer_v1/011_env/011.001_virtual_environment_setup.md`

## PowerShell automation scripts (repo root)
- `./setup.ps1` - create venv, install dependencies, and print next steps
- `./run.ps1` - run smoke test, single-frame analysis, or full app
- `./dev.ps1` - lint/test workflow helper
- `./test.ps1` - run automated tests
