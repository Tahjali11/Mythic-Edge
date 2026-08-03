[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$CharacterizationId,

    [Parameter(Mandatory = $true)]
    [string]$OwnerDecisionRef
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ContractSha256 = '7c7d5cd414b8a893703b014d470b84800b3444a11fe498135a7dd965adeacb69'
$ContractReviewSha256 = 'ceac5499f7d281e99cefea69a4684debc6d86b5bc50fb29dff1eae25fca971f5'
$ControllerSha256 = '2d0e793cf741cba42be4505cae0f0ddcd7b9e6927362dd60696570d84e7324ef'
$BootstrapRelativePath = 'tools\start_role_pool_r0_direct_interpreter_identity_characterizer_secure_ingress.ps1'
# SHA-256 of this UTF-8 source after LF normalization and replacing only this value with 64 zeros.
$BootstrapSourceIdentitySha256 = '3cbd073c2ed5034fbc543ee4d15fb79729eb063e164f536342a735d4e630062a'
$CharacterizationIdPattern = '^r0_direct_interpreter_identity_characterization_v1_[0-9a-f]{32}$'
$OwnerDecisionRefPattern = '^https://github\.com/Tahjali11/Mythic-Edge/issues/795#issuecomment-[1-9][0-9]{0,19}$'
$ControllerRelativePath = 'tools\run_role_pool_r0_direct_interpreter_identity_characterizer_secure_ingress.py'
$ControllerReadinessArguments = @(
    '-I',
    '-B',
    $ControllerRelativePath,
    '--characterization-id',
    $CharacterizationId,
    '--owner-decision-ref',
    $OwnerDecisionRef
)
$LaunchReadinessLine = 'R0 secure launch ingress ready; consume authority, then press Enter.'
$FailureLine = 'R0 secure launch ingress failed.'

function Test-OrdinaryNonReparseFile {
    param([Parameter(Mandatory = $true)][string]$Path)

    try {
        $item = Get-Item -LiteralPath $Path -Force -ErrorAction Stop
        return (
            $item -is [System.IO.FileInfo] -and
            -not [bool]($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)
        )
    }
    catch {
        return $false
    }
}

function Test-OrdinaryNonReparseDirectory {
    param([Parameter(Mandatory = $true)][string]$Path)

    try {
        $item = Get-Item -LiteralPath $Path -Force -ErrorAction Stop
        return (
            $item -is [System.IO.DirectoryInfo] -and
            -not [bool]($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)
        )
    }
    catch {
        return $false
    }
}

function Test-ExactSha256 {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Expected
    )

    if (-not (Test-OrdinaryNonReparseFile -Path $Path)) {
        return $false
    }
    try {
        $actual = (Get-FileHash -LiteralPath $Path -Algorithm SHA256 -ErrorAction Stop).Hash.ToLowerInvariant()
        return $actual -ceq $Expected
    }
    catch {
        return $false
    }
}

function Test-ExactBootstrapSourceIdentity {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Expected
    )

    if (
        $Expected -cnotmatch '^[0-9a-f]{64}$' -or
        -not (Test-OrdinaryNonReparseFile -Path $Path)
    ) {
        return $false
    }

    $source = $null
    $normalized = $null
    $bytes = $null
    $sha256 = $null
    try {
        $utf8 = [System.Text.UTF8Encoding]::new($false, $true)
        $source = [System.IO.File]::ReadAllText($Path, $utf8)
        $source = $source.Replace("`r`n", "`n").Replace("`r", "`n")
        $assignment = '$BootstrapSourceIdentitySha256 = ''' + $Expected + ''''
        $placeholder = '$BootstrapSourceIdentitySha256 = ''' + ('0' * 64) + ''''
        $index = $source.IndexOf($assignment, [System.StringComparison]::Ordinal)
        if (
            $index -lt 0 -or
            $source.IndexOf(
                $assignment,
                $index + $assignment.Length,
                [System.StringComparison]::Ordinal
            ) -ge 0
        ) {
            return $false
        }

        $normalized = (
            $source.Substring(0, $index) +
            $placeholder +
            $source.Substring($index + $assignment.Length)
        )
        $bytes = $utf8.GetBytes($normalized)
        $sha256 = [System.Security.Cryptography.SHA256]::Create()
        $actual = [System.BitConverter]::ToString($sha256.ComputeHash($bytes)).Replace('-', '').ToLowerInvariant()
        return $actual -ceq $Expected
    }
    catch {
        return $false
    }
    finally {
        if ($sha256 -ne $null) {
            $sha256.Dispose()
        }
        if ($bytes -ne $null) {
            [System.Array]::Clear($bytes, 0, $bytes.Length)
        }
        $bytes = $null
        $normalized = $null
        $source = $null
    }
}

function Test-PublicToken {
    param(
        [Parameter(Mandatory = $true)][string]$Value,
        [Parameter(Mandatory = $true)][string]$Pattern
    )

    if ($Value -cnotmatch $Pattern) {
        return $false
    }
    foreach ($character in $Value.ToCharArray()) {
        $code = [int][char]$character
        if ($code -lt 0x21 -or $code -gt 0x7e) {
            return $false
        }
    }
    return $true
}

function Read-InterceptedKey {
    return [Console]::ReadKey($true)
}

function Wait-ForConsumedConfirmation {
    $timer = [System.Diagnostics.Stopwatch]::StartNew()
    try {
        while ($timer.Elapsed.TotalSeconds -lt 600) {
            if (-not [Console]::KeyAvailable) {
                [System.Threading.Thread]::Sleep(25)
                continue
            }
            $key = Read-InterceptedKey
            return (
                $key.Key -eq [ConsoleKey]::Enter -and
                [int][char]$key.KeyChar -eq 13 -and
                $key.Modifiers -eq [ConsoleModifiers]0
            )
        }
        return $false
    }
    finally {
        $timer.Stop()
    }
}

function Read-PrivateLaunchImage {
    $timer = [System.Diagnostics.Stopwatch]::StartNew()
    $utf8 = [System.Text.UTF8Encoding]::new($false, $true)
    $scalars = [System.Collections.Generic.List[string]]::new()
    $pendingHighSurrogate = [char]0
    $hasPendingHighSurrogate = $false
    $polls = 0
    $reads = 0
    $utf8Length = 0
    try {
        while ($true) {
            if ($polls -ge 12001 -or $timer.Elapsed.TotalSeconds -ge 120) {
                throw [System.InvalidOperationException]::new()
            }
            $polls += 1
            if (-not [Console]::KeyAvailable) {
                [System.Threading.Thread]::Sleep(10)
                continue
            }
            if ($reads -ge 8192 -or $timer.Elapsed.TotalSeconds -ge 120) {
                throw [System.InvalidOperationException]::new()
            }
            $key = Read-InterceptedKey
            $reads += 1
            $character = [char]$key.KeyChar
            $code = [int]$character

            if ($character -eq [char]0 -or $character -eq [char]10) {
                throw [System.InvalidOperationException]::new()
            }
            if ($character -eq [char]13) {
                if ($key.Key -ne [ConsoleKey]::Enter -or $hasPendingHighSurrogate) {
                    throw [System.InvalidOperationException]::new()
                }
                break
            }
            if ($character -eq [char]8) {
                if ($key.Key -ne [ConsoleKey]::Backspace -or $hasPendingHighSurrogate) {
                    throw [System.InvalidOperationException]::new()
                }
                if ($scalars.Count -eq 0) {
                    throw [System.InvalidOperationException]::new()
                }
                $last = $scalars[$scalars.Count - 1]
                $utf8Length -= $utf8.GetByteCount($last)
                $scalars.RemoveAt($scalars.Count - 1)
                continue
            }
            if ([char]::IsHighSurrogate($character)) {
                if ($hasPendingHighSurrogate) {
                    throw [System.InvalidOperationException]::new()
                }
                $pendingHighSurrogate = $character
                $hasPendingHighSurrogate = $true
                continue
            }
            if ([char]::IsLowSurrogate($character)) {
                if (-not $hasPendingHighSurrogate) {
                    throw [System.InvalidOperationException]::new()
                }
                $scalar = [char]::ConvertFromUtf32(
                    [char]::ConvertToUtf32($pendingHighSurrogate, $character)
                )
                $pendingHighSurrogate = [char]0
                $hasPendingHighSurrogate = $false
            }
            else {
                if ($hasPendingHighSurrogate -or $code -lt 0x20 -or $code -eq 0x7f) {
                    throw [System.InvalidOperationException]::new()
                }
                $scalar = [string]$character
            }
            $scalarLength = $utf8.GetByteCount($scalar)
            if ($utf8Length + $scalarLength -gt 4095) {
                throw [System.InvalidOperationException]::new()
            }
            $scalars.Add($scalar)
            $utf8Length += $scalarLength
        }

        if ([Console]::KeyAvailable) {
            throw [System.InvalidOperationException]::new()
        }
        $value = [string]::Join('', $scalars.ToArray())
        if (
            [string]::IsNullOrEmpty($value) -or
            $value -cnotmatch '^[A-Za-z]:[\\/]' -or
            -not [System.IO.Path]::IsPathRooted($value) -or
            [System.IO.Path]::GetFileName($value) -cne 'python.exe' -or
            $value -match '(?i)(^|[\\/])windowsapps([\\/]|$)' -or
            $utf8.GetByteCount($value) -gt 4095
        ) {
            throw [System.InvalidOperationException]::new()
        }
        return $value
    }
    finally {
        $timer.Stop()
        $pendingHighSurrogate = [char]0
        for ($index = 0; $index -lt $scalars.Count; $index += 1) {
            $scalars[$index] = ([string][char]0) * $scalars[$index].Length
        }
        $scalars.Clear()
    }
}

function Get-EntryState {
    if (
        [Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT -or
        $PSVersionTable.PSEdition -cne 'Desktop' -or
        $PSVersionTable.PSVersion.Major -ne 5 -or
        [Console]::IsInputRedirected -or
        [Console]::IsOutputRedirected -or
        [Console]::IsErrorRedirected -or
        -not [Environment]::UserInteractive
    ) {
        throw [System.InvalidOperationException]::new()
    }
    if (-not (Test-PublicToken -Value $CharacterizationId -Pattern $CharacterizationIdPattern)) {
        throw [System.InvalidOperationException]::new()
    }
    if (-not (Test-PublicToken -Value $OwnerDecisionRef -Pattern $OwnerDecisionRefPattern)) {
        throw [System.InvalidOperationException]::new()
    }

    $repositoryRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
    $bootstrapPath = [System.IO.Path]::GetFullPath((Join-Path $repositoryRoot $BootstrapRelativePath))
    $controllerPath = [System.IO.Path]::GetFullPath((Join-Path $repositoryRoot $ControllerRelativePath))
    $contractPath = Join-Path $repositoryRoot 'docs\contracts\role_pool_trusted_owner_r0_direct_interpreter_identity_characterizer_secure_ingress_successor.md'
    $reviewPath = Join-Path $repositoryRoot 'docs\contract_test_reports\role_pool_trusted_owner_r0_direct_interpreter_identity_characterizer_secure_ingress_successor.md'
    if (
        -not (Test-OrdinaryNonReparseDirectory -Path $repositoryRoot) -or
        (Get-Location).Provider.Name -cne 'FileSystem' -or
        [System.IO.Path]::GetFullPath((Get-Location).Path) -cne $repositoryRoot -or
        -not (Test-OrdinaryNonReparseFile -Path $PSCommandPath) -or
        [System.IO.Path]::GetFullPath($PSCommandPath) -cne $bootstrapPath -or
        -not (Test-ExactBootstrapSourceIdentity -Path $bootstrapPath -Expected $BootstrapSourceIdentitySha256) -or
        -not (Test-ExactSha256 -Path $controllerPath -Expected $ControllerSha256) -or
        -not (Test-ExactSha256 -Path $contractPath -Expected $ContractSha256) -or
        -not (Test-ExactSha256 -Path $reviewPath -Expected $ContractReviewSha256)
    ) {
        throw [System.InvalidOperationException]::new()
    }
    if (
        [Diagnostics.ProcessStartInfo].GetProperty('Arguments') -eq $null -or
        [Diagnostics.ProcessStartInfo].GetProperty('FileName') -eq $null -or
        [Diagnostics.ProcessStartInfo].GetProperty('UseShellExecute') -eq $null -or
        [Diagnostics.ProcessStartInfo].GetProperty('WorkingDirectory') -eq $null -or
        [Diagnostics.Process].GetMethod('Start', [type[]]@([Diagnostics.ProcessStartInfo])) -eq $null -or
        [Console].GetProperty('KeyAvailable') -eq $null -or
        [Console].GetMethod('ReadKey', [type[]]@([bool])) -eq $null -or
        [Console]::KeyAvailable
    ) {
        throw [System.InvalidOperationException]::new()
    }

    $arguments = [string]::Join(' ', $ControllerReadinessArguments)
    if (
        $ControllerReadinessArguments.Count -ne 7 -or
        $arguments -cne (
            '-I -B tools\run_role_pool_r0_direct_interpreter_identity_characterizer_secure_ingress.py ' +
            '--characterization-id ' + $CharacterizationId +
            ' --owner-decision-ref ' + $OwnerDecisionRef
        ) -or
        ([System.Text.Encoding]::UTF8.GetByteCount($arguments) -gt 512)
    ) {
        throw [System.InvalidOperationException]::new()
    }
    return [pscustomobject]@{
        RepositoryRoot = $repositoryRoot
        Arguments = $arguments
    }
}

$process = $null
$startInfo = $null
$launchImage = $null
$exitCode = 2
try {
    $entry = Get-EntryState
    [Console]::WriteLine($LaunchReadinessLine)
    if (-not (Wait-ForConsumedConfirmation)) {
        throw [System.InvalidOperationException]::new()
    }
    if ([Console]::KeyAvailable) {
        throw [System.InvalidOperationException]::new()
    }
    $launchImage = Read-PrivateLaunchImage

    $startInfo = [Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = $launchImage
    $startInfo.Arguments = $entry.Arguments
    $startInfo.WorkingDirectory = $entry.RepositoryRoot
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $false
    $startInfo.RedirectStandardInput = $false
    $startInfo.RedirectStandardOutput = $false
    $startInfo.RedirectStandardError = $false
    $process = [Diagnostics.Process]::Start($startInfo)
    $startInfo.FileName = [string]::Empty
    $launchImage = $null
    if ($process -eq $null) {
        throw [System.InvalidOperationException]::new()
    }
    if (-not $process.WaitForExit(180000)) {
        try {
            $process.Kill()
            [void]$process.WaitForExit(5000)
        }
        catch {
        }
        throw [System.InvalidOperationException]::new()
    }
    $exitCode = $process.ExitCode
}
catch {
    if ($process -ne $null) {
        try {
            if (-not $process.HasExited) {
                $process.Kill()
                [void]$process.WaitForExit(5000)
            }
        }
        catch {
        }
    }
    [Console]::WriteLine($FailureLine)
    $exitCode = 2
}
finally {
    try {
        $launchImage = $null
        if ($startInfo -ne $null) {
            $startInfo.FileName = [string]::Empty
            $startInfo.Arguments = [string]::Empty
            $startInfo.WorkingDirectory = [string]::Empty
        }
        if ($process -ne $null) {
            $process.Dispose()
        }
    }
    catch {
        $exitCode = 2
    }
    $startInfo = $null
    $process = $null
}

exit $exitCode
