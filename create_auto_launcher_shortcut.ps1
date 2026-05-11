$desktop = [Environment]::GetFolderPath("Desktop")
$launcherRoot = Join-Path $PSScriptRoot "tools\auto_launcher"
$target = Join-Path $launcherRoot "run_manasight_launcher_auto.vbs"
$shortcutPath = Join-Path $desktop "Mythic Edge Launcher.lnk"

$wsh = New-Object -ComObject WScript.Shell
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $target
$shortcut.WorkingDirectory = $launcherRoot
$shortcut.Save()

Write-Host "Created shortcut at $shortcutPath"
