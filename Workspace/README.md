# FilePulse Workspace

Welcome to the FilePulse development workspace! This is a properly organized VS Code workspace for the FilePulse filesystem monitoring application.

## 🚀 Quick Start

### Launch FilePulse
Use VS Code's Command Palette (`Ctrl+Shift+P`) → **Tasks: Run Task** → Select:
- **Launch FilePulse (Main)** - Run the main transparent splash launcher
- **Launch FilePulse (Batch)** - Run via Windows batch file with debug output
- **Launch from Scripts** - Run directly from scripts directory

### Or use keyboard shortcuts:
- `Ctrl+Shift+P` → `Tasks: Run Build Task` → Select launcher

## 📁 Project Structure

```
../                          # Main FilePulse project directory
├── filepulse_launcher.py    # Main application launcher (RECOMMENDED)
├── run_filepulse.bat       # Windows batch launcher
├── filepulse/              # Main application module
│   └── gui.py              # Main GUI class
├── scripts/                # Alternative launchers and entry points
│   ├── launch_gui_transparent.py  # Transparent splash launcher
│   ├── launch_gui_with_splash.py  # Standard splash launcher
│   └── README.md           # Launcher documentation
├── build-tools/            # Build scripts and PyInstaller specs
│   ├── build.bat          # Main build script
│   ├── *.spec             # PyInstaller specifications
│   └── README.md          # Build documentation
├── assets/                 # Images and resources
│   └── splash/            # Splash screen images
├── tests/                 # Test files
├── development/           # Experimental files
└── Workspace/             # This VS Code workspace (current directory)
    ├── .vscode/           # VS Code configuration
    ├── .github/           # GitHub and Copilot configuration
    └── README.md          # This file
```

## 🛠️ Development Features

### Available Tasks
- **Launch FilePulse (Main)** - Primary launcher with transparent splash
- **Launch FilePulse (Batch)** - Batch file launcher with debug output
- **Launch from Scripts** - Direct script execution
- **Run Tests** - Execute test suite
- **Install Dependencies** - Install Python requirements

### VS Code Extensions
- ✅ Python - Core Python support
- ✅ Pylint - Code linting
- ✅ Black Formatter - Code formatting

### Python Environment
- Default interpreter: `python`
- Type checking: Basic
- Linting: Enabled (Pylint)
- Formatting: Black

## 🎨 Key Features

### Transparent Splash Screen
- Beautiful transparent fade effects
- Professional loading animation
- Custom splash image support
- Smooth transitions to main GUI

### Organized Codebase
- Clean separation of concerns
- Dedicated directories for different file types
- Comprehensive documentation
- Easy maintenance and development

## 🔧 Usage

### Running FilePulse
1. **Recommended**: Use `Ctrl+Shift+P` → Tasks: Run Task → Launch FilePulse (Main)
2. **Alternative**: Use the batch file task for debug output
3. **Development**: Use the scripts launcher for testing

### Building Executables
Navigate to `../build-tools/` and run the appropriate build script:
```bash
cd ../build-tools
build.bat
```

### Testing
Use the "Run Tests" task or navigate to the tests directory:
```bash
cd ../tests
python test_filepulse.py
```

## 📋 Requirements

- Python 3.8+
- tkinter (usually included with Python)
- PIL/Pillow for image processing
- pathlib for modern path handling

Install dependencies:
```bash
pip install -r ../requirements.txt
```

## 🎯 Next Steps

1. **Try the launcher**: Run the "Launch FilePulse (Main)" task
2. **Explore the code**: Check out the organized directory structure
3. **Customize**: Modify splash screens, add features, or build executables
4. **Develop**: Use the comprehensive VS Code setup for efficient development

---

**Happy coding!** 🚀 Your FilePulse workspace is ready for professional development.
