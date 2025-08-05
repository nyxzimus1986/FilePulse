# FilePulse Project Structure

FilePulse is organized into a clean, professional directory structure:

```
FilePulse/
├── filepulse/                 # Core application package
│   ├── __init__.py           
│   ├── cli.py                # Command line interface
│   ├── gui.py                # GUI interface
│   ├── monitor.py            # Core monitoring logic
│   ├── advanced_splash.py    # Advanced splash screen
│   └── config/               # Configuration files
│       ├── default.yaml      # Default settings
│       └── logging.yaml      # Logging configuration
│
├── tools/                    # Design and development tools
│   ├── icon_generator.py     # Icon design tool
│   ├── splash_generator.py   # Splash screen design tool
│   └── README.md             # Tools documentation
│
├── assets/                   # Generated visual assets
│   ├── icons/                # Application icons
│   │   ├── filepulse-icon.ico
│   │   ├── filepulse-icon-*.png
│   │   └── ...
│   ├── splash/               # Splash screens
│   │   ├── splash-screen.png
│   │   ├── custom-splash.py
│   │   └── ...
│   ├── presets/              # Design presets
│   │   ├── icon-preset-*.json
│   │   ├── splash-preset-*.json
│   │   └── ...
│   └── README.md             # Assets documentation
│
├── dist/                     # Built executables (generated)
├── build/                    # Build artifacts (generated)
├── tests/                    # Test files
├── docs/                     # Documentation
│
├── gui_final.py              # GUI entry point with splash
├── generate-assets.py        # Default asset generator
├── setup.py                  # Package configuration
├── requirements.txt          # Python dependencies
├── README.md                 # Main documentation
├── LICENSE                   # License file
│
├── build-with-tools.bat      # Complete build script
├── generate-assets.bat       # Asset generation script
├── run-icon-generator.bat    # Icon generator launcher
├── run-splash-generator.bat  # Splash generator launcher
└── demo-splash.bat           # Splash demo script
```

## Directory Purposes

### Core Application (`filepulse/`)
Contains the main FilePulse application code:
- **cli.py**: Command-line interface for terminal usage
- **gui.py**: Tkinter-based graphical interface
- **monitor.py**: Core filesystem monitoring logic
- **advanced_splash.py**: Professional animated splash screen
- **config/**: YAML configuration files for settings and logging

### Design Tools (`tools/`)
Professional design tools for customizing FilePulse appearance:
- **icon_generator.py**: Create custom application icons with multiple styles
- **splash_generator.py**: Design animated startup splash screens
- **README.md**: Comprehensive tools documentation

### Visual Assets (`assets/`)
Organized storage for all generated visual content:
- **icons/**: Application icons in ICO and PNG formats
- **splash/**: Splash screen images and generated Python code
- **presets/**: Saved design configurations for reuse
- **README.md**: Asset management documentation

### Build System
- **build-with-tools.bat**: Creates all executable variants
- **generate-assets.bat**: Generates default visual assets
- **gui_final.py**: Entry point integrating splash screen with GUI

### Development
- **setup.py**: Professional package configuration with entry points
- **requirements.txt**: Python dependencies
- **tests/**: Unit tests and integration tests
- **docs/**: Additional documentation

## Key Features

### Professional Organization
- Clear separation of concerns
- Consistent naming conventions
- Comprehensive documentation
- Asset management system

### Design System Integration
- Automatic asset discovery
- Preset management
- Build system integration
- Professional visual identity

### Development Workflow
- Clean build artifacts in `dist/`
- Organized source code structure
- Tool integration and automation
- Version control friendly

## Usage Patterns

### For End Users:
```bash
# Run the application
FilePulse-GUI.exe

# Use design tools
FilePulse-IconGenerator.exe
FilePulse-SplashGenerator.exe
```

### For Developers:
```bash
# Generate default assets
python generate-assets.py

# Create custom designs
python tools/icon_generator.py
python tools/splash_generator.py

# Build all variants
build-with-tools.bat
```

### For Customization:
1. Use design tools to create custom assets
2. Save presets for reuse
3. Generated assets automatically used in builds
4. Professional deployment ready

This structure supports both casual users and professional deployment scenarios while maintaining clean organization and easy customization.
