# FilePulse Assets

This directory contains all visual assets for FilePulse:

## Directory Structure

```
assets/
├── icons/          # Generated application icons
├── splash/         # Generated splash screen images and code
├── presets/        # Saved design presets
└── README.md       # This file
```

## Icons (`icons/`)
- **PNG Icons**: Web-ready transparent icons
- **ICO Files**: Windows application icons with multiple sizes
- **SVG Icons**: Vector icons (if generated)

### Naming Convention:
- `filepulse-icon.ico` - Main application icon
- `filepulse-icon-{style}.png` - Style variants (modern, classic, minimal, 3d)
- `filepulse-icon-{size}.png` - Size variants (16x16, 32x32, etc.)

## Splash Screens (`splash/`)
- **Images**: PNG/JPEG splash screen images
- **Code**: Generated Python splash screen classes
- **Animations**: Animated splash screen assets

### Naming Convention:
- `splash-screen.png` - Main splash screen image
- `splash-screen-{theme}.png` - Theme variants (blue, dark, green, purple)  
- `custom-splash.py` - Generated splash screen code
- `splash-{width}x{height}.png` - Size variants

## Presets (`presets/`)
- **Icon Presets**: `.json` files with icon settings
- **Splash Presets**: `.json` files with splash screen settings

### Naming Convention:
- `icon-preset-{name}.json` - Icon design presets
- `splash-preset-{name}.json` - Splash screen design presets

## Usage

### Icon Generator
The Icon Generator will automatically save files to `assets/icons/`:
- Generated icons are saved with descriptive names
- ICO files include multiple resolutions
- PNG files maintain transparency

### Splash Screen Generator  
The Splash Screen Generator will save to `assets/splash/`:
- Static images for preview/reference
- Python code for integration
- Animation assets if applicable

### Build Integration
The build scripts automatically look for assets in this directory:
- `filepulse-icon.ico` is used as the default application icon
- Custom splash screens replace the default implementation

## Best Practices

1. **Version Control**: Include generated assets in version control for reproducible builds
2. **Naming**: Use descriptive names that indicate purpose and variant
3. **Organization**: Keep related assets together (e.g., all blue theme assets)
4. **Documentation**: Update this README when adding new asset types
5. **Cleanup**: Remove unused assets to keep the directory clean

## Integration

### Using Generated Icons:
```bash
# Copy your preferred icon as the main icon
copy "assets\icons\filepulse-icon-modern.ico" "assets\icons\filepulse-icon.ico"

# Build with custom icon
pyinstaller --icon=assets\icons\filepulse-icon.ico ...
```

### Using Generated Splash Screens:
```bash
# Copy generated splash code
copy "assets\splash\custom-splash.py" "filepulse\splash_screen.py"

# Rebuild application
python build-with-tools.bat
```

## Asset Management

The design tools automatically:
- Create organized subdirectories
- Generate multiple formats and sizes  
- Save presets for later use
- Maintain consistent naming conventions

This ensures your FilePulse installation stays organized and professional!
