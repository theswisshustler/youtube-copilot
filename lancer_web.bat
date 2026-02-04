@echo off
chcp 65001 >nul
echo ====================================
echo   Generateur de Titres YouTube
echo   Interface Web
echo ====================================
echo.
cd /d "%~dp0"
call venv\Scripts\activate.bat
echo Installation de Streamlit si necessaire...
pip install streamlit>=1.32.0 -q
echo.
echo Lancement de l'interface web...
echo L'application va s'ouvrir dans votre navigateur.
echo.
streamlit run app_web.py
pause
