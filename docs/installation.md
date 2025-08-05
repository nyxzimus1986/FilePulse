# Installation Guide

## Prerequisites

- Python 3.8 or higher
- Operating System: Windows, macOS, or Linux

## Installation Methods

### Standalone Executables (No Python Required) ⭐

**Windows Users - Easiest Option:**

1. **Download**: Get the latest release from [GitHub Releases](https://github.com/yourusername/filepulse/releases)
2. **Extract**: Unzip the downloaded file to any folder on your computer
3. **Run Immediately**: 
   - **GUI Version**: Double-click `FilePulse.exe` for the graphical interface
   - **CLI Version**: Open Command Prompt and run `filepulse-cli.exe --help`

**✅ Zero Dependencies**: No Python, pip, or any other software required!  
**✅ Fully Portable**: Copy the .exe files to any Windows machine and run instantly  
**✅ Small Size**: ~7-11 MB per executable - very lightweight  

**What you get:**
- `FilePulse.exe` - Complete GUI application (~11 MB)
- `filepulse-cli.exe` - Command-line interface (~7 MB)
- Built-in configuration files and documentation

### From PyPI (Python Required)

```bash
pip install filepulse
```

### From Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/filepulse.git
cd filepulse
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install in development mode:
```bash
pip install -e .
```

### Using pip from GitHub

```bash
pip install git+https://github.com/yourusername/filepulse.git
```

## Verification

### For Standalone Executables

**Test the GUI:**
```cmd
# Double-click FilePulse.exe or run from command line:
FilePulse.exe
```

**Test the CLI:**
```cmd
# Run from the folder containing the executable:
filepulse-cli.exe --version
filepulse-cli.exe --help

# Example: Monitor current directory
filepulse-cli.exe monitor .
```

### For Python Installation

Verify the installation by running:

```bash
filepulse --version
```

## Optional Dependencies

### Development Dependencies

For development and testing:

```bash
pip install filepulse[dev]
```

This includes:
- pytest (testing framework)
- pytest-cov (coverage reporting)
- black (code formatting)
- flake8 (linting)
- mypy (type checking)

## Platform-Specific Notes

### Windows

- FilePulse supports Windows 7 and later
- **Standalone executables available** - no Python installation required
- GUI applications may require additional permissions for system-wide monitoring
- Use PowerShell or Command Prompt for CLI operations
- **Portable**: Copy the executable folders to any Windows machine and run directly

### macOS

- Some monitoring features may require special permissions
- GUI applications work best with macOS 10.14 (Mojave) or later

### Linux

- Most distributions are supported
- GUI requires X11 or Wayland display server
- Some features may require additional permissions

## Troubleshooting

### Common Issues

1. **Permission Errors**: Some filesystem monitoring requires elevated permissions
2. **GUI Not Starting**: Ensure display server is available and properly configured
3. **Import Errors**: Verify all dependencies are installed correctly

### Getting Help

- Check the [FAQ](faq.md)
- Review [troubleshooting guide](troubleshooting.md)
- Open an issue on [GitHub](https://github.com/yourusername/filepulse/issues)
