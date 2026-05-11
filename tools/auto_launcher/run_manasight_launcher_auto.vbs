Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run Chr(34) & scriptDir & "\run_manasight_launcher_auto.bat" & Chr(34), 0, False
