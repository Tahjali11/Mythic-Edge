param(
    [Parameter(Mandatory = $true, ValueFromRemainingArguments = $true)]
    [string[]]$Paths
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command ruff -ErrorAction SilentlyContinue)) {
    throw "ruff is not installed or not on PATH."
}

$pythonPaths = New-Object System.Collections.Generic.List[string]

foreach ($path in $Paths) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        Write-Warning "Skipping missing path: $path"
        continue
    }

    $extension = [System.IO.Path]::GetExtension($path).ToLowerInvariant()
    if ($extension -notin @(".py", ".pyi")) {
        Write-Host "Skipping non-Python file: $path"
        continue
    }

    $resolved = (Resolve-Path -LiteralPath $path).Path
    if ($pythonPaths -notcontains $resolved) {
        $pythonPaths.Add($resolved)
    }
}

if ($pythonPaths.Count -eq 0) {
    Write-Host "No Python files to lint."
    exit 0
}

Write-Host "Running ruff on touched Python files..."
& ruff check --force-exclude @pythonPaths
