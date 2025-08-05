#!/usr/bin/env python3
"""
Entry point for FilePulse GUI - handles imports for standalone executables
"""

import sys
import os
from pathlib import Path

# Ensure filepulse module can be imported
current_dir = Path(__file__).parent
if current_dir.name == 'filepulse':
    # We're in the filepulse directory, add parent to path
    sys.path.insert(0, str(current_dir.parent))
else:
    # We're in the root directory, add current to path
    sys.path.insert(0, str(current_dir))

# Now import and run the GUI
try:
    from filepulse.gui import main
    if __name__ == '__main__':
        main()
except ImportError as e:
    print(f"Error importing FilePulse GUI: {e}")
    print("Please ensure FilePulse is properly installed.")
    sys.exit(1)
