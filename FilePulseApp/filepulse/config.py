"""
Configuration management for FilePulse
"""

import os
import yaml
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for FilePulse"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self._config = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file or use defaults"""
        if self.config_path and os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self._config = yaml.safe_load(f) or {}
                logger.info(f"Loaded config from {self.config_path}")
            except Exception as e:
                logger.warning(f"Failed to load config from {self.config_path}: {e}")
                self._config = {}
        
        # Apply defaults
        self._apply_defaults()
    
    def _apply_defaults(self):
        """Apply default configuration values"""
        defaults = {
            'monitoring': {
                'paths': ['.'],
                'events': ['created', 'modified', 'deleted', 'moved'],
                'recursive': True,
                'ignore_directories': ['.git', '__pycache__', 'node_modules', '.vscode'],
                'filters': {
                    'include_patterns': [],
                    'exclude_patterns': ['*.tmp', '*.swp', '*.log~', '.DS_Store'],
                    'min_file_size': 0,
                    'max_file_size': None
                }
            },
            'output': {
                'console': True,
                'console_format': 'simple',  # simple, detailed, json
                'log_file': None,
                'log_level': 'INFO',
                'json_output': False,
                'timestamp_format': '%Y-%m-%d %H:%M:%S'
            },
            'performance': {
                'batch_events': True,
                'batch_timeout': 0.5,  # seconds
                'max_events_per_batch': 100,
                'memory_limit_mb': 50,
                'cpu_throttle': False
            }
        }
        
        # Merge defaults with loaded config
        self._config = self._deep_merge(defaults, self._config)
    
    def _deep_merge(self, default: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries"""
        result = default.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, path: Optional[str] = None):
        """Save current configuration to file"""
        save_path = path or self.config_path
        if not save_path:
            raise ValueError("No config path specified")
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'w', encoding='utf-8') as f:
            yaml.dump(self._config, f, default_flow_style=False, indent=2)
        
        logger.info(f"Configuration saved to {save_path}")
    
    @property
    def monitoring_paths(self) -> List[str]:
        """Get list of paths to monitor"""
        return self.get('monitoring.paths', ['.'])
    
    @property
    def monitoring_events(self) -> List[str]:
        """Get list of events to monitor"""
        return self.get('monitoring.events', ['created', 'modified', 'deleted', 'moved'])
    
    @property
    def is_recursive(self) -> bool:
        """Check if monitoring should be recursive"""
        return self.get('monitoring.recursive', True)
    
    @property
    def ignore_directories(self) -> List[str]:
        """Get list of directories to ignore"""
        return self.get('monitoring.ignore_directories', [])
    
    @property
    def include_patterns(self) -> List[str]:
        """Get include patterns for file filtering"""
        return self.get('monitoring.filters.include_patterns', [])
    
    @property
    def exclude_patterns(self) -> List[str]:
        """Get exclude patterns for file filtering"""
        return self.get('monitoring.filters.exclude_patterns', [])
    
    def to_dict(self) -> Dict:
        """Return configuration as dictionary"""
        return self._config.copy()


def create_default_config(path: str):
    """Create a default configuration file"""
    config = Config()
    config.save(path)
    return config
