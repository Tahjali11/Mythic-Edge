param(
    [switch]$Coverage
)

$ErrorActionPreference = "Stop"

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
    Invoke-Checked "Running coverage test suite..." py -m pytest --cov=src/mythic_edge_parser --cov-report=term-missing tests
} else {
    Invoke-Checked "Running test suite..." py -m pytest -q tests
}

Invoke-Checked "Running lint checks..." py -m ruff check src tests
