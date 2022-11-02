@echo off
cmd /c powershell -Nop -NonI -Nologo -WindowStyle Hidden "Write-Host"
"venv/Scripts/pythonw.exe" "BasicToDoList.py"
