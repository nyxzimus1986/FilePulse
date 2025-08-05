# FilePulse - Filesystem Monitor

A lightweight, cross-platform filesystem monitor with minimal resource usage and an intuitive GUI interface.

![FilePulse GUI](https://img.shields.io/badge/GUI-Tkinter-blue) ![Python](https://img.shields.io/badge/Python-3.8+-green) ![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## Features

### 🔍 **Real-time Monitoring**
- Monitor file and directory changes in real-time
- Track create, modify, delete, and move operations
- Recursive directory monitoring support

### 🎯 **Smart Event Classification**
- Automatically categorizes events as user-initiated or system-generated
- Separate tabs for User Changes, System Changes, and All Events
- Intelligent filtering to reduce noise

### 🖥️ **User-Friendly GUI**
- Clean, tabbed interface built with Tkinter
- Live event counters and statistics
- Color-coded event types for easy identification
- Export logs to text files

### ⚡ **Performance Optimized**
- Configurable memory limits with automatic cleanup
- Event batching to reduce resource usage
- CPU throttling options for minimal system impact
- Real-time memory and performance monitoring

### 🔧 **Highly Configurable**
- Flexible include/exclude pattern matching
- Multiple output formats (console, file, JSON)
- System-wide monitoring capabilities
- Customizable event filtering

## Quick Start

### Installation

```bash
# Install dependencies
pip install watchdog psutil pyyaml click colorama python-dateutil

# Or install from requirements.txt
pip install -r requirements.txt
```

### Basic Usage

Since the package is in development mode, use these commands:

```bash
# Monitor current directory (Windows)
python -c "import sys; sys.path.insert(0, '.'); from filepulse.cli import main; main()" monitor .

# 🌐 SYSTEM-WIDE MONITORING (monitors Desktop, Documents, Downloads, etc.)
python -c "import sys; sys.path.insert(0, '.'); from filepulse.cli import main; main()" monitor --system-wide --stats

# Monitor with specific events
python -c "import sys; sys.path.insert(0, '.'); from filepulse.cli import main; main()" monitor . --events created,modified

# Monitor with statistics
python -c "import sys; sys.path.insert(0, '.'); from filepulse.cli import main; main()" monitor . --stats

# Create a configuration file
python -c "import sys; sys.path.insert(0, '.'); from filepulse.cli import main; main()" init-config filepulse.yaml

# Run with config file
python -c "import sys; sys.path.insert(0, '.'); from filepulse.cli import main; main()" monitor . --config filepulse.yaml

# Show available system paths
python -c "import sys; sys.path.insert(0, '.'); from filepulse.cli import main; main()" system-paths

# Launch GUI (includes system-wide option)
python -c "import sys; sys.path.insert(0, '.'); from filepulse.cli import main; main()" gui
```

Or use the convenient launcher scripts:
```bash
python test_filepulse.py       # Runs tests and shows usage examples
python test_system_wide.py     # Tests system-wide monitoring setup
python launch_gui.py           # Launch GUI application
gui.bat                        # Windows batch launcher for GUI
```

## 🎨 **Design Tools**

FilePulse includes professional design tools for creating custom icons and splash screens:

### Icon Generator
- **Custom Image Support**: Load your own PNG, JPG, or other image files
- **Multiple Styles**: Modern, Classic, Minimal, and 3D icon styles
- **Image Controls**: Adjust opacity (0-100%) and scale (10-200%)
- **Color Themes**: Built-in presets (Blue, Green, Orange, Purple, Dark)
- **Text Overlays**: Add custom text with automatic outline
- **Export Options**: PNG or ICO formats in multiple sizes

### Splash Screen Generator  
- **Custom Backgrounds**: Load high-resolution background images
- **Image Effects**: Opacity, blur (0-20), and scale (50-200%) controls
- **Gradient Overlays**: Blend custom images with color gradients
- **Animation Options**: Pulse, Fade, Slide, Rotate, Scale effects
- **Code Export**: Generate standalone Python splash screen code
- **Theme Presets**: Professional color combinations

### Quick Start Design Tools:
```bash
# Launch icon generator
python tools/icon_generator.py
run-icon-generator.bat          # Windows

# Launch splash screen generator  
python tools/splash_generator.py
run-splash-generator.bat        # Windows

# Create sample images for testing
python demo/create_sample_images.py
```

Try the demo images in the `demo/` folder to test custom image loading!

### Configuration

Create a configuration file to customize monitoring behavior:

```yaml
# config/monitor.yaml
monitoring:
  paths:
    - "/home/user/Documents"
    - "/home/user/Projects"
  events:
    - created
    - modified
    - deleted
  filters:
    include_patterns:
      - "*.py"
      - "*.js"
      - "*.md"
    exclude_patterns:
      - "*.tmp"
      - "__pycache__"
      - ".git"
  output:
    console: true
    log_file: "/var/log/filepulse.log"
    json_output: false
```

## Project Structure

```
filepulse/
├── filepulse/
│   ├── __init__.py
│   ├── cli.py              # Command-line interface
│   ├── monitor.py          # Core monitoring logic
│   ├── config.py           # Configuration management
│   ├── events.py           # Event handling and filtering
│   ├── output.py           # Output formatters
│   └── utils.py           # Utility functions
├── config/
│   └── default.yaml       # Default configuration
├── tests/
│   └── ...
├── setup.py
├── requirements.txt
└── README.md
```

## Development

1. Clone the repository
2. Install in development mode: `pip install -e .`
3. Run tests: `python -m pytest tests/`
4. Format code: `black filepulse/`

## License

MIT License - see LICENSE file for details.
