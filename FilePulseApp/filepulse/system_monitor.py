"""
System-wide monitoring utilities for FilePulse
"""

import os
import platform
import psutil
from typing import List, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class SystemPathManager:
    """Manages system-wide path detection and monitoring"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.user_home = Path.home()
    
    def get_system_paths(self) -> List[str]:
        """Get all system paths that should be monitored for system-wide monitoring"""
        paths = []
        
        if self.system == 'windows':
            paths.extend(self._get_windows_paths())
        elif self.system == 'darwin':  # macOS
            paths.extend(self._get_macos_paths())
        else:  # Linux and other Unix-like
            paths.extend(self._get_linux_paths())
        
        # Filter out paths that don't exist or aren't accessible
        valid_paths = []
        for path in paths:
            try:
                path_obj = Path(path)
                if path_obj.exists() and os.access(path, os.R_OK):
                    valid_paths.append(str(path_obj.resolve()))
                    logger.info(f"Added system path: {path}")
                else:
                    logger.debug(f"Skipping inaccessible path: {path}")
            except (OSError, PermissionError) as e:
                logger.debug(f"Cannot access path {path}: {e}")
        
        return valid_paths
    
    def _get_windows_paths(self) -> List[str]:
        """Get Windows-specific paths to monitor"""
        paths = []
        
        # User directories
        paths.extend([
            str(self.user_home / "Desktop"),
            str(self.user_home / "Documents"),
            str(self.user_home / "Downloads"),
            str(self.user_home / "Pictures"),
            str(self.user_home / "Videos"),
            str(self.user_home / "Music"),
        ])
        
        # Common system directories (be careful with these)
        try:
            # Get all drive letters
            drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]
            for drive in drives:
                # Monitor root of each drive (non-recursive to avoid system files)
                paths.append(drive)
            
            # Program Files (for software installations)
            program_files = os.environ.get('PROGRAMFILES', 'C:\\Program Files')
            program_files_x86 = os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)')
            if os.path.exists(program_files):
                paths.append(program_files)
            if os.path.exists(program_files_x86):
                paths.append(program_files_x86)
                
        except Exception as e:
            logger.warning(f"Error getting Windows system paths: {e}")
        
        return paths
    
    def _get_macos_paths(self) -> List[str]:
        """Get macOS-specific paths to monitor"""
        paths = []
        
        # User directories
        paths.extend([
            str(self.user_home / "Desktop"),
            str(self.user_home / "Documents"),
            str(self.user_home / "Downloads"),
            str(self.user_home / "Pictures"),
            str(self.user_home / "Movies"),
            str(self.user_home / "Music"),
        ])
        
        # System directories
        paths.extend([
            "/Applications",
            "/Users",
            "/Volumes",  # External drives
        ])
        
        return paths
    
    def _get_linux_paths(self) -> List[str]:
        """Get Linux-specific paths to monitor"""
        paths = []
        
        # User directories
        paths.extend([
            str(self.user_home / "Desktop"),
            str(self.user_home / "Documents"),
            str(self.user_home / "Downloads"),
            str(self.user_home / "Pictures"),
            str(self.user_home / "Videos"),
            str(self.user_home / "Music"),
            str(self.user_home),  # Home directory
        ])
        
        # System directories
        paths.extend([
            "/home",
            "/mnt",      # Mount points
            "/media",    # Removable media
            "/opt",      # Optional software
            "/usr/local", # Locally installed software
        ])
        
        return paths
    
    def get_user_paths(self) -> List[str]:
        """Get user-specific paths only (safer for monitoring)"""
        paths = []
        
        # Standard user directories across platforms
        user_dirs = [
            "Desktop", "Documents", "Downloads", "Pictures", 
            "Videos", "Music", "OneDrive"
        ]
        
        for dir_name in user_dirs:
            user_path = self.user_home / dir_name
            if user_path.exists():
                paths.append(str(user_path))
        
        # Add home directory itself
        paths.append(str(self.user_home))
        
        return paths
    
    def get_mounted_drives(self) -> List[str]:
        """Get all mounted drives/volumes"""
        drives = []
        
        try:
            # Use psutil to get all disk partitions
            partitions = psutil.disk_partitions()
            
            for partition in partitions:
                # Skip system/virtual filesystems
                if self.system == 'windows':
                    # On Windows, include all drive letters
                    if partition.fstype and partition.mountpoint:
                        drives.append(partition.mountpoint)
                else:
                    # On Unix-like systems, skip system filesystems
                    skip_types = {'proc', 'sysfs', 'devtmpfs', 'tmpfs', 'devpts'}
                    if partition.fstype not in skip_types and partition.mountpoint != '/':
                        drives.append(partition.mountpoint)
        
        except Exception as e:
            logger.warning(f"Error getting mounted drives: {e}")
        
        return drives
    
    def is_safe_path(self, path: str) -> bool:
        """Check if a path is safe to monitor (avoid system-critical paths)"""
        path_obj = Path(path).resolve()
        path_str = str(path_obj).lower()
        
        # Dangerous paths to avoid
        dangerous_paths = []
        
        if self.system == 'windows':
            dangerous_paths.extend([
                'c:\\windows\\system32',
                'c:\\windows\\syswow64',
                'c:\\windows\\winsxs',
                'c:\\system volume information',
                'c:\\$recycle.bin',
                'c:\\pagefile.sys',
                'c:\\hiberfil.sys'
            ])
        else:
            dangerous_paths.extend([
                '/proc', '/sys', '/dev', '/run', '/tmp',
                '/boot', '/etc', '/var/log', '/var/run'
            ])
        
        # Check if path starts with any dangerous path
        for dangerous in dangerous_paths:
            if path_str.startswith(dangerous.lower()):
                return False
        
        return True


def create_system_wide_config(user_paths_only: bool = True, include_drives: bool = False) -> Dict[str, Any]:
    """Create a configuration for system-wide monitoring"""
    path_manager = SystemPathManager()
    
    config = {
        'monitoring': {
            'paths': [],
            'events': ['created', 'modified', 'deleted', 'moved'],
            'recursive': True,
            'ignore_directories': [
                '.git', '__pycache__', 'node_modules', '.vscode', '.idea',
                'venv', '.env', '.svn', '.hg', 'target', 'build', 'dist',
                '$RECYCLE.BIN', 'System Volume Information', '.Trashes',
                '.Spotlight-V100', '.fseventsd'
            ],
            'filters': {
                'include_patterns': [],
                'exclude_patterns': [
                    '*.tmp', '*.swp', '*.log~', '.DS_Store', 'Thumbs.db',
                    '*.pyc', '*.pyo', '*.class', '*.lock', '~$*',
                    'desktop.ini', '.localized'
                ]
            }
        },
        'output': {
            'console': True,
            'console_format': 'simple',
            'log_file': None,
            'log_level': 'INFO'
        },
        'performance': {
            'batch_events': True,
            'batch_timeout': 1.0,  # Longer timeout for system-wide
            'max_events_per_batch': 50,
            'memory_limit_mb': 100,  # Higher limit for system-wide
            'cpu_throttle': True  # Enable throttling for system-wide
        }
    }
    
    if user_paths_only:
        # Safer option - only monitor user directories
        config['monitoring']['paths'] = path_manager.get_user_paths()
    else:
        # Full system monitoring
        config['monitoring']['paths'] = path_manager.get_system_paths()
        
        if include_drives:
            # Add mounted drives
            drives = path_manager.get_mounted_drives()
            config['monitoring']['paths'].extend(drives)
    
    # Filter out unsafe paths
    safe_paths = []
    for path in config['monitoring']['paths']:
        if path_manager.is_safe_path(path):
            safe_paths.append(path)
        else:
            logger.warning(f"Skipping unsafe path: {path}")
    
    config['monitoring']['paths'] = safe_paths
    
    return config
