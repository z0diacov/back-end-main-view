$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path $ScriptDir -Parent

$env:PYTHONPATH = $ProjectRoot  

Set-Location -Path $ProjectRoot  

pytest -s tests/steps/$args