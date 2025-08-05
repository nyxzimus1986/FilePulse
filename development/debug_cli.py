#!/usr/bin/env python3
"""
Debug entry point for FilePulse CLI - shows error details
"""

import sys
import os
import traceback
from pathlib import Path

def main():
    try:
        print("FilePulse CLI Debug Version")
        print("=" * 40)
        print(f"Python version: {sys.version}")
        print(f"Current directory: {os.getcwd()}")
        print(f"Script location: {__file__}")
        print(f"Python path: {sys.path[:3]}...")  # Show first 3 entries
        print()
        
        # Try to import filepulse modules one by one
        print("Testing imports...")
        
        try:
            import filepulse
            print("✓ filepulse imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import filepulse: {e}")
            
        try:
            from filepulse.config import Config
            print("✓ filepulse.config imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import filepulse.config: {e}")
            
        try:
            from filepulse.cli import main as cli_main
            print("✓ filepulse.cli imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import filepulse.cli: {e}")
            
        # Try to run the actual CLI
        print("\nAttempting to run CLI...")
        from filepulse.cli import main as cli_main
        cli_main()
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        print("\nPress Enter to exit...")
        input()

if __name__ == '__main__':
    main()
