#!/usr/bin/env python3
"""
Example usage of FilePulse filesystem monitor
"""

import os
import sys
import time
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, '.')

from filepulse.config import Config
from filepulse.monitor import FileSystemMonitor

def main():
    """Example of using FilePulse programmatically"""
    
    print("FilePulse Example - Filesystem Monitor")
    print("=" * 50)
    
    # Create a configuration
    config = Config()
    
    # Configure monitoring settings
    config.set('monitoring.paths', ['.'])
    config.set('monitoring.events', ['created', 'modified', 'deleted'])
    config.set('output.console_format', 'detailed')
    
    print(f"Monitoring paths: {config.monitoring_paths}")
    print(f"Monitoring events: {config.monitoring_events}")
    print("Press Ctrl+C to stop monitoring")
    print("-" * 50)
    
    # Create and start monitor
    monitor = FileSystemMonitor(config)
    
    try:
        monitor.run()
    except KeyboardInterrupt:
        print("\nStopping monitor...")
        monitor.stop()
        print("Monitor stopped.")

if __name__ == '__main__':
    main()
