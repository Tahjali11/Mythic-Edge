param(
    [switch]$Check,
    [switch]$Start,
    [switch]$NoOpen,
    [switch]$LogToConsole,
    [int]$BackendPort = 8765,
    [int]$FrontendPort = 5173,
    [string]$AppDataRoot
)

$ErrorActionPreference = "Stop"

if ($Check -and $Start) {
    throw "Choose either -Check or -Start, not both."
}

if (-not $Check -and -not $Start) {
    $Check = $true
}

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptRoot "..\..")
$command = if ($Start) { "start" } else { "check" }

$argsList = @(
    "tools\dev_app\dev_app_launcher.py",
    $command,
    "--repo-root",
    $repoRoot.Path,
    "--backend-port",
    "$BackendPort",
    "--frontend-port",
    "$FrontendPort"
)

if ($AppDataRoot) {
    $argsList += @("--app-data-root", $AppDataRoot)
}

if ($NoOpen) {
    $argsList += "--no-open"
}

if ($LogToConsole) {
    $argsList += "--log-to-console"
}

Push-Location $repoRoot
try {
    & py @argsList
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
