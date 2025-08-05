@echo off
REM FilePulse GUI Launcher for Windows

SET PYTHON_EXE=C:/Users/nyxzi/AppData/Local/Programs/Python/Python313/python.exe

echo 🚀 Launching FilePulse GUI...
echo.

%PYTHON_EXE% launch_gui.py

if errorlevel 1 (
    echo.
    echo ❌ Error launching GUI. Press any key to exit.
    pause >nul
) else (
    echo.
    echo 👋 FilePulse GUI closed.
)
