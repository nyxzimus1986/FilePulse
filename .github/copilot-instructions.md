<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# FilePulse Development Instructions

This is a Python package for system-wide filesystem monitoring with minimal resource usage. The project follows these principles:

## Architecture
- **filepulse/monitor.py**: Core filesystem monitoring using watchdog library
- **filepulse/events.py**: Event handling, filtering, and batching
- **filepulse/config.py**: Configuration management with YAML support
- **filepulse/output.py**: Multiple output formats (console, file, JSON)
- **filepulse/cli.py**: Command-line interface using Click
- **filepulse/utils.py**: Utility functions and helpers

## Key Features
- Real-time filesystem monitoring with configurable events
- Minimal resource usage with CPU/memory monitoring
- Event filtering by patterns, file types, and size
- Batching to reduce noise and improve performance
- Multiple output formats with colored console output
- Cross-platform support (Windows, macOS, Linux)

## Code Style
- Use type hints for all function parameters and return values
- Follow PEP 8 style guidelines
- Use logging for debugging and error reporting
- Handle exceptions gracefully with meaningful error messages
- Optimize for low resource usage

## Dependencies
- watchdog: Filesystem monitoring
- psutil: System resource monitoring
- pyyaml: Configuration file parsing
- click: Command-line interface
- colorama: Cross-platform colored terminal output

## Testing
- Test on multiple platforms
- Test with various file operations (create, modify, delete, move)
- Test resource usage under heavy load
- Test configuration file handling
