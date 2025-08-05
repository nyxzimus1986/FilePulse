# FilePulse Build Script for PowerShell
# This script builds standalone executables for both CLI and GUI versions

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FilePulse Executable Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python version: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ and try again" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install build dependencies
Write-Host "Installing build dependencies..." -ForegroundColor Yellow
pip install -r requirements-build.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install build dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host
Write-Host "Building executables..." -ForegroundColor Yellow
Write-Host "This may take several minutes..." -ForegroundColor Yellow
Write-Host

# Clean previous builds
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }

# Build both executables
Write-Host "Building FilePulse GUI and CLI..." -ForegroundColor Yellow
pyinstaller filepulse.spec --clean --noconfirm
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Build failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host
Write-Host "========================================" -ForegroundColor Green
Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host
Write-Host "Executables created in:" -ForegroundColor Cyan
Write-Host "  GUI: dist\FilePulse-GUI\FilePulse.exe" -ForegroundColor White
Write-Host "  CLI: dist\FilePulse-CLI\filepulse-cli.exe" -ForegroundColor White
Write-Host

# Test the executables
Write-Host "Testing executables..." -ForegroundColor Yellow
Write-Host
Write-Host "Testing CLI version:" -ForegroundColor Cyan
& "dist\FilePulse-CLI\filepulse-cli.exe" --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: CLI executable test failed" -ForegroundColor Yellow
} else {
    Write-Host "CLI executable working correctly" -ForegroundColor Green
}

Write-Host
Write-Host "Testing GUI version (will open briefly):" -ForegroundColor Cyan
Start-Process "dist\FilePulse-GUI\FilePulse.exe" -WindowStyle Hidden
Start-Sleep -Seconds 3
Get-Process FilePulse -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Write-Host "GUI executable test completed" -ForegroundColor Green

Write-Host
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Build Summary:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Get-ChildItem -Path "dist" -Directory | Format-Table Name, @{Name="Size"; Expression={"{0:N2} MB" -f ((Get-ChildItem -Path $_.FullName -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB)}}

Write-Host
Write-Host "To run FilePulse:" -ForegroundColor Cyan
Write-Host "  GUI: Double-click dist\FilePulse-GUI\FilePulse.exe" -ForegroundColor White
Write-Host "  CLI: Run dist\FilePulse-CLI\filepulse-cli.exe from command line" -ForegroundColor White
Write-Host
Write-Host "You can copy these folders to any Windows machine to run FilePulse" -ForegroundColor Green
Write-Host "without requiring Python installation." -ForegroundColor Green
Write-Host

Read-Host "Press Enter to exit"
