# Usage Guide

This guide covers how to use FilePulse for filesystem monitoring in various scenarios.

## Command Line Interface

### Basic Usage

Monitor current directory:
```bash
filepulse monitor .
```

Monitor specific directories:
```bash
filepulse monitor /home/user/projects /var/log
```

Monitor with custom configuration:
```bash
filepulse monitor . --config /path/to/config.yaml
```

### CLI Options

#### `monitor` command

```bash
filepulse monitor [PATHS...] [OPTIONS]
```

**Options:**
- `--config, -c`: Configuration file path
- `--recursive, -r`: Monitor recursively (default: true)
- `--events, -e`: Events to monitor (created,modified,deleted,moved)
- `--include, -i`: Include patterns (can specify multiple)
- `--exclude, -x`: Exclude patterns (can specify multiple)
- `--format, -f`: Output format (console,json,csv)
- `--output, -o`: Output file
- `--stats, -s`: Show performance statistics
- `--memory-limit`: Memory limit in MB
- `--batch-size`: Event batch size
- `--batch-timeout`: Batch timeout in seconds
- `--verbose, -v`: Verbose output
- `--quiet, -q`: Quiet output

**Examples:**

Monitor Python files only:
```bash
filepulse monitor . --include "*.py" --include "*.pyx"
```

Exclude common build directories:
```bash
filepulse monitor . --exclude "__pycache__" --exclude "node_modules"
```

JSON output to file:
```bash
filepulse monitor . --format json --output events.json
```

Monitor specific events:
```bash
filepulse monitor . --events created,modified
```

#### `gui` command

Launch the graphical interface:
```bash
filepulse gui
```

**Options:**
- `--config, -c`: Configuration file path
- `--theme`: GUI theme (default,dark,light)

#### `init-config` command

Create default configuration file:
```bash
filepulse init-config
```

**Options:**
- `--path, -p`: Configuration file path
- `--overwrite`: Overwrite existing configuration

## Graphical User Interface

### Starting the GUI

```bash
filepulse gui
```

Or use the standalone command:
```bash
filepulse-gui
```

### GUI Features

#### Monitor Tab
- **Start/Stop Monitoring**: Control filesystem monitoring
- **Path Selection**: Choose directories to monitor
- **Real-time Events**: View filesystem events as they occur
- **Event Filtering**: Filter events by type, path, or pattern
- **Export Events**: Save events to file

#### Configuration Tab
- **Visual Configuration**: Edit settings with form controls
- **Live Preview**: See configuration changes immediately
- **Load/Save**: Load and save configuration files
- **Validation**: Real-time configuration validation

#### Statistics Tab
- **Performance Metrics**: CPU and memory usage
- **Event Counts**: Number of events by type
- **Resource Usage**: Detailed system resource information
- **Graphs**: Visual representation of monitoring activity

#### About Tab
- **Version Information**: Application and dependency versions
- **System Information**: Platform and environment details
- **Documentation Links**: Quick access to help resources

### GUI Shortcuts

- **Ctrl+S**: Save configuration
- **Ctrl+O**: Open configuration file
- **Ctrl+Q**: Quit application
- **F5**: Refresh statistics
- **F11**: Toggle fullscreen
- **Escape**: Clear event list

## Use Cases

### Development Monitoring

Monitor source code changes during development:

```bash
filepulse monitor ./src --include "*.py" --include "*.js" --exclude "__pycache__"
```

Configuration file example:
```yaml
monitoring:
  paths: ["./src", "./tests"]
  events: ["created", "modified", "deleted"]

filtering:
  include_patterns:
    - "*.py"
    - "*.js"
    - "*.tsx"
    - "*.css"
    - "*.html"
  exclude_patterns:
    - "__pycache__"
    - "node_modules"
    - "*.pyc"
    - ".git"

output:
  format: "console"
  colored: true
```

### System Administration

Monitor system directories for security or maintenance:

```bash
filepulse monitor /etc /var/log --format json --output system-events.json
```

Configuration for system monitoring:
```yaml
monitoring:
  paths:
    - "/etc"
    - "/var/log"
    - "/home"
  events: ["created", "modified", "deleted", "moved"]

filtering:
  exclude_patterns:
    - "*.tmp"
    - "/proc/*"
    - "/sys/*"

performance:
  memory_limit_mb: 500
  batch_size: 100

output:
  format: "json"
  file: "/var/log/filepulse-system.json"
```

### Build Process Monitoring

Monitor build artifacts and compilation:

```bash
filepulse monitor ./build ./dist --events created,modified
```

### Log File Monitoring

Monitor log files for changes:

```bash
filepulse monitor /var/log --include "*.log" --format csv --output log-changes.csv
```

### Backup Verification

Monitor backup directories to ensure files are being copied:

```bash
filepulse monitor /backup --events created --stats
```

## Output Formats

### Console Output

Default human-readable format with colors:

```
[2024-01-15 10:30:15] CREATED  /home/user/file.txt (1.2 KB)
[2024-01-15 10:30:16] MODIFIED /home/user/file.txt (1.3 KB)
[2024-01-15 10:30:17] DELETED  /home/user/file.txt
```

### JSON Output

Structured data format:

```json
{
  "timestamp": "2024-01-15T10:30:15.123456",
  "event_type": "created",
  "path": "/home/user/file.txt",
  "size": 1234,
  "is_directory": false,
  "additional_info": {}
}
```

### CSV Output

Comma-separated values for spreadsheet analysis:

```csv
timestamp,event_type,path,size,is_directory
2024-01-15T10:30:15.123456,created,/home/user/file.txt,1234,false
2024-01-15T10:30:16.234567,modified,/home/user/file.txt,1345,false
```

## Performance Tuning

### Memory Management

Control memory usage with configuration:

```yaml
performance:
  memory_limit_mb: 200      # Limit total memory usage
  max_events: 5000          # Maximum events in memory
  batch_size: 100           # Events per batch
  batch_timeout: 0.5        # Batch timeout in seconds
```

### Event Filtering

Reduce processing overhead by filtering events:

```yaml
filtering:
  include_patterns: ["*.py", "*.js"]  # Only monitor these files
  exclude_patterns: ["*.tmp", "*.log"] # Ignore these files
  min_file_size: 100                   # Ignore small files
  max_file_size: 10485760             # Ignore large files (10MB)
```

### Recursive Monitoring

Control directory traversal:

```yaml
monitoring:
  recursive: true           # Monitor subdirectories
  max_depth: 10            # Limit recursion depth
```

## Integration Examples

### Shell Scripts

```bash
#!/bin/bash
# Start monitoring in background
filepulse monitor ./data --format json --output events.json &
MONITOR_PID=$!

# Do some work
./my-script.sh

# Stop monitoring
kill $MONITOR_PID

# Process events
python process-events.py events.json
```

### Python Integration

```python
import subprocess
import json
import time

# Start monitoring
process = subprocess.Popen([
    'filepulse', 'monitor', './data',
    '--format', 'json',
    '--output', 'events.json'
])

# Let it run for a while
time.sleep(60)

# Stop monitoring
process.terminate()

# Read events
with open('events.json', 'r') as f:
    events = [json.loads(line) for line in f]

print(f"Captured {len(events)} events")
```

### Docker Integration

```dockerfile
FROM python:3.11-slim

RUN pip install filepulse

# Copy monitoring script
COPY monitor.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/monitor.sh

CMD ["monitor.sh"]
```

```bash
#!/bin/bash
# monitor.sh
filepulse monitor /app/data --format json --output /logs/events.json
```

## Troubleshooting

### Common Issues

1. **High Memory Usage**
   - Reduce `memory_limit_mb` in configuration
   - Increase `batch_timeout` to process events more frequently
   - Use more specific `include_patterns` to reduce event volume

2. **Missing Events**
   - Check file permissions
   - Verify paths exist and are accessible
   - Review `exclude_patterns` for overly broad exclusions

3. **Performance Issues**
   - Reduce `batch_size` for faster processing
   - Use `exclude_patterns` to ignore unnecessary files
   - Limit monitoring to specific subdirectories

4. **GUI Not Responding**
   - Check if monitoring too many files/directories
   - Reduce event batch size in configuration
   - Restart the GUI application

### Debug Mode

Enable verbose logging for troubleshooting:

```bash
filepulse monitor . --verbose
```

Or set environment variable:
```bash
export FILEPULSE_LOG_LEVEL=DEBUG
filepulse monitor .
```

### Getting Help

- Use `filepulse --help` for command-line help
- Check the FAQ section
- Review configuration examples
- Open an issue on GitHub for bugs or feature requests
