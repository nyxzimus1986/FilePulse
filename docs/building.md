# Building Executables

This guide explains how to build standalone executables for FilePulse that can run on systems without Python installed.

## Quick Start

### Windows

1. **Using Batch Script (Recommended):**
   ```cmd
   build.bat
   ```

2. **Using PowerShell:**
   ```powershell
   .\build.ps1
   ```

### Linux/macOS

```bash
chmod +x build.sh
./build.sh
```

## Manual Build Process

### Prerequisites

1. **Install Build Dependencies:**
   ```bash
   pip install -r requirements-build.txt
   ```

2. **Verify PyInstaller Installation:**
   ```bash
   pyinstaller --version
   ```

### Building Individual Executables

#### GUI Version Only
```bash
pyinstaller filepulse-gui.spec --clean --noconfirm
```

#### CLI Version Only
```bash
pyinstaller filepulse-cli.spec --clean --noconfirm
```

#### Both Versions (Recommended)
```bash
pyinstaller filepulse.spec --clean --noconfirm
```

## Output Structure

After building, you'll find the executables in the `dist/` directory:

```
dist/
├── FilePulse-GUI/
│   ├── FilePulse.exe          # Main GUI executable (Windows)
│   ├── FilePulse              # Main GUI executable (Linux/macOS)
│   ├── config/
│   │   └── default.yaml
│   ├── docs/
│   └── [supporting files...]
└── FilePulse-CLI/
    ├── filepulse-cli.exe      # CLI executable (Windows)
    ├── filepulse-cli          # CLI executable (Linux/macOS)
    ├── config/
    │   └── default.yaml
    └── [supporting files...]
```

## File Sizes

Typical executable sizes:
- **GUI Version**: ~40-60 MB (includes Tkinter and all dependencies)
- **CLI Version**: ~25-35 MB (smaller, no GUI dependencies)

## Platform-Specific Notes

### Windows

- **Executables**: `.exe` files
- **Icons**: Supports `.ico` files (place in `assets/` folder)
- **Version Info**: Uses `version_info.txt` for file properties
- **UPX Compression**: Enabled by default to reduce file size
- **Console**: GUI version runs without console window

### Linux

- **Executables**: No extension
- **Dependencies**: Includes all Python dependencies
- **Permissions**: May need `chmod +x` to make executable
- **Desktop Integration**: Can create `.desktop` files for GUI

### macOS

- **Executables**: No extension
- **App Bundles**: Can be converted to `.app` bundles
- **Code Signing**: May require signing for distribution
- **Permissions**: May need security permissions for filesystem monitoring

## Customization

### Adding Icons

1. Create an `assets/` folder:
   ```bash
   mkdir assets
   ```

2. Add icon files:
   - `assets/filepulse.ico` - Main GUI icon
   - `assets/cli_icon.ico` - CLI icon (optional)

3. Rebuild executables

### Modifying Build Settings

Edit the `.spec` files to customize:

- **Hidden imports**: Add modules that PyInstaller misses
- **Data files**: Include additional files in the executable
- **Exclusions**: Remove unused modules to reduce size
- **UPX settings**: Adjust compression settings
- **Console settings**: Show/hide console window

### Example Customization

```python
# In filepulse.spec
gui_exe = EXE(
    # ... other settings ...
    console=False,  # Hide console for GUI
    icon='assets/custom_icon.ico',  # Custom icon
    version='version_info.txt',  # Version information
)
```

## Advanced Options

### One-File Executables

To create single-file executables (slower startup, but easier distribution):

```bash
pyinstaller filepulse/gui.py --onefile --name FilePulse --noconsole
pyinstaller filepulse/cli.py --onefile --name filepulse-cli --console
```

### Debug Mode

For troubleshooting build issues:

```bash
pyinstaller filepulse.spec --debug=all --clean
```

### Clean Build

To ensure a completely fresh build:

```bash
# Remove build artifacts
rm -rf build/ dist/ *.spec~

# Clean build
pyinstaller filepulse.spec --clean --noconfirm
```

## Distribution

### Windows

1. **Folder Distribution**: 
   - Zip the `dist/FilePulse-GUI/` folder
   - Users extract and run `FilePulse.exe`

2. **Installer Creation**:
   - Use NSIS, Inno Setup, or similar
   - Create proper Windows installer

### Linux

1. **Portable Distribution**:
   - Tar the executable folder: `tar -czf FilePulse-linux.tar.gz dist/FilePulse-GUI/`

2. **Package Creation**:
   - Create `.deb` packages for Debian/Ubuntu
   - Create `.rpm` packages for Red Hat/Fedora

### macOS

1. **App Bundle**:
   - Use `--windowed` flag for `.app` creation
   - Sign the application for distribution

## Troubleshooting

### Common Issues

1. **Import Errors**:
   - Add missing modules to `hiddenimports` in `.spec` file
   - Check for dynamic imports in your code

2. **File Not Found**:
   - Add missing data files to `datas` in `.spec` file
   - Verify file paths are correct

3. **Large File Size**:
   - Add unused modules to `excludes`
   - Enable UPX compression
   - Remove unnecessary data files

4. **Slow Startup**:
   - Consider using `--onedir` instead of `--onefile`
   - Optimize imports in your code

### Debug Commands

```bash
# Check what's included in the executable
pyi-archive_viewer dist/FilePulse-GUI/FilePulse.exe

# Test import issues
pyinstaller --debug=imports filepulse.spec

# Verbose output
pyinstaller --log-level=DEBUG filepulse.spec
```

## Testing

### Automated Testing

The build scripts include basic tests:

1. **Version Check**: Verifies executable runs and shows version
2. **GUI Test**: Briefly opens GUI to verify it launches
3. **File Structure**: Checks all required files are included

### Manual Testing

1. **Copy to Clean System**: Test on system without Python
2. **Test All Features**: Verify monitoring, configuration, GUI functionality
3. **Performance Test**: Check memory usage and responsiveness
4. **File Associations**: Test opening config files (if implemented)

## CI/CD Integration

### GitHub Actions

The project includes automated builds in `.github/workflows/release.yml`:

- Builds executables for Windows, Linux, and macOS
- Attaches executables to GitHub releases
- Runs automated tests on built executables

### Local CI

```bash
# Build and test all platforms (if cross-compilation tools available)
python scripts/build_all.py
```

## Best Practices

1. **Regular Testing**: Test executables on clean systems
2. **Version Consistency**: Keep version numbers synchronized
3. **Size Optimization**: Regularly review and minimize executable size
4. **Security**: Scan executables for false positives in antivirus
5. **Documentation**: Keep build instructions updated
6. **Backup**: Store successful builds for rollback capability
