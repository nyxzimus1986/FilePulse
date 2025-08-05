#!/usr/bin/env python3
"""
FilePulse - Direct GUI Launcher
Simple launcher that directly starts the GUI without splash screen complications
"""

import tkinter as tk
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Launch FilePulse GUI directly"""
    try:
        print("🚀 Starting FilePulse GUI...")
        
        # Import and create GUI
        from filepulse.gui import FilePulseGUI
        
        # Create root window
        root = tk.Tk()
        root.title("FilePulse - Filesystem Monitor")
        root.geometry("900x700")
        root.minsize(800, 600)
        
        # Create GUI application
        app = FilePulseGUI(root)
        print("✅ GUI created successfully")
        
        # Start main loop
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        try:
            tk.messagebox.showerror("Import Error", 
                                   f"Failed to import FilePulse GUI:\n\n{e}\n\n"
                                   f"Please check that the filepulse module is properly installed.")
        except:
            pass
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
        try:
            tk.messagebox.showerror("Error", f"Failed to start FilePulse:\n\n{e}")
        except:
            pass

if __name__ == "__main__":
    main()
