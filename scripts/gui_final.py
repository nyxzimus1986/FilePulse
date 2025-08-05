#!/usr/bin/env python3
"""
Entry point for FilePulse GUI with advanced splash screen
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
            # Import and show advanced splash screen
            from filepulse.advanced_splash import AdvancedFilePulseSplash
            
            # Show splash screen
            splash = AdvancedFilePulseSplash()
            splash_window = splash.show(duration=4.0)
            
            # Load main GUI in background
            def load_main_gui():
                try:
                    # Give splash time to show loading messages
                    time.sleep(2.5)
                    
                    # Import main GUI components
                    from filepulse.gui import FilePulseGUI
                    
                    # Wait a bit more for splash to complete
                    time.sleep(1.5)
                    
                    # Close splash screen
                    splash.close_splash()
                    
                    # Show main GUI
                    root.deiconify()  # Show the main window
                    root.title("FilePulse - Filesystem Monitor")
                    
                    # Set window icon (if available)
                    try:
                        # Try to set a window icon
                        root.iconname("FilePulse")
                    except:
                        pass
                    
                    # Create and run the GUI
                    app = FilePulseGUI(root)
                    
                except Exception as e:
                    # Close splash if there's an error
                    try:
                        splash.close_splash()
                    except:
                        pass
                    
                    # Show error dialog
                    root.deiconify()
                    messagebox.showerror("FilePulse Error", 
                                       f"Failed to load FilePulse GUI:\n\n{e}")
                    root.quit()
            
            # Start loading in background thread
            loading_thread = threading.Thread(target=load_main_gui, daemon=True)
            loading_thread.start()
            
            # Start the main event loop
            root.mainloop()
            
        except ImportError as e:
            # Handle import errors
            messagebox.showerror("Import Error", 
                               f"Failed to import FilePulse components:\n\n{e}\n\n"
                               f"Please ensure all dependencies are installed.")
            root.destroy()
            
    except Exception as e:
        # Handle any other errors
        error_msg = f"Critical error starting FilePulse: {e}"
        
        # Try to show error dialog
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("FilePulse Critical Error", 
                               f"{error_msg}\n\nCheck filepulse_error.log for details.")
            root.destroy()
        except:
            # If GUI fails, just print to console
            print(error_msg)
        
        # Write detailed error to log file
        try:
            with open("filepulse_error.log", "w", encoding="utf-8") as f:
                f.write("FilePulse Critical Error Log\n")
                f.write("=" * 40 + "\n\n")
                f.write(f"Error: {e}\n")
                f.write(f"Python version: {sys.version}\n")
                f.write(f"Platform: {sys.platform}\n")
                f.write(f"Current directory: {os.getcwd()}\n")
                f.write(f"Script location: {__file__}\n")
                f.write(f"Python path: {sys.path[:5]}\n")  # First 5 entries
                f.write("\nFull traceback:\n")
                f.write(traceback.format_exc())
                f.write("\n" + "=" * 40 + "\n")
        except Exception as log_error:
            print(f"Could not write error log: {log_error}")

if __name__ == '__main__':
    main()
