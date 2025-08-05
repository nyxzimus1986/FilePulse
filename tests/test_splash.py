#!/usr/bin/env python3
"""
Test the FilePulse splash screen
"""

import sys
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from filepulse.advanced_splash import AdvancedFilePulseSplash
import tkinter as tk

def main():
    print("Testing FilePulse Advanced Splash Screen...")
    
    # Create root window
    root = tk.Tk()
    root.withdraw()  # Hide root window
    
    # Show splash screen
    splash = AdvancedFilePulseSplash()
    splash.show(duration=6.0)  # Show for 6 seconds
    
    print("Splash screen should be visible now...")
    print("It will automatically close after 6 seconds.")
    
    # Start main loop
    root.mainloop()
    
    print("Test completed!")

if __name__ == "__main__":
    main()
