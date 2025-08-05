@echo off
REM FilePulse Monitor Launcher for Windows
REM Usage: monitor.bat [path] [options]

SET PYTHON_EXE=C:/Users/nyxzi/AppData/Local/Programs/Python/Python313/python.exe
SET CLI_CMD=import sys; sys.path.insert(0, '.'); from filepulse.cli import main; main()

echo FilePulse Filesystem Monitor
echo ==============================

if "%1"=="" (
    echo Monitoring current directory...
    %PYTHON_EXE% -c "%CLI_CMD%" monitor . --stats
) else if "%1"=="help" (
    %PYTHON_EXE% -c "%CLI_CMD%" --help
) else if "%1"=="test" (
    echo Running tests...
    %PYTHON_EXE% test_filepulse.py
) else if "%1"=="config" (
    echo Creating default config...
    %PYTHON_EXE% -c "%CLI_CMD%" init-config filepulse.yaml
    echo Config created: filepulse.yaml
) else (
    echo Monitoring path: %1
    %PYTHON_EXE% -c "%CLI_CMD%" monitor %1 --stats
)

pause
