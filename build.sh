#!/bin/bash
# FilePulse Build Script for Linux/macOS
# This script builds standalone executables for both CLI and GUI versions

echo "========================================"
echo "FilePulse Executable Build Script"
echo "========================================"
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

echo "Python version:"
python3 --version

echo
echo "Installing build dependencies..."
pip3 install -r requirements-build.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install build dependencies"
    exit 1
fi

echo
echo "Building executables..."
echo "This may take several minutes..."
echo

# Clean previous builds
rm -rf dist build

# Build both executables
echo "Building FilePulse GUI and CLI..."
pyinstaller filepulse.spec --clean --noconfirm
if [ $? -ne 0 ]; then
    echo "ERROR: Build failed"
    exit 1
fi

echo
echo "========================================"
echo "Build completed successfully!"
echo "========================================"
echo
echo "Executables created in:"
echo "  GUI: dist/FilePulse-GUI/FilePulse"
echo "  CLI: dist/FilePulse-CLI/filepulse-cli"
echo

# Test the executables
echo "Testing executables..."
echo
echo "Testing CLI version:"
./dist/FilePulse-CLI/filepulse-cli --version
if [ $? -ne 0 ]; then
    echo "WARNING: CLI executable test failed"
else
    echo "CLI executable working correctly"
fi

echo
echo "GUI executable created (manual testing required on systems with display)"

echo
echo "========================================"
echo "Build Summary:"
echo "========================================"
ls -la dist/
echo
echo "To run FilePulse:"
echo "  GUI: ./dist/FilePulse-GUI/FilePulse"
echo "  CLI: ./dist/FilePulse-CLI/filepulse-cli"
echo
echo "You can copy these folders to any compatible system to run FilePulse"
echo "without requiring Python installation."
echo
