#!/usr/bin/env python3
"""
Test memory limit with GUI
"""

import tkinter as tk
import sys
import os
sys.path.insert(0, '.')

from filepulse.gui import FilePulseGUI

def main():
    print("Starting FilePulse GUI with memory limit testing...")
    print("Instructions:")
    print("1. Go to Configuration tab")
    print("2. Set Memory Limit to 30 MB (current usage is probably around 40-50 MB)")
    print("3. Click 'Apply Settings'")
    print("4. Start monitoring")
    print("5. Go to Statistics tab and watch for memory limit triggers")
    print("6. Create/modify some files to generate events and increase memory usage")
    print()
    
    root = tk.Tk()
    app = FilePulseGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
