#!/usr/bin/env python3
"""
FilePulse - Clean Launcher
Simple, fast startup without splash screen animations.
"""
import sys
import tkinter as tk
from pathlib import Path


class FilePulseLauncher:
    """Clean FilePulse launcher without splash screen."""
    
    def __init__(self):
        self.setup_paths()
        
    def setup_paths(self):
        """Add FilePulse module to Python path."""
        current_dir = Path(__file__).parent.resolve()
        if str(current_dir) not in sys.path:
            sys.path.insert(0, str(current_dir))
            
        # Verify FilePulse module exists
        filepulse_path = current_dir / "filepulse"
        if not filepulse_path.exists():
            raise ImportError(f"FilePulse module not found at: {filepulse_path}")
    
    def launch(self):
        """Launch FilePulse GUI directly."""
        print(" Starting FilePulse...", flush=True)
        
        try:
            # Import FilePulse GUI
            from filepulse.gui import FilePulseGUI
            print(" FilePulse module loaded", flush=True)
            
            # Create main window
            root = tk.Tk()
            root.title("FilePulse - Filesystem Monitor")
            root.geometry("900x700")
            root.minsize(800, 600)
            
            # Set window icon if available
            try:
                icon_path = Path(__file__).parent / "assets" / "icon.ico"
                if icon_path.exists():
                    root.iconbitmap(str(icon_path))
            except:
                pass  # Ignore icon errors
            
            # Create and start application
            print(" Creating FilePulse application...", flush=True)
            app = FilePulseGUI(root)
            print(" FilePulse ready!", flush=True)
            
            # Start GUI main loop
            root.mainloop()
            
        except ImportError as e:
            self.show_error("Import Error", 
                           f"Failed to import FilePulse:\n\n{e}\n\n"
                           f"Please ensure FilePulse is properly installed.")
        except Exception as e:
            self.show_error("Startup Error", 
                           f"Failed to start FilePulse:\n\n{e}")
    
    def show_error(self, title, message):
        """Show error dialog."""
        print(f" {title}: {message}", flush=True)
        try:
            import tkinter.messagebox as msgbox
            root = tk.Tk()
            root.withdraw()  # Hide root window
            msgbox.showerror(title, message)
            root.destroy()
        except:
            pass  # Ignore GUI errors when showing errors


def main():
    """Main entry point."""
    try:
        launcher = FilePulseLauncher()
        launcher.launch()
    except Exception as e:
        print(f" Fatal error: {e}", flush=True)
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
