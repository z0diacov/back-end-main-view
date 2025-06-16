@echo off
setlocal

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

cd /d "%PROJECT_ROOT%"

set VENV_PATH=%PROJECT_ROOT%\venv
if not exist "%VENV_PATH%" (
    python -m venv "%VENV_PATH%"
)

call "%VENV_PATH%\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment
    exit /b 1
)

set REQUIREMENTS_PATH=%PROJECT_ROOT%\requirements.txt
if not exist "%REQUIREMENTS_PATH%" (
    echo requirements.txt file is missing
    exit /b 1
)

pip install -r "%REQUIREMENTS_PATH%"

cmd /k