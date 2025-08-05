#!/usr/bin/env python3
"""
Test system-wide monitoring functionality
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, '.')

def test_system_monitoring():
    """Test system-wide monitoring setup"""
    print("Testing FilePulse System-Wide Monitoring...")
    print("=" * 45)
    
    try:
        from filepulse.system_monitor import SystemPathManager, create_system_wide_config
        
        # Test path manager
        path_manager = SystemPathManager()
        
        print("📁 User Directories:")
        user_paths = path_manager.get_user_paths()
        for path in user_paths:
            exists = "✓" if os.path.exists(path) else "✗"
            print(f"  {exists} {path}")
        
        print(f"\n💿 Mounted Drives:")
        drives = path_manager.get_mounted_drives()
        for drive in drives:
            exists = "✓" if os.path.exists(drive) else "✗"
            print(f"  {exists} {drive}")
        
        print(f"\n⚙️  System-Wide Configuration:")
        config = create_system_wide_config(user_paths_only=True)
        print(f"  Paths to monitor: {len(config['monitoring']['paths'])}")
        print(f"  Events: {config['monitoring']['events']}")
        print(f"  Batch events: {config['performance']['batch_events']}")
        
        print(f"\n🎯 Ready for system-wide monitoring!")
        print(f"   Use: python -c \"import sys; sys.path.insert(0, '.'); from filepulse.cli import main; main()\" monitor --system-wide")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_system_monitoring()
