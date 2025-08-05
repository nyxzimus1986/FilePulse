# Configuration Guide

FilePulse uses YAML configuration files to customize monitoring behavior. This guide covers all available configuration options.

## Configuration File Location

Default configuration locations:
- Windows: `%USERPROFILE%\.filepulse\config.yaml`
- macOS/Linux: `~/.filepulse/config.yaml`

You can also specify a custom configuration file using the `--config` option.

## Creating Configuration

### Initialize Default Configuration

```bash
filepulse init-config
```

This creates a default configuration file with commonly used settings.

### Manual Configuration

Create a YAML file with your desired settings:

```yaml
# Example configuration
monitoring:
  paths:
    - "."
    - "/home/user/documents"
  recursive: true
  events:
    - created
    - modified
    - deleted
    - moved
  
filtering:
  include_patterns:
    - "*.py"
    - "*.js"
    - "*.txt"
  exclude_patterns:
    - "__pycache__"
    - "*.pyc"
    - ".git"
  
performance:
  memory_limit_mb: 100
  batch_size: 50
  batch_timeout: 1.0
```

## Configuration Options

### Monitoring Section

#### `paths`
- **Type**: List of strings
- **Default**: `["."]`
- **Description**: Directories to monitor

```yaml
monitoring:
  paths:
    - "/home/user/projects"
    - "/var/log"
    - "C:\\Users\\User\\Documents"
```

#### `recursive`
- **Type**: Boolean
- **Default**: `true`
- **Description**: Monitor subdirectories recursively

#### `events`
- **Type**: List of strings
- **Default**: `["created", "modified", "deleted", "moved"]`
- **Options**: `created`, `modified`, `deleted`, `moved`
- **Description**: Types of filesystem events to monitor

### Filtering Section

#### `include_patterns`
- **Type**: List of strings
- **Default**: `["*"]`
- **Description**: Glob patterns for files to include

```yaml
filtering:
  include_patterns:
    - "*.py"      # Python files
    - "*.js"      # JavaScript files
    - "*.md"      # Markdown files
    - "data/*"    # Files in data directory
```

#### `exclude_patterns`
- **Type**: List of strings
- **Default**: `[]`
- **Description**: Glob patterns for files to exclude

```yaml
filtering:
  exclude_patterns:
    - "__pycache__"
    - "*.pyc"
    - ".git"
    - "node_modules"
    - "*.tmp"
```

#### `min_file_size`
- **Type**: Integer (bytes)
- **Default**: `0`
- **Description**: Minimum file size to monitor

#### `max_file_size`
- **Type**: Integer (bytes)
- **Default**: `null` (no limit)
- **Description**: Maximum file size to monitor

### Performance Section

#### `memory_limit_mb`
- **Type**: Integer
- **Default**: `100`
- **Description**: Maximum memory usage in MB

#### `batch_size`
- **Type**: Integer
- **Default**: `50`
- **Description**: Number of events to batch together

#### `batch_timeout`
- **Type**: Float
- **Default**: `1.0`
- **Description**: Timeout in seconds for batching events

#### `max_events`
- **Type**: Integer
- **Default**: `10000`
- **Description**: Maximum number of events to keep in memory

### Output Section

#### `format`
- **Type**: String
- **Default**: `"console"`
- **Options**: `console`, `json`, `csv`
- **Description**: Output format for events

#### `colored`
- **Type**: Boolean
- **Default**: `true`
- **Description**: Use colored output in console

#### `file`
- **Type**: String
- **Default**: `null`
- **Description**: File to write output to

```yaml
output:
  format: "json"
  file: "/var/log/filepulse.log"
  colored: false
```

### GUI Section

#### `theme`
- **Type**: String
- **Default**: `"default"`
- **Options**: `default`, `dark`, `light`
- **Description**: GUI theme

#### `window_size`
- **Type**: String
- **Default**: `"800x600"`
- **Description**: Initial window size

#### `auto_scroll`
- **Type**: Boolean
- **Default**: `true`
- **Description**: Auto-scroll to latest events

```yaml
gui:
  theme: "dark"
  window_size: "1024x768"
  auto_scroll: true
```

## Complete Example

```yaml
# FilePulse Configuration File
# This file controls all aspects of filesystem monitoring

monitoring:
  # Paths to monitor (can be files or directories)
  paths:
    - "."
    - "/home/user/projects"
  
  # Monitor subdirectories recursively
  recursive: true
  
  # Types of events to monitor
  events:
    - created
    - modified
    - deleted
    - moved

filtering:
  # Only monitor these file patterns
  include_patterns:
    - "*.py"
    - "*.js"
    - "*.tsx"
    - "*.json"
    - "*.yaml"
    - "*.md"
  
  # Ignore these patterns
  exclude_patterns:
    - "__pycache__"
    - "*.pyc"
    - ".git"
    - "node_modules"
    - "*.tmp"
    - "*.log"
  
  # File size limits (in bytes)
  min_file_size: 1
  max_file_size: 10485760  # 10MB

performance:
  # Memory limit in MB
  memory_limit_mb: 200
  
  # Event batching settings
  batch_size: 100
  batch_timeout: 0.5
  
  # Maximum events to keep in memory
  max_events: 5000

output:
  # Output format: console, json, csv
  format: "console"
  
  # Use colored output
  colored: true
  
  # Optional: write to file
  # file: "/var/log/filepulse.log"

gui:
  # GUI theme
  theme: "default"
  
  # Initial window size
  window_size: "900x700"
  
  # Auto-scroll to latest events
  auto_scroll: true

# Logging configuration
logging:
  level: "INFO"
  file: "filepulse.log"
```

## Environment Variables

You can override configuration values using environment variables:

- `FILEPULSE_CONFIG`: Path to configuration file
- `FILEPULSE_MEMORY_LIMIT`: Memory limit in MB
- `FILEPULSE_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

Example:
```bash
export FILEPULSE_MEMORY_LIMIT=500
export FILEPULSE_LOG_LEVEL=DEBUG
filepulse monitor /path/to/monitor
```

## Validation

FilePulse validates configuration files on startup. Common validation errors:

1. **Invalid YAML syntax**: Check for proper indentation and syntax
2. **Unknown options**: Remove any typos or deprecated options
3. **Invalid values**: Ensure values match expected types (string, integer, boolean)
4. **Path issues**: Verify that specified paths exist and are accessible

Use the `--validate-config` option to check your configuration:

```bash
filepulse --validate-config /path/to/config.yaml
```
