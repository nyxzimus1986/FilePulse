@echo off
REM FilePulse System-Wide Monitor Launcher for Windows

SET PYTHON_EXE=C:/Users/nyxzi/AppData/Local/Programs/Python/Python313/python.exe
SET CLI_CMD=import sys; sys.path.insert(0, '.'); from filepulse.cli import main; main()

echo 🌐 FilePulse System-Wide Filesystem Monitor
echo ==========================================
echo.
echo This will monitor your:
echo   📂 Desktop
echo   📂 Documents  
echo   📂 Downloads
echo   📂 Pictures, Videos, Music
echo   📂 OneDrive
echo   📂 Home Directory
echo.
echo Press Ctrl+C to stop monitoring
echo.

%PYTHON_EXE% -c "%CLI_CMD%" monitor --system-wide --stats

echo.
echo 👋 System-wide monitoring stopped.
pause
