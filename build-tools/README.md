# Build Tools Directory

This directory contains all build-related files for creating standalone executables and managing the build process.

## Build Scripts
- `build.bat` - Main build script for Windows
- `build.ps1` - PowerShell build script
- `build.sh` - Shell script for Unix/Linux builds
- `build-complete.bat` - Complete build with all components
- `build-final.bat` - Final production build
- `build-standalone.bat` - Standalone executable build
- `build-with-tools.bat` - Build including development tools

## PyInstaller Specs
- `filepulse.spec` - Main application spec
- `filepulse-gui.spec` - GUI application spec
- `filepulse-cli.spec` - CLI application spec
- `FilePulse-*.spec` - Various specialized build configurations

## Utility Scripts
- `demo-splash.bat` - Demo splash screen
- `generate-assets.bat` - Generate application assets
- `run-icon-generator.bat` - Icon generation utility
- `run-splash-generator.bat` - Splash screen generation utility
- `test-all.bat` - Run all tests
- `test-cli.bat` - Test CLI functionality

## Requirements
- `requirements-build.txt` - Build-time dependencies

## Usage
Run the main build script:
```bash
build.bat
```

For specific builds:
```bash
build-standalone.bat  # For standalone executable
build-complete.bat    # For complete build with all features
```
