#!/usr/bin/env python3
"""
Simple GUI test to debug FilePulse GUI issues
"""

import sys
import os
import traceback

# Add current directory to Python path
sys.path.insert(0, '.')

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    
    try:
        import tkinter as tk
        print("✓ tkinter imported")
    except ImportError as e:
        print(f"✗ tkinter import failed: {e}")
        return False
    
    try:
        from tkinter import ttk, filedialog, messagebox, scrolledtext
        print("✓ tkinter components imported")
    except ImportError as e:
        print(f"✗ tkinter components import failed: {e}")
        return False
    
    try:
        from filepulse.config import Config
        print("✓ Config imported")
    except ImportError as e:
        print(f"✗ Config import failed: {e}")
        return False
    
    try:
        from filepulse.monitor import FileSystemMonitor
        print("✓ FileSystemMonitor imported")
    except ImportError as e:
        print(f"✗ FileSystemMonitor import failed: {e}")
        return False
    
    try:
        from filepulse.events import FileSystemEvent
        print("✓ FileSystemEvent imported")
    except ImportError as e:
        print(f"✗ FileSystemEvent import failed: {e}")
        return False
    
    try:
        from filepulse.output import create_statistics_collector
        print("✓ create_statistics_collector imported")
    except ImportError as e:
        print(f"✗ create_statistics_collector import failed: {e}")
        return False
    
    return True

def test_config():
    """Test config instantiation"""
    print("\nTesting config...")
    
    try:
        from filepulse.config import Config
        config = Config()
        print(f"✓ Config created: paths={config.monitoring_paths}")
        print(f"✓ Events: {config.monitoring_events}")
        print(f"✓ Recursive: {config.is_recursive}")
        print(f"✓ Include patterns: {config.include_patterns}")
        print(f"✓ Exclude patterns: {config.exclude_patterns}")
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        traceback.print_exc()
        return False

def test_gui_basic():
    """Test basic GUI creation"""
    print("\nTesting basic GUI...")
    
    try:
        import tkinter as tk
        root = tk.Tk()
        root.title("FilePulse Test")
        root.geometry("400x300")
        
        tk.Label(root, text="FilePulse GUI Test", font=('Arial', 16)).pack(pady=20)
        tk.Label(root, text="If you can see this, basic GUI works!").pack(pady=10)
        
        def close_test():
            root.quit()
            root.destroy()
        
        tk.Button(root, text="Close Test", command=close_test).pack(pady=20)
        
        # Auto-close after 3 seconds
        root.after(3000, close_test)
        
        print("✓ Basic GUI window created, showing for 3 seconds...")
        root.mainloop()
        print("✓ Basic GUI test completed")
        return True
    except Exception as e:
        print(f"✗ Basic GUI test failed: {e}")
        traceback.print_exc()
        return False

def test_filepulse_gui():
    """Test FilePulse GUI creation"""
    print("\nTesting FilePulse GUI...")
    
    try:
        from filepulse.gui import FilePulseGUI
        import tkinter as tk
        
        root = tk.Tk()
        app = FilePulseGUI(root)
        print("✓ FilePulse GUI created")
        
        # Auto-close after 2 seconds
        def close_app():
            root.quit()
            root.destroy()
        
        root.after(2000, close_app)
        root.mainloop()
        print("✓ FilePulse GUI test completed")
        return True
    except Exception as e:
        print(f"✗ FilePulse GUI test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("FilePulse GUI Debug Test")
    print("=" * 40)
    
    success = True
    
    if not test_imports():
        success = False
    
    if not test_config():
        success = False
    
    if not test_gui_basic():
        success = False
    
    if not test_filepulse_gui():
        success = False
    
    print("\n" + "=" * 40)
    if success:
        print("✓ All tests passed! GUI should work.")
    else:
        print("✗ Some tests failed. Check the errors above.")
    
    return success

if __name__ == '__main__':
    main()
