<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# FilePulse Project - Copilot Instructions

## Project Overview
FilePulse is a cross-platform filesystem monitoring application with a GUI built using Python tkinter and PIL for image processing.

## Project Structure
- `filepulse/` - Main application module with GUI components
- `scripts/` - Launcher scripts and entry points
- `build-tools/` - Build scripts, batch files, and PyInstaller specs
- `assets/` - Images, splash screens, and other assets
- `tests/` - Test files and debugging utilities
- `development/` - Experimental and development files

## Key Files
- `filepulse_launcher.py` - Main application launcher with transparent splash screen
- `run_filepulse.bat` - Windows batch launcher
- `filepulse/gui.py` - Main GUI application class
- `assets/splash/` - Splash screen images with transparency support

## Technologies Used
- **Python 3.8+** - Main programming language
- **tkinter** - GUI framework
- **PIL/Pillow** - Image processing and transparency effects
- **pathlib** - Modern path handling
- **PyInstaller** - Executable building

## Development Guidelines
- Use pathlib for all file path operations
- Implement proper error handling with try/catch blocks
- Add flush=True to print statements for immediate output
- Use transparent fade effects for professional UI appearance
- Maintain cross-platform compatibility
- Follow the existing code style and structure

## Common Tasks
- Launch with splash: `python filepulse_launcher.py`
- Run from scripts: `python scripts/launch_gui_transparent.py`
- Build executable: Use batch files in `build-tools/`
- Test functionality: Files in `tests/` directory
