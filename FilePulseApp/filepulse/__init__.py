"""
FilePulse - A lightweight system-wide filesystem monitor
"""

__version__ = "0.1.0"
__author__ = "FilePulse Developer"
__email__ = "developer@filepulse.com"

from .monitor import FileSystemMonitor
from .config import Config
from .events import EventHandler, EventFilter

__all__ = [
    "FileSystemMonitor",
    "Config", 
    "EventHandler",
    "EventFilter",
]
