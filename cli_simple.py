#!/usr/bin/env python3
"""
Simple CLI entry point for FilePulse with better error handling
"""

import sys
import os
from pathlib import Path
import traceback

def main():
    try:
        print("FilePulse CLI v0.1.0")
        print("==================")
        
        # Ensure filepulse module can be imported
        current_dir = Path(__file__).parent
        sys.path.insert(0, str(current_dir))
        
        # Try to import and run FilePulse CLI
        from filepulse.cli import main as cli_main
        cli_main()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\nThis might be caused by:")
        print("1. Missing dependencies in the executable")
        print("2. Module path issues")
        print("3. Python version compatibility")
        print(f"\nCurrent Python path: {sys.path[0]}")
        print(f"Script location: {__file__}")
        input("\nPress Enter to exit...")
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        print("\nFull error details:")
        traceback.print_exc()
        input("\nPress Enter to exit...")

if __name__ == '__main__':
    main()
