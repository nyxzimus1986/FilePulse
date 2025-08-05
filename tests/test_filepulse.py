#!/usr/bin/env python3
"""
Quick test script for FilePulse
"""

import sys
import os
import tempfile
import time
from pathlib import Path

# Add current directory to path
sys.path.insert(0, '.')

def test_basic_functionality():
    """Test basic FilePulse functionality"""
    print("Testing FilePulse basic functionality...")
    
    try:
        # Test imports
        from filepulse.config import Config
        from filepulse.events import FileSystemEvent, EventFilter
        from filepulse.monitor import FileSystemMonitor
        print("✓ All imports successful")
        
        # Test configuration
        config = Config()
        print(f"✓ Configuration loaded with paths: {config.monitoring_paths}")
        
        # Test event creation
        event = FileSystemEvent('created', '/test/path', is_directory=False)
        print(f"✓ Event created: {event}")
        
        # Test event filtering
        event_filter = EventFilter(config)
        should_process = event_filter.should_process_event(event)
        print(f"✓ Event filtering works: {should_process}")
        
        # Test monitor creation (don't start it)
        monitor = FileSystemMonitor(config)
        status = monitor.get_status()
        print(f"✓ Monitor created with status: {status['is_running']}")
        
        print("\n🎉 All basic tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_import():
    """Test CLI import"""
    try:
        from filepulse.cli import cli
        print("✓ CLI import successful")
        return True
    except Exception as e:
        print(f"❌ CLI import failed: {e}")
        return False

if __name__ == '__main__':
    print("FilePulse Test Suite")
    print("=" * 30)
    
    all_passed = True
    all_passed &= test_basic_functionality()
    all_passed &= test_cli_import()
    
    if all_passed:
        print("\n🎉 All tests passed! FilePulse is ready to use.")
        
        print("\nQuick Start Commands:")
        print("1. Monitor current directory:")
        print("   python -c \"import sys; sys.path.insert(0, '.'); from filepulse.cli import main; main()\" monitor .")
        
        print("\n2. Create a config file:")
        print("   python -c \"import sys; sys.path.insert(0, '.'); from filepulse.cli import main; main()\" init-config filepulse.yaml")
        
        print("\n3. Monitor with custom events:")
        print("   python -c \"import sys; sys.path.insert(0, '.'); from filepulse.cli import main; main()\" monitor . --events created,modified")
        
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)
