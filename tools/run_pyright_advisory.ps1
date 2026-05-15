param(
    [string]$Project = "pyrightconfig.json"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command pyright -ErrorAction SilentlyContinue)) {
    throw "pyright is not installed or not on PATH."
}

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw "The Python launcher 'py' is not installed or not on PATH."
}

$pythonPath = (& py -c "import sys; print(sys.executable)").Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($pythonPath)) {
    throw "Could not resolve the active Python interpreter through the py launcher."
}

Write-Host "Running Pyright advisory check with Python interpreter: $pythonPath"
& pyright --project $Project --pythonpath $pythonPath
if ($LASTEXITCODE -ne 0) {
    throw "Pyright advisory check reported findings with exit code $LASTEXITCODE."
}
