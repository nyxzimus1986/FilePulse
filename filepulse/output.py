"""
Output handling for FilePulse events
"""

import json
import sys
from typing import List, Dict, Any, TextIO
from datetime import datetime
from pathlib import Path
import logging

from .events import FileSystemEvent

logger = logging.getLogger(__name__)


class ConsoleOutputHandler:
    """Output events to console"""
    
    def __init__(self, config, output_stream: TextIO = None):
        self.config = config
        self.output_stream = output_stream or sys.stdout
        self.format_type = config.get('output.console_format', 'simple')
        self.timestamp_format = config.get('output.timestamp_format', '%Y-%m-%d %H:%M:%S')
        
        # Color support
        try:
            import colorama
            colorama.init()
            self.colors = {
                'created': colorama.Fore.GREEN,
                'modified': colorama.Fore.YELLOW,
                'deleted': colorama.Fore.RED,
                'moved': colorama.Fore.BLUE,
                'reset': colorama.Style.RESET_ALL
            }
        except ImportError:
            self.colors = {key: '' for key in ['created', 'modified', 'deleted', 'moved', 'reset']}
    
    def __call__(self, events: List[FileSystemEvent]):
        """Handle a batch of events"""
        for event in events:
            self._output_event(event)
    
    def _output_event(self, event: FileSystemEvent):
        """Output a single event"""
        if self.format_type == 'json':
            self._output_json(event)
        elif self.format_type == 'detailed':
            self._output_detailed(event)
        else:
            self._output_simple(event)
    
    def _output_simple(self, event: FileSystemEvent):
        """Simple output format"""
        timestamp = datetime.fromtimestamp(event.timestamp).strftime(self.timestamp_format)
        color = self.colors.get(event.event_type, '')
        reset = self.colors['reset']
        
        if event.event_type == 'moved':
            message = f"[{timestamp}] {color}{event.event_type.upper()}{reset}: {event.src_path} -> {event.dest_path}"
        else:
            message = f"[{timestamp}] {color}{event.event_type.upper()}{reset}: {event.src_path}"
        
        print(message, file=self.output_stream)
        self.output_stream.flush()
    
    def _output_detailed(self, event: FileSystemEvent):
        """Detailed output format"""
        timestamp = datetime.fromtimestamp(event.timestamp).strftime(self.timestamp_format)
        color = self.colors.get(event.event_type, '')
        reset = self.colors['reset']
        
        file_type = "DIR" if event.is_directory else "FILE"
        
        if event.event_type == 'moved':
            message = f"[{timestamp}] {color}{event.event_type.upper()}{reset} {file_type}: {event.src_path} -> {event.dest_path}"
        else:
            message = f"[{timestamp}] {color}{event.event_type.upper()}{reset} {file_type}: {event.src_path}"
        
        print(message, file=self.output_stream)
        self.output_stream.flush()
    
    def _output_json(self, event: FileSystemEvent):
        """JSON output format"""
        json_str = json.dumps(event.to_dict(), indent=None, separators=(',', ':'))
        print(json_str, file=self.output_stream)
        self.output_stream.flush()


class FileOutputHandler:
    """Output events to a file"""
    
    def __init__(self, config, file_path: str):
        self.config = config
        self.file_path = file_path
        self.timestamp_format = config.get('output.timestamp_format', '%Y-%m-%d %H:%M:%S')
        
        # Ensure directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    
    def __call__(self, events: List[FileSystemEvent]):
        """Handle a batch of events"""
        try:
            with open(self.file_path, 'a', encoding='utf-8') as f:
                for event in events:
                    self._write_event(f, event)
        except IOError as e:
            logger.error(f"Failed to write to log file {self.file_path}: {e}")
    
    def _write_event(self, file: TextIO, event: FileSystemEvent):
        """Write a single event to file"""
        timestamp = datetime.fromtimestamp(event.timestamp).strftime(self.timestamp_format)
        
        if event.event_type == 'moved':
            line = f"[{timestamp}] {event.event_type.upper()}: {event.src_path} -> {event.dest_path}\n"
        else:
            line = f"[{timestamp}] {event.event_type.upper()}: {event.src_path}\n"
        
        file.write(line)
        file.flush()


class JsonFileOutputHandler:
    """Output events to a JSON file"""
    
    def __init__(self, config, file_path: str):
        self.config = config
        self.file_path = file_path
        
        # Ensure directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    
    def __call__(self, events: List[FileSystemEvent]):
        """Handle a batch of events"""
        try:
            with open(self.file_path, 'a', encoding='utf-8') as f:
                for event in events:
                    json_str = json.dumps(event.to_dict())
                    f.write(json_str + '\n')
                    f.flush()
        except IOError as e:
            logger.error(f"Failed to write to JSON file {self.file_path}: {e}")


class CustomOutputHandler:
    """Custom output handler that can be extended"""
    
    def __init__(self, config, handler_func):
        self.config = config
        self.handler_func = handler_func
    
    def __call__(self, events: List[FileSystemEvent]):
        """Handle a batch of events"""
        try:
            self.handler_func(events)
        except Exception as e:
            logger.error(f"Error in custom output handler: {e}")


class StatisticsCollector:
    """Collect statistics about filesystem events"""
    
    def __init__(self):
        self.stats = {
            'total_events': 0,
            'events_by_type': {},
            'events_by_extension': {},
            'start_time': datetime.now(),
            'last_event_time': None
        }
    
    def __call__(self, events: List[FileSystemEvent]):
        """Handle a batch of events for statistics"""
        for event in events:
            self._process_event(event)
    
    def _process_event(self, event: FileSystemEvent):
        """Process a single event for statistics"""
        self.stats['total_events'] += 1
        self.stats['last_event_time'] = event.datetime
        
        # Count by event type
        event_type = event.event_type
        self.stats['events_by_type'][event_type] = self.stats['events_by_type'].get(event_type, 0) + 1
        
        # Count by file extension
        if not event.is_directory:
            ext = Path(event.src_path).suffix.lower()
            if ext:
                self.stats['events_by_extension'][ext] = self.stats['events_by_extension'].get(ext, 0) + 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics"""
        stats = self.stats.copy()
        stats['start_time'] = stats['start_time'].isoformat()
        if stats['last_event_time']:
            stats['last_event_time'] = stats['last_event_time'].isoformat()
        return stats
    
    def reset_stats(self):
        """Reset statistics"""
        self.stats = {
            'total_events': 0,
            'events_by_type': {},
            'events_by_extension': {},
            'start_time': datetime.now(),
            'last_event_time': None
        }


def create_output_handlers(config) -> List:
    """Create output handlers based on configuration"""
    handlers = []
    
    # Console output
    if config.get('output.console', True):
        handlers.append(ConsoleOutputHandler(config))
    
    # File output
    log_file = config.get('output.log_file')
    if log_file:
        handlers.append(FileOutputHandler(config, log_file))
    
    # JSON output
    if config.get('output.json_output', False):
        json_file = config.get('output.json_file', 'filepulse_events.jsonl')
        handlers.append(JsonFileOutputHandler(config, json_file))
    
    return handlers


def create_statistics_collector() -> StatisticsCollector:
    """Create a statistics collector"""
    return StatisticsCollector()
