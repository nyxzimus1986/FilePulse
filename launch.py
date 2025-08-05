#!/usr/bin/env python3
"""
Launch FilePulse filesystem monitor
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, '.')

def launch_filepulse():
    """Launch FilePulse with default settings"""
    try:
        from filepulse.cli import main
        
        print("🚀 Launching FilePulse Filesystem Monitor...")
        print("   Monitoring current directory with statistics")
        print("   Press Ctrl+C to stop monitoring")
        print()
        
        # Simulate command line arguments
        sys.argv = [
            'filepulse',
            'monitor', 
            '.',
            '--stats',
            '--events', 'created,modified,deleted,moved'
        ]
        
        # Launch the CLI
        main()
        
    except KeyboardInterrupt:
        print("\n👋 FilePulse stopped by user")
    except Exception as e:
        print(f"❌ Error launching FilePulse: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    launch_filepulse()
