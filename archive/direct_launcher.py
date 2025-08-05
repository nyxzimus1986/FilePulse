#!/usr/bin/env python3
"""
FilePulse - Direct Launcher (No Splash Screen)
Launches FilePulse GUI directly without splash screen animations
"""
import sys
from pathlib import Path

def main():
    print(' FilePulse - Direct Launch (No Splash)', flush=True)
    
    try:
        # Add current directory to path for imports
        current_dir = Path(__file__).parent
        if str(current_dir) not in sys.path:
            sys.path.insert(0, str(current_dir))
        
        print(f'Current directory: {current_dir}', flush=True)
        
        # Check if filepulse module exists
        filepulse_path = current_dir / 'filepulse'
        if not filepulse_path.exists():
            print(f' FilePulse module not found at: {filepulse_path}', flush=True)
            return False
        
        print(' FilePulse directory found', flush=True)
        
        # Import GUI components
        from filepulse.gui import FilePulseGUI
        print(' GUI module imported successfully', flush=True)
        
        # Create and launch GUI
        import tkinter as tk
        root = tk.Tk()
        root.title('FilePulse - Filesystem Monitor')
        root.geometry('900x700')
        root.minsize(800, 600)
        
        print(' Creating GUI application...', flush=True)
        app = FilePulseGUI(root)
        print(' GUI application created successfully', flush=True)
        print(' Starting FilePulse main loop...', flush=True)
        
        # Start the application
        root.mainloop()
        
    except ImportError as e:
        print(f' Import error: {e}', flush=True)
        import tkinter.messagebox as msgbox
        msgbox.showerror('Import Error', 
                        f'Failed to import FilePulse GUI:\n\n{e}\n\n'
                        f'Please check that the filepulse module is properly installed.')
        return False
    except Exception as e:
        print(f' GUI launch error: {e}', flush=True)
        import traceback
        traceback.print_exc()
        import tkinter.messagebox as msgbox
        msgbox.showerror('Error', f'Failed to launch GUI:\n\n{e}')
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        input('Press Enter to exit...')
