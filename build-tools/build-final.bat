@echo off
REM Final FilePulse Standalone Executable Builder
REM This creates working standalone .exe files

echo ==========================================
echo FilePulse Standalone Executable Builder
echo ==========================================
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo Building CLI executable...
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
    --hidden-import "watchdog.observers" ^
    --hidden-import "watchdog.events" ^
    cli_entry.py

echo.  
echo Building GUI executable...
C:/Users/nyxzi/AppData/Local/Programs/Python/Python313/python.exe -m PyInstaller ^
    --onefile ^
    --noconsole ^
    --name "FilePulse" ^
    --add-data "config/default.yaml;config" ^
    --hidden-import "filepulse.config" ^
    --hidden-import "filepulse.monitor" ^
    --hidden-import "filepulse.events" ^
    --hidden-import "filepulse.output" ^
    --hidden-import "filepulse.utils" ^
    --hidden-import "filepulse.system_monitor" ^
    --hidden-import "watchdog.observers" ^
    --hidden-import "watchdog.events" ^
    --hidden-import "tkinter" ^
    --hidden-import "tkinter.ttk" ^
    --hidden-import "tkinter.filedialog" ^
    --hidden-import "tkinter.messagebox" ^
    --hidden-import "tkinter.scrolledtext" ^
    gui_entry.py

echo.
echo ==========================================
echo Build Complete!
echo ==========================================
echo.

dir dist

echo.
echo Testing CLI executable...
echo.
dist\filepulse-cli.exe --version

echo.
echo Files created:
echo   CLI: dist\filepulse-cli.exe
echo   GUI: dist\FilePulse.exe
echo.
echo These are completely standalone executables!
echo No Python installation required on target machines.
echo.
pause
