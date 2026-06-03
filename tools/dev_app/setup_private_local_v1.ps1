param(
    [switch]$Check,
    [switch]$Install,
    [switch]$ExistingCheckout,
    [switch]$InitializeSqlite,
    [switch]$JsonReport,
    [string]$InstallRoot,
    [string]$SourceCheckout
)

$ErrorActionPreference = "Stop"

if ($Check -and $Install) {
    throw "Choose either -Check or -Install, not both."
}

if (-not $Check -and -not $Install) {
    $Check = $true
}

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptRoot "..\..")

$argsList = @("tools\dev_app\private_local_v1_setup.py")

if ($Install) {
    $argsList += "--install"
}
else {
    $argsList += "--check"
}

if ($ExistingCheckout) {
    $argsList += "--existing-checkout"
}

$source = if ($SourceCheckout) { $SourceCheckout } else { $repoRoot.Path }
$argsList += @("--source-checkout", $source)

if ($InstallRoot) {
    $argsList += @("--install-root", $InstallRoot)
}

if ($InitializeSqlite) {
    $argsList += "--initialize-sqlite"
}

if ($JsonReport) {
    $argsList += "--json-report"
}

Push-Location $repoRoot
try {
    & py @argsList
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
