' CURIO Bot Silent Launcher (Zero console window)
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.Run "python """ & scriptDir & "\curio_discord_bot.py""", 0, False
