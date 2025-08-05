#!/usr/bin/env python3
"""
Test both memory limit and event display issues
"""

import sys
import os
import time
import threading

# Add current directory to Python path
sys.path.insert(0, '.')

from filepulse.config import Config
from filepulse.monitor import FileSystemMonitor

def test_memory_and_events():
    """Test memory limit and event processing"""
    
    print("Testing Memory Limit and Event Processing")
    print("=" * 50)
    
    # Create config with very low memory limit
    config = Config()
    config.set('monitoring.paths', ['.'])
    config.set('monitoring.events', ['created', 'modified', 'deleted'])
    config.set('performance.memory_limit_mb', 15)  # Very low for testing
    config.set('performance.batch_events', True)
    config.set('performance.batch_timeout', 0.2)  # Fast batching
    config.set('performance.max_events_per_batch', 5)  # Small batches
    
    events_received = []
    
    def test_handler(events):
        print(f"Handler received {len(events)} events")
        events_received.extend(events)
        for event in events:
            print(f"  Event: {event}")
    
    # Create monitor
    monitor = FileSystemMonitor(config)
    monitor.event_handler.add_output_handler(test_handler)
    
    print(f"Memory limit: {monitor.resource_monitor.memory_limit_mb} MB")
    
    # Start monitoring
    monitor.start()
    
    # Let it run and create files
    print("\nCreating test files...")
    for i in range(3):
        filename = f"test_mem_{i}.txt"
        with open(filename, 'w') as f:
            f.write(f"Test file {i} content")
        time.sleep(0.5)
        
        # Modify
        with open(filename, 'a') as f:
            f.write(f"\nModified {i}")
        time.sleep(0.5)
    
    # Wait for events
    time.sleep(2)
    monitor.event_handler.flush()
    time.sleep(1)
    
    # Cleanup
    for i in range(3):
        filename = f"test_mem_{i}.txt"
        if os.path.exists(filename):
            os.remove(filename)
            time.sleep(0.5)
    
    time.sleep(2)
    monitor.event_handler.flush()
    time.sleep(1)
    
    monitor.stop()
    
    print(f"\nResults:")
    print(f"Total events received: {len(events_received)}")
    print(f"Memory limit working: {'YES' if monitor.resource_monitor.memory_limit_mb == 15 else 'NO'}")
    
    return len(events_received) > 0

if __name__ == '__main__':
    success = test_memory_and_events()
    if success:
        print("\n✓ Test PASSED - Events are being processed")
    else:
        print("\n✗ Test FAILED - No events received")
