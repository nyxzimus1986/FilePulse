@echo off
echo Building FilePulse with custom design tools...
cd /d "%~dp0"

REM Check if custom icon exists
set ICON_PATH=assets\icons\filepulse-icon.ico
if not exist "%ICON_PATH%" (
    echo No custom icon found at %ICON_PATH%
    echo Using default icon...
    set ICON_ARG=
) else (
    echo Using custom icon: %ICON_PATH%
    set ICON_ARG=--icon=%ICON_PATH%
)

echo.
echo [1/4] Building standard CLI version...
pyinstaller --onefile --name=FilePulse-CLI filepulse\cli.py --hidden-import=watchdog.observers.polling --hidden-import=yaml --distpath=dist --workpath=build --clean %ICON_ARG%

echo.
echo [2/4] Building GUI version with splash screen...
pyinstaller --onefile --windowed --name=FilePulse-GUI gui_final.py --hidden-import=tkinter --hidden-import=watchdog.observers.polling --hidden-import=yaml --hidden-import=PIL --distpath=dist --workpath=build --clean %ICON_ARG%

echo.
echo [3/4] Building Icon Generator...
pyinstaller --onefile --windowed --name=FilePulse-IconGenerator tools\icon_generator.py --hidden-import=tkinter --hidden-import=PIL --distpath=dist --workpath=build --clean %ICON_ARG%

echo.
echo [4/4] Building Splash Generator...
pyinstaller --onefile --windowed --name=FilePulse-SplashGenerator tools\splash_generator.py --hidden-import=tkinter --hidden-import=PIL --distpath=dist --workpath=build --clean %ICON_ARG%

echo.
echo Build complete! Generated executables:
echo   - FilePulse-CLI.exe (Command line version)
echo   - FilePulse-GUI.exe (GUI with splash screen)
echo   - FilePulse-IconGenerator.exe (Icon design tool)
echo   - FilePulse-SplashGenerator.exe (Splash screen design tool)
echo.
echo Assets directory structure:
echo   assets\icons\      - Generated application icons
echo   assets\splash\     - Generated splash screens and code
echo   assets\presets\    - Saved design presets
echo.
echo All files are in the dist\ directory.

pause
