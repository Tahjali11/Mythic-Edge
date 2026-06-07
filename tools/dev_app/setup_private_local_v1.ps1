param(
    [switch]$Check,
    [switch]$Install,
    [switch]$Proof,
    [switch]$ExistingCheckout,
    [switch]$InitializeSqlite,
    [switch]$NoOpen,
    [switch]$LeaveRunning,
    [switch]$StopAfterVerify,
    [switch]$JsonReport,
    [string]$InstallRoot,
    [string]$SourceCheckout,
    [string]$RepoUrl,
    [string]$ReleaseRef,
    [int]$BackendPort = 8765,
    [int]$FrontendPort = 5173
)

$ErrorActionPreference = "Stop"

$selectedModes = @($Check, $Install, $Proof) | Where-Object { $_ }
if ($selectedModes.Count -gt 1) {
    throw "Choose only one of -Check, -Install, or -Proof."
}

if (-not $Check -and -not $Install -and -not $Proof) {
    $Check = $true
}

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptRoot "..\..")

$argsList = @("tools\dev_app\private_local_v1_setup.py")

if ($Proof) {
    $argsList += "--proof"
}
elseif ($Install) {
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

if ($RepoUrl) {
    $argsList += @("--repo-url", $RepoUrl)
}

if ($ReleaseRef) {
    $argsList += @("--release-ref", $ReleaseRef)
}

if ($NoOpen) {
    $argsList += "--no-open"
}

if ($LeaveRunning) {
    $argsList += "--leave-running"
}

if ($StopAfterVerify) {
    $argsList += "--stop-after-verify"
}

$argsList += @("--backend-port", "$BackendPort", "--frontend-port", "$FrontendPort")

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
