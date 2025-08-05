#!/usr/bin/env python3
"""
GUI Launcher for FilePulse
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, '.')

def launch_gui():
    """Launch the FilePulse GUI"""
    try:
        from filepulse.gui import main
        print("🚀 Launching FilePulse GUI...")
        main()
    except ImportError as e:
        print(f"❌ Error: GUI dependencies not available: {e}")
        print("GUI requires tkinter which should be included with Python.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    launch_gui()
