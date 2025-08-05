@echo off
echo ======================================
echo Starting FilePulse Application
echo ======================================
cd /d "%~dp0"
echo Current directory: %CD%
echo Running: python filepulse_launcher.py
python filepulse_launcher.py
echo ======================================
echo FilePulse finished with exit code: %ERRORLEVEL%
echo ======================================
pause
