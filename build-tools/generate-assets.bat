@echo off
echo Generating default FilePulse assets...
cd /d "%~dp0"
python generate-assets.py
pause
