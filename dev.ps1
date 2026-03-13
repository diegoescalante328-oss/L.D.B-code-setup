$ErrorActionPreference = "Stop"

Write-Host "[dev] Running tests via test.ps1"
& (Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) "test.ps1")
