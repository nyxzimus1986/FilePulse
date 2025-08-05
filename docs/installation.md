# Installation Guide

## Prerequisites

- Python 3.8 or higher
- Operating System: Windows, macOS, or Linux

## Installation Methods

### From PyPI (Recommended)

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
- GUI applications may require additional permissions for system-wide monitoring
- Use PowerShell or Command Prompt for CLI operations

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
