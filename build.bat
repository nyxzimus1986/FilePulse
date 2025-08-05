@echo off
REM FilePulse Build Script for Windows
REM This script builds standalone executables for both CLI and GUI versions

echo ========================================
echo FilePulse Executable Build Script
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Installing build dependencies...
pip install -r requirements-build.txt
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to install build dependencies
    pause
    exit /b 1
)

echo.
echo Building executables...
echo This may take several minutes...
echo.

REM Clean previous builds
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

REM Build both executables
echo Building FilePulse GUI and CLI...
pyinstaller filepulse.spec --clean --noconfirm
if %ERRORLEVEL% neq 0 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Executables created in:
echo   GUI: dist\FilePulse-GUI\FilePulse.exe
echo   CLI: dist\FilePulse-CLI\filepulse-cli.exe
echo.

REM Test the executables
echo Testing executables...
echo.
echo Testing CLI version:
"dist\FilePulse-CLI\filepulse-cli.exe" --version
if %ERRORLEVEL% neq 0 (
    echo WARNING: CLI executable test failed
) else (
    echo CLI executable working correctly
)

echo.
echo Testing GUI version (will open briefly):
start "" "dist\FilePulse-GUI\FilePulse.exe"
timeout /t 3 >nul
taskkill /im FilePulse.exe /f >nul 2>&1
echo GUI executable test completed

echo.
echo ========================================
echo Build Summary:
echo ========================================
dir /b dist
echo.
echo To run FilePulse:
echo   GUI: Double-click dist\FilePulse-GUI\FilePulse.exe
echo   CLI: Run dist\FilePulse-CLI\filepulse-cli.exe from command line
echo.
echo You can copy these folders to any Windows machine to run FilePulse
echo without requiring Python installation.
echo.
pause
