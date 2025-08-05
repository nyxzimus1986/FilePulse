@echo off
REM FilePulse Complete Build Script with Splash Screen
REM Creates all executable versions

echo ==========================================
echo FilePulse Complete Build Suite
echo ==========================================
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo.
echo Building FilePulse executables...
echo This will create multiple versions for different use cases.
echo.

REM 1. Main GUI with Advanced Splash Screen (Recommended)
echo [1/3] Building main GUI with splash screen...
C:/Users/nyxzi/AppData/Local/Programs/Python/Python313/python.exe -m PyInstaller ^
    --onefile ^
    --noconsole ^
    --name "FilePulse" ^
    --add-data "config/default.yaml;config" ^
    --hidden-import "filepulse.advanced_splash" ^
    --hidden-import "filepulse.splash" ^
    --hidden-import "filepulse.config" ^
    --hidden-import "filepulse.monitor" ^
    --hidden-import "filepulse.events" ^
    --hidden-import "filepulse.output" ^
    --hidden-import "filepulse.utils" ^
    --hidden-import "filepulse.system_monitor" ^
    --hidden-import "tkinter" ^
    --hidden-import "tkinter.ttk" ^
    gui_final.py

echo.

REM 2. CLI Version
echo [2/3] Building CLI version...
C:/Users/nyxzi/AppData/Local/Programs/Python/Python313/python.exe -m PyInstaller ^
    --onefile ^
    --console ^
    --name "filepulse-cli" ^
    --add-data "config/default.yaml;config" ^
    --hidden-import "filepulse.config" ^
    --hidden-import "filepulse.monitor" ^
    --hidden-import "filepulse.events" ^
    --hidden-import "filepulse.output" ^
    --hidden-import "filepulse.utils" ^
    cli_simple.py

echo.

REM 3. Simple GUI without splash (fallback)
echo [3/3] Building simple GUI (no splash)...
C:/Users/nyxzi/AppData/Local/Programs/Python/Python313/python.exe -m PyInstaller ^
    --onefile ^
    --noconsole ^
    --name "FilePulse-Simple" ^
    --add-data "config/default.yaml;config" ^
    --hidden-import "filepulse.config" ^
    --hidden-import "filepulse.monitor" ^
    --hidden-import "filepulse.events" ^
    --hidden-import "filepulse.output" ^
    --hidden-import "filepulse.utils" ^
    --hidden-import "tkinter" ^
    gui_noconsole.py

echo.
echo ==========================================
echo Build Complete!
echo ==========================================
echo.

dir dist

echo.
echo ==========================================
echo FilePulse Executable Suite:
echo ==========================================
echo.
echo FilePulse.exe          - Main GUI with splash screen (RECOMMENDED)
echo FilePulse-Simple.exe   - Simple GUI without splash (fallback)
echo filepulse-cli.exe      - Command-line interface
echo.
echo Features:
echo ✓ Completely standalone - no Python required
echo ✓ Professional splash screen with loading animation
echo ✓ Advanced GUI with real-time monitoring
echo ✓ CLI for automation and scripting
echo ✓ Small file sizes (7-11 MB each)
echo.
echo Ready for distribution!
echo.
pause
