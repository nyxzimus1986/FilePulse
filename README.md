#  FilePulse - Clean & Simple

**FilePulse** is a cross-platform filesystem monitoring application with a modern GUI. This version removes all splash screen complexity for instant, reliable startup.

##  Features

- **Instant Startup**: No splash screens, animations, or delays
- **Clean Interface**: Modern tkinter GUI with professional appearance
- **Reliable**: Simplified launcher eliminates freezing issues
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **VS Code Ready**: Complete development workspace included

##  Quick Start

### **Launch FilePulse**

**Option 1 - Simple Python:**
`ash
python filepulse.py
`

**Option 2 - Batch File (Windows):**
`ash
run_filepulse.bat
`

**Option 3 - VS Code Task:**
1. Open Workspace/ folder in VS Code
2. Press Ctrl+Shift+P
3. Type "Tasks: Run Task"
4. Select **"Launch FilePulse"**

### **Development**

**Debug in VS Code:**
1. Open Workspace/ folder
2. Press F5 or go to Run & Debug
3. Select "Launch FilePulse (Debug)"

##  Project Structure

`
 filepulse.py            #  MAIN LAUNCHER (Clean & Simple)
 run_filepulse.bat      # Windows batch launcher
 filepulse/             # Main application module
    gui.py             # GUI application class
 assets/                # Images and resources
 archive/               # Old launchers (with splash screens)
 Workspace/             # VS Code development environment
    .vscode/           # VS Code tasks, debug config, settings
    README.md          # Workspace documentation
 scripts/               # Alternative launchers
 build-tools/           # Build and packaging scripts
 tests/                 # Test files
 development/           # Experimental code
`

##  Development Setup

1. **Clone/Download** FilePulse project
2. **Install Dependencies:** pip install -r requirements.txt
3. **Launch:** python filepulse.py
4. **Develop:** Open Workspace/ in VS Code for full IDE experience

##  What's New - Clean Version

-  **Removed all splash screens** - Instant startup
-  **Simplified launcher** - Single ilepulse.py file
-  **Eliminated freezing issues** - No complex animations
-  **Professional startup** - Clean, fast, reliable
-  **Archived old versions** - Available in rchive/ folder

##  Why This Version?

The previous versions had complex splash screen animations that could freeze during startup. This clean version:

- **Starts immediately** - No waiting for animations
- **Never freezes** - Simple, direct GUI launch
- **More professional** - Clean startup experience
- **Easier to maintain** - Simplified codebase

##  Legacy Launchers

Old splash screen launchers are preserved in rchive/:
- ilepulse_launcher.py - Transparent bottom fade splash
- direct_launcher.py - Direct launch with basic splash
- launch_gui_transparent.py - Transparent overlay splash

Use the legacy versions if you prefer animated startup screens.

---

**Ready to use!** Just run python filepulse.py and start monitoring your filesystem! 
