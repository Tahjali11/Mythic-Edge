param(
    [switch]$Coverage
)

$ErrorActionPreference = "Stop"
$CoverageFloorPercent = "85"
$CoverageRunId = "run_repo_checks"
$CoverageRoot = "_review_/quality_coverage_global_line_floor/$CoverageRunId"
$CoverageXml = "$CoverageRoot/coverage.xml"

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Label,
        [Parameter(Mandatory = $true, ValueFromRemainingArguments = $true)]
        [string[]]$Command
    )

    Write-Host $Label
    & $Command[0] $Command[1..($Command.Count - 1)]
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE."
    }
}

if ($Coverage) {
    $env:COVERAGE_FILE = "$CoverageRoot/.coverage"
    try {
        Invoke-Checked "Running coverage test suite..." py -m pytest -q tests --cov=src/mythic_edge_parser --cov-report=term-missing "--cov-report=xml:$CoverageXml"
        Invoke-Checked "Checking global Python line coverage floor (85.00%; branch coverage advisory-only)..." py tools/check_coverage_floor.py --coverage-xml $CoverageXml --line-floor $CoverageFloorPercent --command-label "tools/run_repo_checks.ps1 -Coverage"
    } finally {
        Remove-Item Env:\COVERAGE_FILE -ErrorAction SilentlyContinue
    }
} else {
    Invoke-Checked "Running test suite..." py -m pytest -q tests
}

Invoke-Checked "Running lint checks..." py -m ruff check src tests tools
