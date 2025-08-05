@echo off
echo FilePulse GUI Launcher - Choose Your Style
echo =========================================
echo.
echo [1] Standard TTK Progress Bar
echo [2] Custom Canvas Animation  
echo [3] Simple Smooth Animation
echo [4] Ultra Simple Animation
echo [5] Transparent Bottom Fade (Modern!)
echo [6] No Splash (Direct Launch)
echo.
set /p choice="Choose (1-6): "

cd /d "%~dp0"

if "%choice%"=="1" (
    echo Starting with TTK progress bar...
    python launch_gui_with_splash.py
) else if "%choice%"=="2" (
    echo Starting with custom canvas animation...
    python launch_gui_animated.py
) else if "%choice%"=="3" (
    echo Starting with simple smooth animation...
    python launch_gui_simple_animated.py
) else if "%choice%"=="4" (
    echo Starting with ultra simple animation...
    python launch_gui_ultra_simple.py
) else if "%choice%"=="5" (
    echo Starting with transparent bottom fade...
    python launch_gui_transparent.py
) else if "%choice%"=="6" (
    echo Starting GUI directly...
    python launch_gui.py
) else (
    echo Invalid choice. Using transparent fade (modern look)...
    python launch_gui_transparent.py
)

if errorlevel 1 (
    echo.
    echo Launch failed. Trying direct GUI...
    python launch_gui.py
)

echo.
pause
