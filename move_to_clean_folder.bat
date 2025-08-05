@echo off
REM Batch script to move all required FilePulse files to a new clean folder

set NEWDIR=%~dp0FilePulseApp

REM Create the new directory
if not exist "%NEWDIR%" mkdir "%NEWDIR%"
if not exist "%NEWDIR%\filepulse" mkdir "%NEWDIR%\filepulse"
if not exist "%NEWDIR%\assets" mkdir "%NEWDIR%\assets"
if not exist "%NEWDIR%\assets\splash" mkdir "%NEWDIR%\assets\splash"
if not exist "%NEWDIR%\assets\presets" mkdir "%NEWDIR%\assets\presets"

REM Copy main files
copy /Y "%~dp0filepulse.py" "%NEWDIR%\filepulse.py"
copy /Y "%~dp0run_filepulse.bat" "%NEWDIR%\run_filepulse.bat"

REM Copy all .py files from filepulse folder
xcopy /Y /S /I "%~dp0filepulse\*.py" "%NEWDIR%\filepulse\"

REM Copy splash and preset assets if they exist
xcopy /Y /S /I "%~dp0assets\splash\*.*" "%NEWDIR%\assets\splash\"
xcopy /Y /S /I "%~dp0assets\presets\*.*" "%NEWDIR%\assets\presets\"

REM Copy icon if it exists
if exist "%~dp0assets\icon.ico" copy /Y "%~dp0assets\icon.ico" "%NEWDIR%\assets\icon.ico"

REM Done
@echo.
@echo All required files have been moved to %NEWDIR%
@echo You can now run FilePulse from the new folder.
pause
