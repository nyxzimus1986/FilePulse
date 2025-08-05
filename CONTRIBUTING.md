# Contributing to FilePulse

Thank you for your interest in contributing to FilePulse! This document provides guidelines and information for contributors.

## Code of Conduct

Please be respectful and constructive in all interactions. We welcome contributions from everyone regardless of experience level.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/FilePulse/issues)
2. If not, create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)
   - Any relevant log output

### Suggesting Features

1. Check existing issues and discussions for similar ideas
2. Create a new issue with the "enhancement" label
3. Describe the feature and its use case clearly
4. Explain why it would be beneficial

### Submitting Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/FilePulse.git
   cd FilePulse
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Make your changes**
   - Follow the coding standards below
   - Add tests for new functionality
   - Update documentation as needed

5. **Test your changes**
   ```bash
   python -m pytest tests/
   python -m filepulse.gui  # Test GUI
   python -m filepulse.cli monitor .  # Test CLI
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of your changes"
   ```

7. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub.

## Development Guidelines

### Code Style

- **Follow PEP 8** for Python code style
- **Use type hints** for all function parameters and return values
- **Add docstrings** for all public functions and classes
- **Keep lines under 100 characters** when reasonable
- **Use meaningful variable and function names**

### Example Code Style

```python
def process_events(self, events: List[FileSystemEvent]) -> None:
    """Process a batch of filesystem events.
    
    Args:
        events: List of filesystem events to process
        
    Raises:
        ProcessingError: If event processing fails
    """
    for event in events:
        if self._should_process(event):
            self._handle_event(event)
```

### Project Structure

```
FilePulse/
├── filepulse/           # Main package
│   ├── __init__.py
│   ├── cli.py          # Command-line interface
│   ├── gui.py          # GUI interface
│   ├── monitor.py      # Core monitoring
│   ├── events.py       # Event handling
│   ├── config.py       # Configuration
│   ├── output.py       # Output handling
│   └── utils.py        # Utilities
├── tests/              # Test suite
├── config/             # Default configs
├── docs/               # Documentation
└── scripts/            # Utility scripts
```

### Testing

- **Write tests** for new functionality
- **Update existing tests** when modifying behavior
- **Test on multiple platforms** when possible
- **Include edge cases** in your tests

#### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_events.py

# Run with coverage
python -m pytest --cov=filepulse tests/
```

### Documentation

- **Update README.md** for new features
- **Add docstrings** to all public APIs
- **Update CHANGELOG.md** for your changes
- **Include examples** for new functionality

### Commit Messages

Use clear, descriptive commit messages:

- `Add: new feature description`
- `Fix: bug description`
- `Update: what was updated`
- `Remove: what was removed`
- `Refactor: what was refactored`

Examples:
```
Add: memory limit enforcement in ResourceMonitor
Fix: GUI not displaying user-created folder events
Update: README with installation instructions
```

## Areas for Contribution

### High Priority
- **Bug fixes** in existing functionality
- **Performance optimizations**
- **Cross-platform compatibility** improvements
- **Documentation** improvements

### Medium Priority
- **New output formats** (database, webhooks, etc.)
- **Plugin system** for custom event handlers
- **Web dashboard** interface
- **Enhanced filtering** options

### Nice to Have
- **Docker support**
- **Configuration validation**
- **Event replay functionality**
- **Integration tests**

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- A code editor (VS Code recommended)

### Setup Steps

1. **Clone and setup**
   ```bash
   git clone https://github.com/yourusername/FilePulse.git
   cd FilePulse
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

2. **Verify installation**
   ```bash
   python -m filepulse.gui
   python -m filepulse.cli --help
   ```

3. **Run tests**
   ```bash
   python -m pytest tests/
   ```

### Development Tools

Recommended tools for development:

- **VS Code** with Python extension
- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking
- **Pytest** for testing

## Questions?

- **General questions**: Start a [Discussion](https://github.com/yourusername/FilePulse/discussions)
- **Bug reports**: Create an [Issue](https://github.com/yourusername/FilePulse/issues)
- **Feature requests**: Create an [Issue](https://github.com/yourusername/FilePulse/issues) with "enhancement" label

## Recognition

Contributors will be recognized in:
- README.md contributors section
- CHANGELOG.md for their contributions
- GitHub contributors page

Thank you for contributing to FilePulse! 🚀
