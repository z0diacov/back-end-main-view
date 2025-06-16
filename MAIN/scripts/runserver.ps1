$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path $ScriptDir -Parent

Set-Location -Path $ProjectRoot

$VenvPath = Join-Path $ProjectRoot "venv"
if (-Not (Test-Path $VenvPath)) {
    python -m venv $VenvPath
}

$ActivatePath = Join-Path $VenvPath "Scripts/Activate.ps1"
if (-Not (Test-Path $ActivatePath)) {
    Write-Error "Virtual environment not found"
    exit 1
}
. $ActivatePath

$RequirementsPath = Join-Path $ProjectRoot "requirements.txt"
if (-Not (Test-Path $RequirementsPath)) {
    Write-Error "requirements.txt file is missing"
    exit 1
}

pip install -r $RequirementsPath

$env:PYTHONPATH = $ProjectRoot

uvicorn main:app --reload