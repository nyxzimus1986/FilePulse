#!/usr/bin/env python3
"""
Simple GUI test - launch GUI and create test files
"""

import sys
import os
import time
import threading
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, '.')

def create_test_files():
    """Create test files after GUI starts"""
    print("Waiting 5 seconds for GUI to start...")
    time.sleep(5)
    
    print("Creating test files in current directory...")
    
    # Create files in current directory
    for i in range(3):
        test_file = Path(f"gui_test_{i}.txt")
        test_file.write_text(f"Test file {i} created at {time.time()}")
        print(f"Created: {test_file}")
        time.sleep(2)
        
        # Modify the file
        test_file.write_text(f"Test file {i} modified at {time.time()}")
        print(f"Modified: {test_file}")
        time.sleep(1)
    
    print("Test file creation completed")

def main():
    """Launch GUI and create test files"""
    # Start file creation in background
    file_thread = threading.Thread(target=create_test_files, daemon=True)
    file_thread.start()
    
    # Launch GUI
    try:
        from filepulse.gui import main as gui_main
        print("🚀 Launching FilePulse GUI with test file creation...")
        gui_main()
    except Exception as e:
        print(f"Error launching GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
