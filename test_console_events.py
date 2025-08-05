#!/usr/bin/env python3
"""
Test script to debug GUI event handling
"""

import sys
import os
import time
import tempfile
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, '.')

def create_test_events():
    """Create some test files to trigger events"""
    print("Creating test files to trigger filesystem events...")
    
    test_dir = Path(tempfile.gettempdir()) / "filepulse_test"
    test_dir.mkdir(exist_ok=True)
    
    # Create a file
    test_file = test_dir / "test_file.txt"
    test_file.write_text("Hello FilePulse!")
    print(f"Created: {test_file}")
    
    time.sleep(1)
    
    # Modify the file
    test_file.write_text("Hello FilePulse! Modified")
    print(f"Modified: {test_file}")
    
    time.sleep(1)
    
    # Create another file
    test_file2 = test_dir / "test_file2.txt"
    test_file2.write_text("Another test file")
    print(f"Created: {test_file2}")
    
    time.sleep(1)
    
    # Delete a file
    test_file.unlink()
    print(f"Deleted: {test_file}")
    
    return str(test_dir)

def test_console_monitoring():
    """Test console monitoring to verify events are working"""
    print("Testing console monitoring first...")
    
    from filepulse.config import Config
    from filepulse.monitor import FileSystemMonitor
    
    # Create config for temp directory
    config = Config()
    test_dir = create_test_events()
    config.set('monitoring.paths', [test_dir])
    config.set('monitoring.events', ['created', 'modified', 'deleted'])
    
    # Create console output handler
    def console_handler(events):
        for event in events:
            print(f"CONSOLE EVENT: {event}")
    
    # Start monitoring
    monitor = FileSystemMonitor(config)
    monitor.event_handler.add_output_handler(console_handler)
    
    print(f"Starting console monitor for: {test_dir}")
    monitor.start()
    
    # Create more test events
    time.sleep(2)
    print("Creating more test events...")
    test_file3 = Path(test_dir) / "console_test.txt"
    test_file3.write_text("Console test")
    
    time.sleep(1)
    test_file3.write_text("Console test modified")
    
    time.sleep(1)
    test_file3.unlink()
    
    # Wait and flush
    time.sleep(2)
    monitor.event_handler.flush()
    monitor.stop()
    
    print("Console monitoring test completed")

if __name__ == '__main__':
    try:
        test_console_monitoring()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
