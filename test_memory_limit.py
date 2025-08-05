#!/usr/bin/env python3
"""
Test memory limit functionality
"""

import sys
import os
import time

# Add current directory to Python path
sys.path.insert(0, '.')

from filepulse.config import Config
from filepulse.monitor import FileSystemMonitor

def test_memory_limit():
    """Test memory limit configuration and enforcement"""
    
    print("Testing Memory Limit Functionality")
    print("=" * 40)
    
    # Create config with low memory limit for testing
    config = Config()
    config.set('monitoring.paths', ['.'])
    config.set('monitoring.events', ['created', 'modified', 'deleted'])
    config.set('performance.memory_limit_mb', 20)  # Very low for testing
    config.set('performance.batch_events', True)
    config.set('performance.max_events_per_batch', 10)
    
    print(f"Memory limit set to: {config.get('performance.memory_limit_mb')} MB")
    
    # Create monitor
    monitor = FileSystemMonitor(config)
    
    print(f"Resource monitor memory limit: {monitor.resource_monitor.memory_limit_mb} MB")
    print(f"Event handler max batch memory: {monitor.event_handler.max_batch_memory_mb:.2f} MB")
    
    try:
        # Start monitoring
        print("\nStarting monitor...")
        monitor.start()
        
        # Show initial memory usage
        import psutil
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        print(f"Initial memory usage: {memory_mb:.1f} MB")
        
        # Let it run for a short time
        print("Monitoring for 10 seconds...")
        for i in range(10):
            time.sleep(1)
            memory_mb = process.memory_info().rss / 1024 / 1024
            print(f"Memory usage: {memory_mb:.1f} MB", end="")
            if memory_mb > config.get('performance.memory_limit_mb'):
                print(" (EXCEEDS LIMIT - should trigger cleanup)")
            else:
                print(" (within limit)")
    
    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        print("\nStopping monitor...")
        monitor.stop()
        print("Test completed")

if __name__ == '__main__':
    test_memory_limit()
