@echo off
chcp 65001 >nul
echo ====================================
echo   Installation de la commande
echo   youtube-titles
echo ====================================
echo.

REM Créer le script de commande
set INSTALL_DIR=%~dp0
set SCRIPT_PATH=%INSTALL_DIR%youtube-titles.bat

echo @echo off > "%SCRIPT_PATH%"
echo chcp 65001 ^>nul >> "%SCRIPT_PATH%"
echo cd /d "%INSTALL_DIR%" >> "%SCRIPT_PATH%"
echo call venv\Scripts\activate.bat >> "%SCRIPT_PATH%"
echo python main.py >> "%SCRIPT_PATH%"

echo Script cree: %SCRIPT_PATH%
echo.

REM Vérifier si le dossier est déjà dans le PATH
echo %PATH% | find /i "%INSTALL_DIR%" >nul
if %errorlevel% equ 0 (
    echo Le dossier est deja dans le PATH.
) else (
    echo Ajout au PATH systeme...
    setx PATH "%PATH%;%INSTALL_DIR%" >nul
    echo.
    echo IMPORTANT:
    echo - Fermez et rouvrez votre terminal
    echo - Ensuite tapez simplement: youtube-titles
)

echo.
echo ====================================
echo   Installation terminee!
echo ====================================
echo.
echo Pour utiliser:
echo 1. Fermez ce terminal
echo 2. Ouvrez un nouveau terminal
echo 3. Tapez: youtube-titles
echo.
pause
