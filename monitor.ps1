# FilePulse Monitor Launcher for PowerShell
# Usage: .\monitor.ps1 [path] [options]

$PythonExe = "C:/Users/nyxzi/AppData/Local/Programs/Python/Python313/python.exe"
$CliCmd = "import sys; sys.path.insert(0, '.'); from filepulse.cli import main; main()"

Write-Host "FilePulse Filesystem Monitor" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Green

if ($args.Count -eq 0) {
    Write-Host "Monitoring current directory..." -ForegroundColor Yellow
    & $PythonExe -c $CliCmd monitor . --stats
}
elseif ($args[0] -eq "help") {
    & $PythonExe -c $CliCmd --help
}
elseif ($args[0] -eq "test") {
    Write-Host "Running tests..." -ForegroundColor Yellow
    & $PythonExe test_filepulse.py
}
elseif ($args[0] -eq "config") {
    Write-Host "Creating default config..." -ForegroundColor Yellow
    & $PythonExe -c $CliCmd init-config filepulse.yaml
    Write-Host "Config created: filepulse.yaml" -ForegroundColor Green
}
else {
    Write-Host "Monitoring path: $($args[0])" -ForegroundColor Yellow
    & $PythonExe -c $CliCmd monitor $args[0] --stats
}
