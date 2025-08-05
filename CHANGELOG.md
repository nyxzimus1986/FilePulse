# Changelog

All notable changes to FilePulse will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial repository setup
- GitHub Actions CI/CD workflows
- Comprehensive documentation

### Changed
- Improved README with detailed feature descriptions
- Enhanced code documentation

### Fixed
- User event detection for manually created folders and files
- Memory limit enforcement functionality
- GUI responsiveness optimizations

## [0.1.0] - 2025-01-05

### Added
- Real-time filesystem monitoring with watchdog
- Tkinter-based GUI interface with tabbed layout
- Command-line interface with Click
- Event classification (user vs system events)
- Configurable memory limits with automatic cleanup
- Event batching and filtering system
- YAML-based configuration management
- Multiple output formats (console, file, JSON)
- Cross-platform support (Windows, macOS, Linux)
- Pattern-based file filtering (include/exclude)
- Resource monitoring and statistics
- Export functionality for event logs
- System-wide monitoring capabilities

### Features
- **Monitor Tab**: Real-time event display with separate tabs for user/system/all events
- **Configuration Tab**: Easy-to-use settings panel with pattern help
- **Statistics Tab**: Live memory usage and performance metrics
- **About Tab**: Application information and version details

### Technical Highlights
- Modular architecture with separation of concerns
- Type hints throughout the codebase
- Comprehensive error handling and logging
- Memory-aware event processing
- GUI-optimized event batching (300ms intervals)
- Resource monitor with automatic cleanup
- Configurable CPU throttling options
