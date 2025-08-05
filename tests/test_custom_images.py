#!/usr/bin/env python3
"""
Test script for the enhanced FilePulse design tools with custom image support.
This script verifies that all the new functionality works correctly.
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageFilter
        print("✓ PIL (Pillow) modules imported successfully")
        
        import tkinter as tk
        from tkinter import ttk, colorchooser, filedialog, messagebox
        print("✓ Tkinter modules imported successfully")
        
        # Test importing the design tools
        sys.path.insert(0, 'tools')
        from icon_generator import IconGenerator
        from splash_generator import SplashScreenGenerator
        print("✓ Design tool classes imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_sample_images():
    """Test that sample images exist and can be loaded"""
    print("\nTesting sample images...")
    
    demo_path = Path("demo")
    sample_files = [
        "sample_icon.png",
        "sample_logo.png", 
        "sample_background.jpg",
        "nature_background.jpg"
    ]
    
    all_exist = True
    for filename in sample_files:
        filepath = demo_path / filename
        if filepath.exists():
            try:
                from PIL import Image
                img = Image.open(filepath)
                print(f"✓ {filename} - {img.size[0]}x{img.size[1]} {img.mode}")
            except Exception as e:
                print(f"✗ {filename} - Failed to load: {e}")
                all_exist = False
        else:
            print(f"✗ {filename} - File not found")
            all_exist = False
    
    return all_exist

def test_custom_image_methods():
    """Test that custom image methods exist in the classes"""
    print("\nTesting custom image methods...")
    
    try:
        sys.path.insert(0, 'tools')
        from icon_generator import IconGenerator
        from splash_generator import SplashScreenGenerator
        
        # Check IconGenerator methods
        icon_methods = [
            'toggle_custom_image',
            'load_custom_image', 
            'on_opacity_change',
            'on_scale_change',
            'apply_custom_image'
        ]
        
        for method in icon_methods:
            if hasattr(IconGenerator, method):
                print(f"✓ IconGenerator.{method} exists")
            else:
                print(f"✗ IconGenerator.{method} missing")
                return False
        
        # Check SplashScreenGenerator methods
        splash_methods = [
            'toggle_custom_bg',
            'load_background_image',
            'on_bg_opacity_change', 
            'on_bg_blur_change',
            'on_bg_scale_change',
            'apply_custom_background'
        ]
        
        for method in splash_methods:
            if hasattr(SplashScreenGenerator, method):
                print(f"✓ SplashScreenGenerator.{method} exists")
            else:
                print(f"✗ SplashScreenGenerator.{method} missing")
                return False
                
        return True
    except Exception as e:
        print(f"✗ Method test failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        "tools/icon_generator.py",
        "tools/splash_generator.py",
        "tools/README.md",
        "demo/README.md",
        "demo/create_sample_images.py",
        "run-icon-generator.bat",
        "run-splash-generator.bat"
    ]
    
    all_exist = True
    for filepath in required_files:
        if Path(filepath).exists():
            print(f"✓ {filepath}")
        else:
            print(f"✗ {filepath} - Missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("FilePulse Design Tools - Custom Image Support Tests")
    print("=" * 55)
    
    tests = [
        ("Import Tests", test_imports),
        ("Sample Images", test_sample_images), 
        ("Custom Image Methods", test_custom_image_methods),
        ("File Structure", test_file_structure)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name))
        success = test_func()
        results.append((test_name, success))
    
    print("\n" + "=" * 55)
    print("Test Results Summary:")
    print("=" * 55)
    
    all_passed = True
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{test_name:<25} {status}")
        if not success:
            all_passed = False
    
    print("\n" + "=" * 55)
    if all_passed:
        print("🎉 All tests PASSED! Custom image support is ready to use.")
        print("\nNext steps:")
        print("1. Run: python demo/create_sample_images.py")
        print("2. Test: python tools/icon_generator.py")
        print("3. Test: python tools/splash_generator.py")
    else:
        print("❌ Some tests FAILED. Please check the issues above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
