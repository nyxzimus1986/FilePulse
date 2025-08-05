"""
Memory Limit Test for FilePulse GUI
This script helps you test and see the memory limit functionality in action.
"""

import sys
import os
sys.path.insert(0, '.')

from filepulse.gui import FilePulseGUI
import tkinter as tk

def main():
    print("=" * 60)
    print("FILEPULSE MEMORY LIMIT TEST")
    print("=" * 60)
    print()
    print("Follow these steps to see the memory limit in action:")
    print()
    print("1. The GUI will open with debug output enabled")
    print("2. Go to the 'Configuration' tab")
    print("3. Set 'Memory Limit (MB)' to a low value like 30 or 35")
    print("4. Click 'Apply Settings'")
    print("5. Go to the 'Monitor' tab and click 'Start Monitoring'")
    print("6. Go to the 'Statistics' tab - you'll see memory usage info")
    print("7. Create/modify files in the monitored directory")
    print("8. Watch the console output and Statistics tab for memory limit messages")
    print()
    print("What to look for:")
    print("- Console messages like '[FilePulse] MEMORY LIMIT EXCEEDED'")
    print("- Memory usage percentage in Statistics tab")
    print("- Resource Monitor status showing 'ACTIVE'")
    print()
    print("Current Python process memory usage:")
    
    try:
        import psutil
        process = psutil.Process()
        current_mem = process.memory_info().rss / 1024 / 1024
        print(f"- Starting memory: {current_mem:.1f} MB")
        print(f"- Try setting limit to: {max(25, int(current_mem * 0.8))} MB")
    except:
        print("- Install psutil to see current memory usage")
    
    print()
    print("Starting FilePulse GUI...")
    print("=" * 60)
    
    root = tk.Tk()
    app = FilePulseGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
