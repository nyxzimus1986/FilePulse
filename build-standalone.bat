@echo off
REM Quick Build Script for FilePulse Standalone Executables

echo ========================================
echo Building FilePulse Standalone Executables
echo ========================================
echo.

REM Clean previous builds
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo Building GUI version...
C:/Users/nyxzi/AppData/Local/Programs/Python/Python313/python.exe -m PyInstaller --onefile --noconsole --name FilePulse filepulse/gui.py

echo.
echo Building CLI version...
C:/Users/nyxzi/AppData/Local/Programs/Python/Python313/python.exe -m PyInstaller --onefile --console --name filepulse-cli filepulse/cli.py

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.

dir dist

echo.
echo Files created:
echo   GUI: dist\FilePulse.exe (no console window)
echo   CLI: dist\filepulse-cli.exe (with console)
echo.
echo These are completely standalone - no Python required!
echo Copy to any Windows machine and run directly.
echo.
pause
