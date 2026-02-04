' Script VBS pour créer un raccourci sur le bureau
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = oWS.SpecialFolders("Desktop") & "\Générateur Titres YouTube.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)

' Chemin du script à lancer
scriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
oLink.TargetPath = scriptDir & "\lancer_web.bat"
oLink.WorkingDirectory = scriptDir
oLink.Description = "Générateur de titres YouTube avec IA"
oLink.IconLocation = "C:\Windows\System32\shell32.dll,165"
oLink.Save

MsgBox "Raccourci créé sur votre bureau !" & vbCrLf & vbCrLf & "Nom: Générateur Titres YouTube", vbInformation, "Succès"
