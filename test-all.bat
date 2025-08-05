@echo off
echo ========================================
echo FilePulse Executable Test Suite
echo ========================================
echo.

echo Available Executables:
dir dist\*.exe /B
echo.

echo Testing GUI Version (No Console)...
echo This should open the GUI without showing a console window.
echo.
echo Starting FilePulse-NoConsole.exe...
start "" "dist\FilePulse-NoConsole.exe"

echo.
echo GUI should now be running in the background.
echo Check your taskbar for the FilePulse window.
echo.

echo Testing CLI Version...
echo This will show the CLI help and version info.
echo.
pause

echo.
echo CLI Version Help:
dist\FilePulse-CLI-Simple.exe --help

echo.
echo ========================================
echo Test Summary:
echo ========================================
echo.
echo FilePulse-NoConsole.exe    - GUI without console (recommended)
echo FilePulse-CLI-Simple.exe   - CLI with error handling
echo.
echo All executables are completely standalone!
echo No Python installation required.
echo.
pause
