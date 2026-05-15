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

Invoke-Checked "Running agent docs checks..." py tools\check_agent_docs.py
Invoke-Checked "Running content secret checks..." py tools\check_secret_patterns.py --all
Invoke-Checked "Running clean-clone local artifact check..." py tools\check_local_environment.py --profile clean_clone
Invoke-Checked "Running workbook state probe..." py tools\report_workbook_state.py
Invoke-Checked "Running lint checks..." py -m ruff check src tests tools
