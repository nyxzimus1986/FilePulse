@echo off
echo Starting FilePulse Icon Generator with Custom Image Support...
echo.
echo Features:
echo - Load your own images (PNG, JPG, GIF, etc.)
echo - Adjust opacity and scale  
echo - Multiple icon styles
echo - Text overlays
echo - Color customization
echo.
echo Sample images available in demo\ folder
echo.
cd /d "%~dp0"
python tools\icon_generator.py
pause
