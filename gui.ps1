# FilePulse GUI Launcher for PowerShell

$PythonExe = "C:/Users/nyxzi/AppData/Local/Programs/Python/Python313/python.exe"

Write-Host "🚀 Launching FilePulse GUI..." -ForegroundColor Green
Write-Host ""

try {
    & $PythonExe launch_gui.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error launching GUI." -ForegroundColor Red
    } else {
        Write-Host "👋 FilePulse GUI closed." -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}
