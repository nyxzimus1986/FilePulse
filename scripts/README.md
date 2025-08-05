# Scripts Directory

This directory contains various launcher scripts and entry points for FilePulse.

## Main Launchers
- `launch_gui_transparent.py` - Main GUI launcher with transparent splash screen (RECOMMENDED)
- `launch_gui_with_splash.py` - GUI launcher with standard splash screen
- `launch_simple_splash.py` - Simple splash screen implementation

## Alternative Launchers
- `launch_gui_animated.py` - Animated splash screen version
- `launch_gui_ultra_simple.py` - Minimal launcher
- `launch_direct_gui.py` - Direct GUI launch without splash

## Entry Points
- `gui_entry.py` - GUI application entry point
- `cli_entry.py` - CLI application entry point
- `gui_final.py` - Final GUI implementation
- `gui_noconsole.py` - GUI without console window

## Usage
For the best experience, use the main launcher in the root directory:
```bash
python ../filepulse_launcher.py
```

Or run any specific launcher directly:
```bash
python launch_gui_transparent.py
```
