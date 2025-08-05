#!/usr/bin/env python3
"""
Simple test to verify monitoring works with GUI setup
"""

import sys
import os
import time
import threading

# Add current directory to Python path
sys.path.insert(0, '.')

from filepulse.config import Config
from filepulse.monitor import FileSystemMonitor
from filepulse.events import FileSystemEvent

def test_gui_monitoring():
    """Test monitoring with GUI-like setup"""
    
    print("Testing GUI-like monitoring setup...")
    
    # Create config like GUI does
    config = Config()
    config.set('monitoring.paths', ['.'])
    config.set('monitoring.events', ['created', 'modified', 'deleted', 'moved'])
    config.set('performance.memory_limit_mb', 30)  # Low for testing
    config.set('performance.batch_events', True)
    
    print(f"Config memory limit: {config.get('performance.memory_limit_mb')} MB")
    
    # Track events received
    events_received = []
    
    # Create GUI-style output handler
    def gui_output_handler(events):
        print(f"GUI handler received {len(events)} events")
        for event in events:
            print(f"Event: {event}")
            events_received.append(event)
    
    # Create monitor like GUI does
    monitor = FileSystemMonitor(config)
    print(f"Monitor memory limit: {monitor.resource_monitor.memory_limit_mb} MB")
    
    # Add handler
    monitor.event_handler.add_output_handler(gui_output_handler)
    print(f"Output handlers: {len(monitor.event_handler.output_handlers)}")
    
    # Start monitoring
    print("Starting monitor...")
    monitor.start()
    
    # Create test files to generate events
    print("Creating test files...")
    test_file = "monitor_test.txt"
    
    # Create file
    with open(test_file, 'w') as f:
        f.write("test content")
    time.sleep(1)
    
    # Modify file  
    with open(test_file, 'a') as f:
        f.write("\nmodified")
    time.sleep(1)
    
    # Delete file
    if os.path.exists(test_file):
        os.remove(test_file)
    time.sleep(1)
    
    # Force flush any pending events
    monitor.event_handler.flush()
    time.sleep(1)
    
    # Stop monitoring
    print("Stopping monitor...")
    monitor.stop()
    
    print(f"\nTest Results:")
    print(f"Events received: {len(events_received)}")
    for i, event in enumerate(events_received):
        print(f"  {i+1}: {event}")
    
    if events_received:
        print("✓ Monitoring is working!")
    else:
        print("✗ No events received - monitoring issue")

if __name__ == '__main__':
    test_gui_monitoring()
