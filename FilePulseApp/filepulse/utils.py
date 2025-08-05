"""
Utility functions for FilePulse
"""

import os
import sys
import time
import hashlib
import platform
from typing import Dict, List, Any, Optional
from pathlib import Path


def get_file_info(file_path: str) -> Dict[str, Any]:
    """Get detailed information about a file"""
    try:
        path = Path(file_path)
        stat = path.stat()
        
        return {
            'path': str(path.resolve()),
            'name': path.name,
            'size': stat.st_size,
            'created': stat.st_ctime,
            'modified': stat.st_mtime,
            'accessed': stat.st_atime,
            'is_directory': path.is_dir(),
            'is_file': path.is_file(),
            'exists': path.exists(),
            'extension': path.suffix,
            'parent': str(path.parent)
        }
    except (OSError, IOError) as e:
        return {
            'path': file_path,
            'error': str(e),
            'exists': False
        }


def calculate_file_hash(file_path: str, algorithm: str = 'md5') -> Optional[str]:
    """Calculate hash of a file"""
    if not os.path.exists(file_path) or os.path.isdir(file_path):
        return None
    
    try:
        hasher = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (OSError, IOError):
        return None


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"


def format_timestamp(timestamp: float, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """Format timestamp in readable format"""
    return time.strftime(format_str, time.localtime(timestamp))


def is_hidden_file(file_path: str) -> bool:
    """Check if file is hidden (cross-platform)"""
    path = Path(file_path)
    
    # Unix-like systems: starts with dot
    if path.name.startswith('.'):
        return True
    
    # Windows: check file attributes
    if platform.system() == 'Windows':
        try:
            import stat
            return bool(os.stat(file_path).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
        except (AttributeError, OSError):
            pass
    
    return False


def get_system_info() -> Dict[str, Any]:
    """Get system information"""
    return {
        'platform': platform.system(),
        'platform_release': platform.release(),
        'platform_version': platform.version(),
        'architecture': platform.architecture()[0],
        'machine': platform.machine(),
        'processor': platform.processor(),
        'python_version': sys.version,
        'python_executable': sys.executable
    }


def ensure_directory(path: str) -> bool:
    """Ensure directory exists, create if necessary"""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except OSError:
        return False


def safe_path_join(*paths) -> str:
    """Safely join paths, resolving any relative components"""
    return str(Path(*paths).resolve())


def is_subpath(path: str, parent: str) -> bool:
    """Check if path is a subpath of parent"""
    try:
        path_obj = Path(path).resolve()
        parent_obj = Path(parent).resolve()
        return parent_obj in path_obj.parents or path_obj == parent_obj
    except (OSError, ValueError):
        return False


def find_config_file(start_path: str = '.', config_names: List[str] = None) -> Optional[str]:
    """Find configuration file by searching up the directory tree"""
    if config_names is None:
        config_names = [
            'filepulse.yaml',
            'filepulse.yml', 
            '.filepulse.yaml',
            '.filepulse.yml',
            'filepulse_config.yaml'
        ]
    
    current_path = Path(start_path).resolve()
    
    # Search up the directory tree
    for path in [current_path] + list(current_path.parents):
        for config_name in config_names:
            config_path = path / config_name
            if config_path.exists() and config_path.is_file():
                return str(config_path)
    
    return None


def validate_path(path: str) -> bool:
    """Validate if path is safe to monitor"""
    try:
        path_obj = Path(path).resolve()
        
        # Check if path exists
        if not path_obj.exists():
            return False
        
        # Check if we have read permissions
        if not os.access(path, os.R_OK):
            return False
        
        # Avoid system-critical paths
        critical_paths = [
            '/sys',
            '/proc',
            '/dev',
            'C:\\Windows\\System32',
            'C:\\Windows\\SysWOW64'
        ]
        
        for critical in critical_paths:
            if is_subpath(str(path_obj), critical):
                return False
        
        return True
        
    except (OSError, ValueError):
        return False


def cleanup_old_logs(log_directory: str, max_age_days: int = 30, max_files: int = 10):
    """Clean up old log files"""
    try:
        log_path = Path(log_directory)
        if not log_path.exists():
            return
        
        # Find log files
        log_files = []
        for pattern in ['*.log', '*.jsonl']:
            log_files.extend(log_path.glob(pattern))
        
        # Sort by modification time (newest first)
        log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        current_time = time.time()
        max_age_seconds = max_age_days * 24 * 60 * 60
        
        # Remove old files or excess files
        for i, log_file in enumerate(log_files):
            should_remove = (
                i >= max_files or  # Too many files
                (current_time - log_file.stat().st_mtime) > max_age_seconds  # Too old
            )
            
            if should_remove:
                try:
                    log_file.unlink()
                except OSError:
                    pass  # Ignore deletion errors
                    
    except Exception:
        pass  # Ignore cleanup errors


def get_disk_usage(path: str) -> Dict[str, int]:
    """Get disk usage statistics for a path"""
    try:
        import shutil
        total, used, free = shutil.disk_usage(path)
        return {
            'total': total,
            'used': used,
            'free': free,
            'percent_used': (used / total) * 100 if total > 0 else 0
        }
    except Exception:
        return {'total': 0, 'used': 0, 'free': 0, 'percent_used': 0}


class RateLimiter:
    """Simple rate limiter to prevent event flooding"""
    
    def __init__(self, max_calls: int = 100, time_window: float = 1.0):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
    
    def allow(self) -> bool:
        """Check if call is allowed under rate limit"""
        current_time = time.time()
        
        # Remove old calls outside the time window
        self.calls = [call_time for call_time in self.calls 
                     if current_time - call_time < self.time_window]
        
        # Check if we're under the limit
        if len(self.calls) < self.max_calls:
            self.calls.append(current_time)
            return True
        
        return False
    
    def reset(self):
        """Reset the rate limiter"""
        self.calls.clear()


def debounce_events(events: List, key_func, time_window: float = 0.1):
    """Debounce events that are too frequent"""
    if not events:
        return events
    
    # Group events by key
    event_groups = {}
    for event in events:
        key = key_func(event)
        if key not in event_groups:
            event_groups[key] = []
        event_groups[key].append(event)
    
    # For each group, only keep the latest event if multiple events
    # occur within the time window
    debounced = []
    for key, group in event_groups.items():
        if len(group) == 1:
            debounced.extend(group)
        else:
            # Sort by timestamp and check time differences
            group.sort(key=lambda x: x.timestamp)
            last_event = None
            
            for event in group:
                if last_event is None or (event.timestamp - last_event.timestamp) > time_window:
                    debounced.append(event)
                    last_event = event
                else:
                    # Update the last event instead of adding a new one
                    if debounced and debounced[-1] == last_event:
                        debounced[-1] = event
                    last_event = event
    
    return debounced
