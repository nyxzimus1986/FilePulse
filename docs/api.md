# API Reference

This document provides detailed information about FilePulse's Python API for programmatic usage.

## Core Classes

### `FilePulseMonitor`

The main monitoring class that handles filesystem event detection.

```python
from filepulse.monitor import FilePulseMonitor

monitor = FilePulseMonitor(
    paths=['./src'],
    config_path='config.yaml'
)
```

#### Constructor Parameters

- `paths` (List[str]): Directories to monitor
- `config_path` (str, optional): Path to configuration file
- `recursive` (bool): Monitor subdirectories recursively (default: True)
- `events` (List[str]): Event types to monitor (default: all)

#### Methods

##### `start()`
Start filesystem monitoring.

```python
monitor.start()
```

##### `stop()`
Stop filesystem monitoring.

```python
monitor.stop()
```

##### `is_running()`
Check if monitoring is active.

```python
if monitor.is_running():
    print("Monitoring active")
```

##### `get_events(limit=None)`
Get collected events.

```python
events = monitor.get_events(limit=100)
for event in events:
    print(f"{event.event_type}: {event.path}")
```

**Parameters:**
- `limit` (int, optional): Maximum number of events to return

**Returns:** List of `FileEvent` objects

##### `clear_events()`
Clear the event history.

```python
monitor.clear_events()
```

##### `add_event_handler(handler)`
Add custom event handler.

```python
def my_handler(event):
    print(f"Custom handler: {event}")

monitor.add_event_handler(my_handler)
```

### `FileEvent`

Represents a single filesystem event.

#### Attributes

- `event_type` (str): Type of event ('created', 'modified', 'deleted', 'moved')
- `path` (str): Path to the affected file/directory
- `timestamp` (datetime): When the event occurred
- `size` (int): File size in bytes (if applicable)
- `is_directory` (bool): Whether the path is a directory
- `src_path` (str): Source path for move events
- `additional_info` (dict): Extra event metadata

#### Methods

##### `to_dict()`
Convert event to dictionary.

```python
event_dict = event.to_dict()
print(json.dumps(event_dict, indent=2))
```

##### `to_json()`
Convert event to JSON string.

```python
json_str = event.to_json()
```

### `Config`

Configuration management class.

```python
from filepulse.config import Config

config = Config('config.yaml')
```

#### Constructor Parameters

- `config_path` (str): Path to configuration file

#### Methods

##### `load()`
Load configuration from file.

```python
config.load()
```

##### `save(path=None)`
Save configuration to file.

```python
config.save()  # Save to original path
config.save('new-config.yaml')  # Save to new path
```

##### `get(key, default=None)`
Get configuration value.

```python
memory_limit = config.get('performance.memory_limit_mb', 100)
```

##### `set(key, value)`
Set configuration value.

```python
config.set('performance.memory_limit_mb', 200)
```

##### `validate()`
Validate configuration.

```python
is_valid, errors = config.validate()
if not is_valid:
    for error in errors:
        print(f"Config error: {error}")
```

### `EventBatcher`

Batches events for efficient processing.

```python
from filepulse.events import EventBatcher

batcher = EventBatcher(
    batch_size=50,
    timeout=1.0,
    callback=process_batch
)
```

#### Constructor Parameters

- `batch_size` (int): Maximum events per batch
- `timeout` (float): Maximum time to wait for batch completion
- `callback` (callable): Function to call with completed batches

#### Methods

##### `add_event(event)`
Add event to current batch.

```python
batcher.add_event(file_event)
```

##### `flush()`
Force process current batch.

```python
batcher.flush()
```

##### `start()`
Start background batch processing.

```python
batcher.start()
```

##### `stop()`
Stop batch processing.

```python
batcher.stop()
```

## Utility Functions

### `filepulse.utils`

#### `format_file_size(size_bytes)`
Format file size in human-readable format.

```python
from filepulse.utils import format_file_size

print(format_file_size(1024))     # "1.0 KB"
print(format_file_size(1048576))  # "1.0 MB"
```

#### `match_patterns(path, patterns)`
Check if path matches any of the given patterns.

```python
from filepulse.utils import match_patterns

patterns = ['*.py', '*.js']
if match_patterns('/path/to/file.py', patterns):
    print("File matches patterns")
```

#### `get_file_info(path)`
Get detailed file information.

```python
from filepulse.utils import get_file_info

info = get_file_info('/path/to/file.txt')
print(f"Size: {info['size']}, Modified: {info['modified']}")
```

**Returns:** Dictionary with file information:
- `size` (int): File size in bytes
- `modified` (datetime): Last modification time
- `created` (datetime): Creation time
- `is_directory` (bool): Whether path is directory
- `permissions` (str): File permissions

## Event Handlers

### Custom Event Handlers

Create custom handlers to process events:

```python
def log_handler(event):
    """Log events to file"""
    with open('events.log', 'a') as f:
        f.write(f"{event.timestamp}: {event.event_type} {event.path}\n")

def database_handler(event):
    """Store events in database"""
    # Database storage logic
    pass

def email_handler(event):
    """Send email notifications for critical events"""
    if event.event_type == 'deleted' and event.path.endswith('.important'):
        send_email(f"Important file deleted: {event.path}")

# Add handlers to monitor
monitor.add_event_handler(log_handler)
monitor.add_event_handler(database_handler)
monitor.add_event_handler(email_handler)
```

### Built-in Handlers

#### `ConsoleHandler`
Output events to console.

```python
from filepulse.output import ConsoleHandler

handler = ConsoleHandler(colored=True)
monitor.add_event_handler(handler.handle_event)
```

#### `FileHandler`
Output events to file.

```python
from filepulse.output import FileHandler

handler = FileHandler('events.log', format='json')
monitor.add_event_handler(handler.handle_event)
```

#### `JSONHandler`
Output events as JSON.

```python
from filepulse.output import JSONHandler

handler = JSONHandler('events.json')
monitor.add_event_handler(handler.handle_event)
```

## Examples

### Basic Monitoring

```python
from filepulse.monitor import FilePulseMonitor
import time

# Create monitor
monitor = FilePulseMonitor(['./src'])

# Start monitoring
monitor.start()

try:
    # Let it run for 60 seconds
    time.sleep(60)
    
    # Get events
    events = monitor.get_events()
    print(f"Captured {len(events)} events")
    
    for event in events:
        print(f"{event.timestamp}: {event.event_type} {event.path}")
        
finally:
    # Always stop monitoring
    monitor.stop()
```

### Programmatic Configuration

```python
from filepulse.monitor import FilePulseMonitor
from filepulse.config import Config

# Create configuration
config = Config()
config.set('monitoring.paths', ['./src', './tests'])
config.set('monitoring.events', ['created', 'modified'])
config.set('filtering.include_patterns', ['*.py', '*.js'])
config.set('filtering.exclude_patterns', ['__pycache__', '*.pyc'])
config.set('performance.memory_limit_mb', 200)

# Create monitor with configuration
monitor = FilePulseMonitor(config=config)

# Custom event handler
def process_event(event):
    if event.event_type == 'created':
        print(f"New file: {event.path}")
    elif event.event_type == 'modified':
        print(f"Modified: {event.path} ({event.size} bytes)")

monitor.add_event_handler(process_event)

# Start monitoring
monitor.start()

# Your application logic here
# ...

monitor.stop()
```

### Batch Processing

```python
from filepulse.monitor import FilePulseMonitor
from filepulse.events import EventBatcher

def process_batch(events):
    """Process a batch of events"""
    print(f"Processing batch of {len(events)} events")
    
    # Group by event type
    by_type = {}
    for event in events:
        if event.event_type not in by_type:
            by_type[event.event_type] = []
        by_type[event.event_type].append(event)
    
    # Process each type
    for event_type, type_events in by_type.items():
        print(f"  {event_type}: {len(type_events)} events")

# Create batcher
batcher = EventBatcher(
    batch_size=25,
    timeout=0.5,
    callback=process_batch
)

# Create monitor
monitor = FilePulseMonitor(['./data'])

# Add batcher as event handler
monitor.add_event_handler(batcher.add_event)

# Start both
batcher.start()
monitor.start()

try:
    time.sleep(120)  # Run for 2 minutes
finally:
    monitor.stop()
    batcher.stop()
```

### Integration with Web Framework

```python
from flask import Flask, jsonify
from filepulse.monitor import FilePulseMonitor
import threading

app = Flask(__name__)
monitor = FilePulseMonitor(['./uploads'])

@app.route('/api/events')
def get_events():
    events = monitor.get_events(limit=100)
    return jsonify([event.to_dict() for event in events])

@app.route('/api/start', methods=['POST'])
def start_monitoring():
    if not monitor.is_running():
        monitor.start()
        return jsonify({'status': 'started'})
    return jsonify({'status': 'already_running'})

@app.route('/api/stop', methods=['POST'])
def stop_monitoring():
    if monitor.is_running():
        monitor.stop()
        return jsonify({'status': 'stopped'})
    return jsonify({'status': 'not_running'})

@app.route('/api/stats')
def get_stats():
    events = monitor.get_events()
    stats = {
        'total_events': len(events),
        'is_running': monitor.is_running(),
        'by_type': {}
    }
    
    for event in events:
        event_type = event.event_type
        if event_type not in stats['by_type']:
            stats['by_type'][event_type] = 0
        stats['by_type'][event_type] += 1
    
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)
```

## Error Handling

### Exception Types

#### `ConfigError`
Raised when configuration is invalid.

```python
from filepulse.config import Config, ConfigError

try:
    config = Config('invalid-config.yaml')
    config.load()
except ConfigError as e:
    print(f"Configuration error: {e}")
```

#### `MonitorError`
Raised when monitoring fails to start or encounters issues.

```python
from filepulse.monitor import FilePulseMonitor, MonitorError

try:
    monitor = FilePulseMonitor(['/nonexistent/path'])
    monitor.start()
except MonitorError as e:
    print(f"Monitoring error: {e}")
```

### Best Practices

1. **Always stop monitoring** in a finally block or using context managers
2. **Handle exceptions** appropriately for your use case
3. **Limit memory usage** with appropriate configuration
4. **Use event batching** for high-volume scenarios
5. **Filter events** to reduce processing overhead

```python
from filepulse.monitor import FilePulseMonitor
from contextlib import contextmanager

@contextmanager
def file_monitor(paths, **kwargs):
    monitor = FilePulseMonitor(paths, **kwargs)
    try:
        monitor.start()
        yield monitor
    finally:
        monitor.stop()

# Usage
with file_monitor(['./src']) as monitor:
    # Your monitoring logic here
    time.sleep(60)
    events = monitor.get_events()
    # Monitor is automatically stopped when exiting the context
```
