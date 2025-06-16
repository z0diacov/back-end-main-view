$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path $ScriptDir -Parent

$VenvPath = Join-Path $ProjectRoot "venv"

if (-Not (Test-Path $VenvPath)) {
    python -m venv $VenvPath
}

$ActivatePath = Join-Path $VenvPath "Scripts/Activate.ps1"
if (-Not (Test-Path $ActivatePath)) {
    Write-Error "Failed to find the virtual environment"
    exit 1
}
. $ActivatePath

$RequirementsPath = Join-Path $ProjectRoot "requirements.txt"
if (-Not (Test-Path $RequirementsPath)) {
    Write-Error "requirements.txt file is missing"
    exit 1
}

pip install -r $RequirementsPath

