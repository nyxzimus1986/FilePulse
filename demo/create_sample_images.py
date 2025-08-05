#!/usr/bin/env python3
"""
Create sample images for testing the icon and splash generators
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_icon():
    """Create a sample icon image"""
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a colorful circle
    draw.ellipse([50, 50, 206, 206], fill="#3498db", outline="#2980b9", width=8)
    
    # Draw inner circle
    draw.ellipse([90, 90, 166, 166], fill="#e74c3c", outline="#c0392b", width=4)
    
    # Draw center dot
    draw.ellipse([118, 118, 138, 138], fill="#f1c40f")
    
    img.save("demo/sample_icon.png")
    print("Created demo/sample_icon.png")

def create_sample_background():
    """Create a sample background image"""
    img = Image.new('RGB', (800, 600), "#2c3e50")
    draw = ImageDraw.Draw(img)
    
    # Draw gradient circles
    for i in range(10):
        alpha = 255 - (i * 20)
        radius = 50 + (i * 30)
        color = f"#{hex(100 + i * 15)[2:]:0>2}{hex(150 + i * 10)[2:]:0>2}{hex(200 + i * 5)[2:]:0>2}"
        
        # Multiple circles for interesting pattern
        draw.ellipse([100 + i*20, 100 + i*20, 100 + i*20 + radius, 100 + i*20 + radius], 
                    fill=color)
        draw.ellipse([500 - i*15, 300 + i*10, 500 - i*15 + radius, 300 + i*10 + radius], 
                    fill=color)
    
    img.save("demo/sample_background.jpg")
    print("Created demo/sample_background.jpg")

def create_logo_sample():
    """Create a sample logo image"""
    img = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a simple FilePulse logo
    # Folder shape
    draw.rectangle([40, 80, 160, 160], fill="#3498db", outline="#2980b9", width=3)
    draw.rectangle([50, 70, 90, 80], fill="#3498db", outline="#2980b9", width=2)
    
    # Pulse waves
    for i in range(3):
        y = 100 + i * 15
        draw.arc([60, y, 140, y + 20], 0, 180, fill="#e74c3c", width=4)
    
    img.save("demo/sample_logo.png")
    print("Created demo/sample_logo.png")

def create_nature_background():
    """Create a nature-inspired background"""
    img = Image.new('RGB', (1024, 768), "#1a4f3a")
    draw = ImageDraw.Draw(img)
    
    # Draw mountain silhouettes
    points = [(0, 500), (200, 300), (400, 400), (600, 250), (800, 350), (1024, 280), (1024, 768), (0, 768)]
    draw.polygon(points, fill="#0f3d2c")
    
    # Draw trees (simplified)
    for x in range(50, 1000, 80):
        # Tree trunk
        draw.rectangle([x, 450, x+10, 500], fill="#3d2914")
        # Tree top
        draw.ellipse([x-20, 400, x+30, 460], fill="#2d5a3d")
    
    # Add some stars
    for i in range(50):
        x = i * 20 + 10
        y = 50 + (i % 7) * 30
        draw.ellipse([x, y, x+3, y+3], fill="#ffffff")
    
    img.save("demo/nature_background.jpg")
    print("Created demo/nature_background.jpg")

if __name__ == "__main__":
    print("Creating sample images for FilePulse generators...")
    
    create_sample_icon()
    create_sample_background()
    create_logo_sample()
    create_nature_background()
    
    print("\nSample images created! You can now:")
    print("1. Run the icon generator and load demo/sample_icon.png or demo/sample_logo.png")
    print("2. Run the splash generator and load demo/sample_background.jpg or demo/nature_background.jpg")
    print("3. Experiment with different opacity, scale, and blur settings")
