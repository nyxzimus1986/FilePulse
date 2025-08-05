"""
Event handling and filtering for FilePulse
"""

import os
import fnmatch
import time
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FileSystemEvent:
    """Represents a filesystem event"""
    
    def __init__(self, event_type: str, src_path: str, dest_path: str = None, 
                 is_directory: bool = False, timestamp: float = None):
        self.event_type = event_type  # created, modified, deleted, moved
        self.src_path = str(Path(src_path).resolve())
        self.dest_path = str(Path(dest_path).resolve()) if dest_path else None
        self.is_directory = is_directory
        self.timestamp = timestamp or time.time()
        self.datetime = datetime.fromtimestamp(self.timestamp)
    
    def __str__(self):
        if self.event_type == 'moved' and self.dest_path:
            return f"{self.event_type.upper()}: {self.src_path} -> {self.dest_path}"
        return f"{self.event_type.upper()}: {self.src_path}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary"""
        return {
            'event_type': self.event_type,
            'src_path': self.src_path,
            'dest_path': self.dest_path,
            'is_directory': self.is_directory,
            'timestamp': self.timestamp,
            'datetime': self.datetime.isoformat()
        }


class EventFilter:
    """Filters filesystem events based on configuration"""
    
    def __init__(self, config):
        self.config = config
        self.include_patterns = config.include_patterns
        self.exclude_patterns = config.exclude_patterns
        self.ignore_directories = config.ignore_directories
        self.monitoring_events = set(config.monitoring_events)
        
        # File size filters
        self.min_file_size = config.get('monitoring.filters.min_file_size', 0)
        self.max_file_size = config.get('monitoring.filters.max_file_size')
    
    def should_process_event(self, event: FileSystemEvent) -> bool:
        """Determine if an event should be processed"""
        
        # Check event type
        if event.event_type not in self.monitoring_events:
            return False
        
        # Check if path should be ignored
        if self._is_ignored_path(event.src_path):
            return False
        
        # For move events, also check destination path
        if event.event_type == 'moved' and event.dest_path:
            if self._is_ignored_path(event.dest_path):
                return False
        
        # Apply pattern filters
        if not self._matches_patterns(event.src_path):
            return False
        
        # Apply file size filters
        if not event.is_directory and not self._matches_file_size(event.src_path):
            return False
        
        return True
    
    def _is_ignored_path(self, path: str) -> bool:
        """Check if path should be ignored"""
        path_obj = Path(path)
        
        # Check if any parent directory is in ignore list
        for part in path_obj.parts:
            if part in self.ignore_directories:
                return True
        
        # Check if filename matches ignore patterns
        filename = path_obj.name
        for pattern in self.ignore_directories:
            if fnmatch.fnmatch(filename, pattern):
                return True
        
        return False
    
    def _matches_patterns(self, path: str) -> bool:
        """Check if path matches include/exclude patterns"""
        filename = Path(path).name
        
        # If include patterns are specified, file must match at least one
        if self.include_patterns:
            if not any(fnmatch.fnmatch(filename, pattern) for pattern in self.include_patterns):
                return False
        
        # File must not match any exclude patterns
        if self.exclude_patterns:
            if any(fnmatch.fnmatch(filename, pattern) for pattern in self.exclude_patterns):
                return False
        
        return True
    
    def _matches_file_size(self, path: str) -> bool:
        """Check if file size is within limits"""
        try:
            if not os.path.exists(path):
                return True  # File might be deleted, allow the event
            
            file_size = os.path.getsize(path)
            
            if file_size < self.min_file_size:
                return False
            
            if self.max_file_size is not None and file_size > self.max_file_size:
                return False
            
            return True
        except (OSError, IOError):
            # If we can't get file size, allow the event
            return True


class EventHandler:
    """Handles processed filesystem events"""
    
    def __init__(self, config, output_handlers: List[Callable] = None):
        self.config = config
        self.output_handlers = output_handlers or []
        self.event_filter = EventFilter(config)
        
        # Event batching
        self.batch_events = config.get('performance.batch_events', True)
        self.batch_timeout = config.get('performance.batch_timeout', 0.5)
        self.max_events_per_batch = config.get('performance.max_events_per_batch', 100)
        
        # Memory management
        self.memory_limit_mb = config.get('performance.memory_limit_mb', 50)
        self.max_batch_memory_mb = min(self.memory_limit_mb * 0.2, 10)  # Use max 20% of limit or 10MB
        
        self._event_batch = []
        self._last_batch_time = time.time()
    
    def handle_event(self, event: FileSystemEvent):
        """Handle a filesystem event"""
        
        # Apply filtering
        if not self.event_filter.should_process_event(event):
            return
        
        if self.batch_events:
            self._handle_batched_event(event)
        else:
            self._process_event(event)
    
    def _handle_batched_event(self, event: FileSystemEvent):
        """Handle event with batching"""
        self._event_batch.append(event)
        current_time = time.time()
        
        # Check if we should process batch due to memory concerns
        batch_memory_usage = self._estimate_batch_memory()
        
        # Process batch if conditions are met
        should_process = (
            len(self._event_batch) >= self.max_events_per_batch or
            current_time - self._last_batch_time >= self.batch_timeout or
            batch_memory_usage > self.max_batch_memory_mb
        )
        
        if should_process:
            self._process_batch()
    
    def _estimate_batch_memory(self) -> float:
        """Estimate memory usage of current event batch in MB"""
        if not self._event_batch:
            return 0.0
        
        try:
            import sys
            total_size = 0
            for event in self._event_batch:
                # Rough estimate: event object + strings
                total_size += sys.getsizeof(event)
                total_size += sys.getsizeof(event.src_path) if event.src_path else 0
                total_size += sys.getsizeof(event.dest_path) if event.dest_path else 0
                total_size += 200  # Overhead per event
            
            return total_size / (1024 * 1024)  # Convert to MB
        except:
            # Fallback: assume ~500 bytes per event
            return len(self._event_batch) * 500 / (1024 * 1024)
    
    def _process_batch(self):
        """Process accumulated events as a batch"""
        if not self._event_batch:
            return
        
        # Sort events by timestamp
        self._event_batch.sort(key=lambda e: e.timestamp)
        
        # Send to output handlers
        for handler in self.output_handlers:
            try:
                handler(self._event_batch)
            except Exception as e:
                logger.error(f"Error in output handler: {e}")
        
        # Clear batch
        self._event_batch.clear()
        self._last_batch_time = time.time()
    
    def _process_event(self, event: FileSystemEvent):
        """Process single event immediately"""
        for handler in self.output_handlers:
            try:
                handler([event])
            except Exception as e:
                logger.error(f"Error in output handler: {e}")
    
    def flush(self):
        """Force processing of any pending batched events"""
        if self._event_batch:
            self._process_batch()
    
    def add_output_handler(self, handler: Callable):
        """Add an output handler"""
        self.output_handlers.append(handler)
    
    def remove_output_handler(self, handler: Callable):
        """Remove an output handler"""
        if handler in self.output_handlers:
            self.output_handlers.remove(handler)
