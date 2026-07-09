$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"

if (Test-Path $venvPython) {
    & $venvPython (Join-Path $PSScriptRoot "dictate.py") @args
} else {
    python (Join-Path $PSScriptRoot "dictate.py") @args
}
