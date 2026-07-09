@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%.."
set "VENV_PYTHON=%REPO_ROOT%\.venv\Scripts\python.exe"

if exist "%VENV_PYTHON%" (
    "%VENV_PYTHON%" "%SCRIPT_DIR%dictate.py" %*
) else (
    python "%SCRIPT_DIR%dictate.py" %*
)

endlocal
