@echo off
echo Starting FilePulse Splash Screen Generator with Custom Backgrounds...
echo.
echo Features:
echo - Load custom background images
echo - Opacity, blur, and scale controls
echo - Gradient overlays
echo - Animation options
echo - Theme presets
echo - Code generation
echo.
echo Sample backgrounds available in demo\ folder
echo.
cd /d "%~dp0"
python tools\splash_generator.py
pause
