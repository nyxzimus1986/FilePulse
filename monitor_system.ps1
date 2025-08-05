# FilePulse System-Wide Monitor Launcher for PowerShell

$PythonExe = "C:/Users/nyxzi/AppData/Local/Programs/Python/Python313/python.exe"
$CliCmd = "import sys; sys.path.insert(0, '.'); from filepulse.cli import main; main()"

Write-Host "🌐 FilePulse System-Wide Filesystem Monitor" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "This will monitor your:" -ForegroundColor Yellow
Write-Host "  📂 Desktop" -ForegroundColor Cyan
Write-Host "  📂 Documents" -ForegroundColor Cyan  
Write-Host "  📂 Downloads" -ForegroundColor Cyan
Write-Host "  📂 Pictures, Videos, Music" -ForegroundColor Cyan
Write-Host "  📂 OneDrive" -ForegroundColor Cyan
Write-Host "  📂 Home Directory" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop monitoring" -ForegroundColor Yellow
Write-Host ""

& $PythonExe -c $CliCmd monitor --system-wide --stats

Write-Host ""
Write-Host "👋 System-wide monitoring stopped." -ForegroundColor Yellow
