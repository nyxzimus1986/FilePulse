#!/usr/bin/env python3
"""
Entry point for FilePulse GUI with splash screen
"""

import sys
import os
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import traceback
import threading
import time

def main():
    try:
        # Ensure filepulse module can be imported
        current_dir = Path(__file__).parent
        sys.path.insert(0, str(current_dir))
        
        # Create root window (hidden initially)
        root = tk.Tk()
        root.withdraw()  # Hide main window during loading
        
        try:
            # Import splash screen
            from filepulse.splash import FilePulseSplash
            
            # Show splash screen
            splash = FilePulseSplash()
            splash_window = splash.show(duration=3.0)
            
            # Import main GUI (this might take a moment)
            def load_main_gui():
                try:
                    time.sleep(1.5)  # Give splash time to display
                    from filepulse.gui import FilePulseGUI
                    
                    # Close splash screen
                    splash.close_splash()
                    
                    # Show main GUI
                    root.deiconify()  # Show the main window
                    app = FilePulseGUI(root)
                    
                except Exception as e:
                    splash.close_splash()
                    messagebox.showerror("Error", f"Failed to load FilePulse GUI: {e}")
                    root.quit()
            
            # Load GUI in background while splash is showing
            threading.Thread(target=load_main_gui, daemon=True).start()
            
            # Start the main loop
            root.mainloop()
            
        except ImportError as e:
            messagebox.showerror("Import Error", 
                               f"Failed to import FilePulse components:\n{e}\n\nPlease check the installation.")
            root.destroy()
            
    except Exception as e:
        # Show error in a message box since there's no console
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("FilePulse Error", 
                               f"Error starting FilePulse:\n{e}\n\nCheck filepulse_error.log for details.")
            root.destroy()
        except:
            pass
        
        # Write detailed error to log file
        try:
            with open("filepulse_error.log", "w") as f:
                f.write(f"FilePulse GUI Error: {e}\n")
                f.write(f"Python version: {sys.version}\n")
                f.write(f"Current directory: {os.getcwd()}\n")
                f.write(f"Script location: {__file__}\n")
                f.write("Full traceback:\n")
                f.write(traceback.format_exc())
        except:
            pass

if __name__ == '__main__':
    main()
