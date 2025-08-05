#!/usr/bin/env python3
"""
Generate default FilePulse assets
Creates default icons and splash screens using the design tools
"""

import os
import sys
from pathlib import Path
import json

# Add tools directory to path
tools_dir = Path(__file__).parent / "tools"
sys.path.insert(0, str(tools_dir))

def generate_default_icon():
    """Generate default FilePulse icon"""
    try:
        from icon_generator import IconGenerator
        import tkinter as tk
        from PIL import Image, ImageDraw
        
        print("Generating default FilePulse icon...")
        
        # Create assets directory
        assets_dir = Path(__file__).parent / "assets" / "icons"
        assets_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a simple icon programmatically
        size = 256
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Background circle
        bg_color = "#3498db"
        draw.ellipse([10, 10, size-10, size-10], fill=bg_color)
        
        # Folder
        center = size // 2
        folder_size = size // 4
        folder_x = center - folder_size
        folder_y = center - folder_size // 2
        
        # Folder body
        draw.rectangle([folder_x, folder_y, folder_x + folder_size*2, folder_y + folder_size],
                      fill="#2980b9")
        
        # Folder tab
        tab_width = folder_size // 2
        draw.rectangle([folder_x, folder_y - folder_size//4, folder_x + tab_width, folder_y],
                      fill="#2980b9")
        
        # Pulse rings
        pulse_color = "#e74c3c"
        for i, radius in enumerate([size//6, size//4.5, size//3.5]):
            draw.ellipse([center-radius, center-radius, center+radius, center+radius],
                        outline=pulse_color, width=3)
        
        # Save as ICO with multiple sizes
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        icon_images = []
        
        for ico_size in sizes:
            resized = img.resize(ico_size, Image.Resampling.LANCZOS)
            icon_images.append(resized)
            
            # Save individual PNG
            png_path = assets_dir / f"filepulse-icon-{ico_size[0]}x{ico_size[1]}.png"
            resized.save(png_path, format='PNG')
        
        # Save main ICO file
        ico_path = assets_dir / "filepulse-icon.ico"
        icon_images[0].save(ico_path, format='ICO', sizes=[(img.size[0], img.size[1]) for img in icon_images])
        
        # Save main PNG
        png_path = assets_dir / "filepulse-icon.png"
        img.save(png_path, format='PNG')
        
        print(f"✓ Default icon saved to {ico_path}")
        print(f"✓ PNG variants saved to assets/icons/")
        
    except Exception as e:
        print(f"✗ Failed to generate default icon: {e}")

def generate_default_splash():
    """Generate default splash screen"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        print("Generating default splash screen...")
        
        # Create assets directory
        assets_dir = Path(__file__).parent / "assets" / "splash"
        assets_dir.mkdir(parents=True, exist_ok=True)
        
        # Splash settings
        width, height = 600, 400
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Gradient background
        start_color = (44, 62, 80)  # #2c3e50
        end_color = (52, 152, 219)  # #3498db
        
        for y in range(height):
            ratio = y / height
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Logo
        center_x = width // 2
        logo_y = height // 3
        logo_size = 60
        
        # Folder
        folder_width = logo_size
        folder_height = logo_size // 2
        folder_x = center_x - folder_width // 2
        folder_y = logo_y - folder_height // 2
        
        draw.rectangle([folder_x, folder_y, folder_x + folder_width, folder_y + folder_height],
                      fill="#ffffff")
        
        # Folder tab
        tab_width = folder_width // 3
        draw.rectangle([folder_x, folder_y - folder_height//3, folder_x + tab_width, folder_y],
                      fill="#ffffff")
        
        # Pulse rings
        for i, radius in enumerate([30, 40, 50]):
            draw.ellipse([center_x - radius, logo_y - radius, center_x + radius, logo_y + radius],
                        outline="#ffffff", width=2)
        
        # Text
        try:
            title_font = ImageFont.truetype("arial.ttf", 32)
            subtitle_font = ImageFont.truetype("arial.ttf", 16)
            loading_font = ImageFont.truetype("arial.ttf", 12)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            loading_font = ImageFont.load_default()
        
        # Title
        title_text = "FilePulse"
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text((center_x - title_width//2, height//2), title_text, 
                 fill="#ffffff", font=title_font)
        
        # Subtitle
        subtitle_text = "Real-time Filesystem Monitor"
        subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        draw.text((center_x - subtitle_width//2, height//2 + 40), subtitle_text,
                 fill="#bdc3c7", font=subtitle_font)
        
        # Loading text
        loading_text = "Loading..."
        loading_bbox = draw.textbbox((0, 0), loading_text, font=loading_font)
        loading_width = loading_bbox[2] - loading_bbox[0]
        draw.text((center_x - loading_width//2, height - 60), loading_text,
                 fill="#bdc3c7", font=loading_font)
        
        # Progress bar
        bar_width = width // 2
        bar_height = 6
        bar_x = (width - bar_width) // 2
        bar_y = height - 40
        
        # Background
        draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height],
                      fill="#34495e")
        
        # Progress (60% for demo)
        progress_width = int(bar_width * 0.6)
        draw.rectangle([bar_x, bar_y, bar_x + progress_width, bar_y + bar_height],
                      fill="#3498db")
        
        # Save splash screen
        splash_path = assets_dir / "splash-screen.png"
        img.save(splash_path, format='PNG')
        
        print(f"✓ Default splash screen saved to {splash_path}")
        
    except Exception as e:
        print(f"✗ Failed to generate default splash screen: {e}")

def main():
    """Generate all default assets"""
    print("FilePulse Asset Generator")
    print("=" * 40)
    
    # Create main assets directory
    assets_dir = Path(__file__).parent / "assets"
    assets_dir.mkdir(exist_ok=True)
    
    # Generate assets
    generate_default_icon()
    generate_default_splash()
    
    print("\n" + "=" * 40)
    print("Asset generation complete!")
    print("\nGenerated assets:")
    print("  assets/icons/filepulse-icon.ico - Main application icon")
    print("  assets/icons/filepulse-icon-*.png - PNG icon variants")
    print("  assets/splash/splash-screen.png - Default splash screen")
    print("  assets/presets/*.json - Design presets")
    print("\nUse the design tools to create custom variants:")
    print("  python tools/icon_generator.py")
    print("  python tools/splash_generator.py")

if __name__ == "__main__":
    main()
