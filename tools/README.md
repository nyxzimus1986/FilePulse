# FilePulse Design Tools

This directory contains visual design tools for customizing FilePulse:

## Icon Generator (`icon_generator.py`)

Create custom icons for FilePulse with various styles and color schemes.

### Features:
- **Multiple Icon Styles**: Modern, Classic, Minimal, and 3D styles
- **Color Customization**: Full control over background, folder, and pulse colors
- **Custom Image Loading**: Import your own images (PNG, JPG, etc.) as icon base
- **Image Controls**: Adjust opacity (0-100%) and scale (10-200%) for custom images
- **Size Options**: Generate icons from 16x16 to 512x512 pixels
- **Text Overlay**: Add custom text to icons with automatic outline
- **Quick Presets**: Blue, Green, Orange, Purple, and Dark themes
- **Export Formats**: Save as PNG or ICO (Windows icon format)
- **Real-time Preview**: See changes instantly

### New Custom Image Features:
- Load PNG, JPG, GIF, BMP, or TIFF images
- Blend custom images with background colors using opacity control
- Scale images from 10% to 200% of the icon size
- Automatic transparency handling for PNG files
- Works with all icon styles and text overlays

### Usage:
```bash
# Run directly
python tools/icon_generator.py

# Or use the batch file
run-icon-generator.bat
```

### Preset Colors:
- **Default Blue**: Modern blue gradient with red pulse
- **Forest Green**: Nature-inspired green theme
- **Sunset Orange**: Warm orange/yellow theme  
- **Deep Purple**: Rich purple gradient
- **Dark Mode**: Dark theme with blue accents

## Splash Screen Generator (`splash_generator.py`)

Design custom animated splash screens for FilePulse startup.

### Features:
- **Gradient Backgrounds**: Customizable color gradients
- **Custom Background Images**: Load your own background images (PNG, JPG, etc.)
- **Image Effects**: Control opacity (0-100%), blur (0-20), and scale (50-200%)
- **Logo Integration**: FilePulse folder icon with pulse rings
- **Text Customization**: Title, subtitle, and loading text
- **Progress Bar**: Animated loading progress indicator
- **Animation Options**: Pulse, Fade, Slide, Rotate, Scale effects
- **Theme Presets**: Blue, Dark, Green, Purple color themes
- **Code Generation**: Export as standalone Python code
- **Real-time Preview**: Live preview with animation simulation

### New Background Image Features:
- Load high-resolution backgrounds (PNG, JPG, GIF, BMP, TIFF)
- Intelligent scaling to fill screen while maintaining aspect ratio
- Gaussian blur effects for depth and focus
- Opacity blending with gradient backgrounds
- Automatic image centering and cropping

### Usage:
```bash
# Run directly
python tools/splash_generator.py

# Or use the batch file
run-splash-generator.bat
```

### Components:
- **Size & Layout**: Dimensions, logo/progress visibility
- **Colors**: Background gradients, text colors, progress colors
- **Text**: Customizable title, subtitle, and loading messages
- **Animation**: Enable/disable animations with style selection

## Integration with FilePulse

### Using Custom Icons:
1. Generate your icon with the Icon Generator
2. Save as `icon.ico` in the FilePulse directory
3. Update PyInstaller build scripts to use your custom icon:
   ```bash
   pyinstaller --icon=icon.ico ...
   ```

### Using Custom Splash Screens:
1. Design your splash screen with the Splash Generator
2. Export as Python code or save preset
3. Replace `filepulse/advanced_splash.py` with generated code
4. Rebuild FilePulse executable

## Dependencies

Both tools require:
- `tkinter` (included with Python)
- `Pillow` (PIL) for image processing
- `json` for preset saving/loading

Install dependencies:
```bash
pip install Pillow
```

## Tips for Best Results

### Icon Design:
- Use high contrast colors for better visibility
- Test icons at multiple sizes (16x16, 32x32, 48x48)
- Keep designs simple for small sizes
- Use the 3D style for modern Windows applications

### Splash Screen Design:
- Keep text readable against gradient backgrounds
- Use brand colors consistently
- Test animations to ensure smooth performance
- Consider accessibility with color choices

## Export Options

### Icons:
- **PNG**: For web use, transparency support
- **ICO**: For Windows applications, multiple sizes in one file

### Splash Screens:
- **PNG/JPEG**: Static image export
- **Python Code**: Complete standalone splash screen class
- **JSON Preset**: Save/load settings for later use

## Professional Tips

1. **Consistency**: Use the same color palette across icons and splash screens
2. **Branding**: Incorporate your organization's brand colors
3. **Performance**: Larger splash screens may take longer to load
4. **Accessibility**: Ensure sufficient color contrast for readability
5. **Testing**: Test on different screen resolutions and DPI settings
6. **Custom Images**: Use high-quality source images for best results
7. **Image Format**: PNG for icons (transparency), JPG for backgrounds (smaller size)

## Demo and Testing

The `demo/` folder contains sample images to test the custom image loading features:

### Sample Files:
- `sample_icon.png` - Colorful icon for testing icon generator
- `sample_logo.png` - FilePulse-style logo for icons
- `sample_background.jpg` - Abstract background for splash screens
- `nature_background.jpg` - Scenic background for splash screens

### Quick Test:
```bash
# Create sample images
python demo/create_sample_images.py

# Test icon generator with custom image
python tools/icon_generator.py
# Check "Use Custom Image" and load demo/sample_icon.png

# Test splash generator with custom background
python tools/splash_generator.py  
# Go to "Background Image" tab and load demo/sample_background.jpg
```

See `demo/README.md` for detailed testing instructions.
