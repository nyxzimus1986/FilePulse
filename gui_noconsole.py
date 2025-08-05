#!/usr/bin/env python3
"""
Simple test entry point for FilePulse GUI without console
"""

import sys
import os
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import traceback

def main():
    try:
        # Ensure filepulse module can be imported
        current_dir = Path(__file__).parent
        sys.path.insert(0, str(current_dir))
        
        # Test basic tkinter first
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        try:
            # Try to import FilePulse GUI
            from filepulse.gui import main as gui_main
            root.destroy()  # Clean up test window
            gui_main()  # Run the actual GUI
            
        except ImportError as e:
            messagebox.showerror("Import Error", 
                               f"Failed to import FilePulse GUI:\n{e}\n\nPlease check the installation.")
            root.destroy()
            
    except Exception as e:
        # Show error in a message box since there's no console
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("FilePulse Error", 
                               f"Error starting FilePulse:\n{e}\n\nSee the console for more details.")
            root.destroy()
        except:
            # If even tkinter fails, write to a log file
            with open("filepulse_error.log", "w") as f:
                f.write(f"FilePulse GUI Error: {e}\n")
                f.write(traceback.format_exc())

if __name__ == '__main__':
    main()
