# FilePulse Demo Images

This folder contains sample images to test the enhanced icon and splash screen generators with custom image loading functionality.

## Sample Images

### For Icon Generator:
- **sample_icon.png** - A colorful circular icon with concentric circles (256x256, transparent background)
- **sample_logo.png** - A simple FilePulse-style logo with folder and pulse waves (200x200, transparent background)

### For Splash Screen Generator:
- **sample_background.jpg** - An abstract background with gradient circles (800x600)
- **nature_background.jpg** - A nature-inspired background with mountains and trees (1024x768)

## How to Use

### Icon Generator
1. Run the icon generator: `python tools/icon_generator.py`
2. Check "Use Custom Image" in the Custom Image section
3. Click "Load Image" and select one of the sample icons
4. Adjust opacity (0-100%) to blend with background colors
5. Adjust scale (10-200%) to resize the image
6. Add text overlay if desired
7. Generate preview and export when satisfied

### Splash Screen Generator
1. Run the splash screen generator: `python tools/splash_generator.py`
2. Go to the "Background Image" tab
3. Check "Use Custom Background Image"
4. Click "Load Background Image" and select one of the sample backgrounds
5. Adjust opacity (0-100%) to blend with gradient colors
6. Adjust blur (0-20) to create depth effects
7. Adjust scale (50-200%) to resize the background
8. Customize other elements (text, colors, animations) as desired
9. Generate preview and export when satisfied

## Creating Your Own Images

Run `python demo/create_sample_images.py` to regenerate the sample images or modify the script to create custom samples.

## Tips

- **PNG files** work best for icons as they support transparency
- **JPG files** work well for backgrounds and are smaller in size
- **High resolution images** (1024x768 or larger) work best for splash screen backgrounds
- **Square images** work best for icons
- Experiment with different opacity and blur settings to achieve the desired visual effect
- Custom images can be combined with existing color themes and styles
