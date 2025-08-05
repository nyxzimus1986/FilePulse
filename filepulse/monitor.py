"""
Core filesystem monitoring functionality
"""

import os
import time
import threading
import logging
import psutil
from typing import List, Optional, Callable
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler as WatchdogHandler

from .config import Config
from .events import FileSystemEvent, EventHandler
from .output import create_output_handlers

logger = logging.getLogger(__name__)


class FilePulseHandler(WatchdogHandler):
    """Custom watchdog event handler"""
    
    def __init__(self, event_handler: EventHandler):
        super().__init__()
        self.event_handler = event_handler
    
    def on_created(self, event):
        fs_event = FileSystemEvent(
            event_type='created',
            src_path=event.src_path,
            is_directory=event.is_directory
        )
        self.event_handler.handle_event(fs_event)
    
    def on_deleted(self, event):
        fs_event = FileSystemEvent(
            event_type='deleted',
            src_path=event.src_path,
            is_directory=event.is_directory
        )
        self.event_handler.handle_event(fs_event)
    
    def on_modified(self, event):
        # Avoid duplicate events for directory modifications
        if event.is_directory:
            return
            
        fs_event = FileSystemEvent(
            event_type='modified',
            src_path=event.src_path,
            is_directory=event.is_directory
        )
        self.event_handler.handle_event(fs_event)
    
    def on_moved(self, event):
        fs_event = FileSystemEvent(
            event_type='moved',
            src_path=event.src_path,
            dest_path=event.dest_path,
            is_directory=event.is_directory
        )
        self.event_handler.handle_event(fs_event)


class ResourceMonitor:
    """Monitor resource usage to ensure minimal impact"""
    
    def __init__(self, memory_limit_mb: int = 50, cpu_throttle: bool = False):
        self.memory_limit_mb = memory_limit_mb
        self.cpu_throttle = cpu_throttle
        self.process = psutil.Process()
        self._monitoring = False
        self._monitor_thread = None
    
    def start_monitoring(self):
        """Start resource monitoring"""
        self._monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_resources, daemon=True)
        self._monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop resource monitoring"""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=1.0)
    
    def _monitor_resources(self):
        """Monitor and limit resource usage"""
        logger.info(f"Resource monitoring started with memory limit: {self.memory_limit_mb}MB")
        
        while self._monitoring:
            try:
                # Check memory usage
                memory_mb = self.process.memory_info().rss / 1024 / 1024
                
                # Log memory usage periodically for debugging
                if hasattr(self, '_debug_counter'):
                    self._debug_counter += 1
                else:
                    self._debug_counter = 1
                
                # Log every 5 checks (15 seconds)
                if self._debug_counter % 5 == 0:
                    logger.info(f"Memory check: {memory_mb:.1f}MB / {self.memory_limit_mb}MB limit")
                
                if memory_mb > self.memory_limit_mb:
                    logger.warning(f"MEMORY LIMIT EXCEEDED: {memory_mb:.1f}MB > {self.memory_limit_mb}MB")
                    print(f"[FilePulse] MEMORY LIMIT EXCEEDED: {memory_mb:.1f}MB > {self.memory_limit_mb}MB")
                    
                    # Try to reduce memory usage
                    self._reduce_memory_usage()
                
                # CPU throttling if enabled
                if self.cpu_throttle:
                    cpu_percent = self.process.cpu_percent()
                    if cpu_percent > 10:  # Throttle if using more than 10% CPU
                        time.sleep(0.1)
                
                time.sleep(3)  # Check every 3 seconds
                
            except Exception as e:
                logger.error(f"Error monitoring resources: {e}")
                break
    
    def _reduce_memory_usage(self):
        """Attempt to reduce memory usage when limit is exceeded"""
        try:
            import gc
            
            print("[FilePulse] Attempting to reduce memory usage...")
            logger.info("Starting memory cleanup procedure")
            
            # Force garbage collection
            collected = gc.collect()
            logger.info(f"Garbage collection freed {collected} objects")
            print(f"[FilePulse] Garbage collection freed {collected} objects")
            
            # Check if we have access to the event handler to flush events
            if hasattr(self, '_event_handler_ref') and self._event_handler_ref:
                try:
                    event_handler = self._event_handler_ref()
                    if event_handler:
                        event_handler.flush()
                        logger.info("Flushed pending events to reduce memory")
                        print("[FilePulse] Flushed pending events to reduce memory")
                    else:
                        logger.warning("Event handler reference is None")
                except Exception as ref_e:
                    logger.warning(f"Failed to flush events: {ref_e}")
            else:
                logger.warning("No event handler reference available for memory cleanup")
            
            # Sleep briefly to allow memory cleanup
            time.sleep(1)
            
            # Check memory again
            new_memory_mb = self.process.memory_info().rss / 1024 / 1024
            reduction = self.process.memory_info().rss / 1024 / 1024
            logger.info(f"Memory usage after cleanup: {new_memory_mb:.1f}MB")
            print(f"[FilePulse] Memory after cleanup: {new_memory_mb:.1f}MB")
            
        except Exception as e:
            logger.error(f"Error reducing memory usage: {e}")
            print(f"[FilePulse] Error during memory cleanup: {e}")
    
    def set_event_handler_ref(self, event_handler_ref):
        """Set a weak reference to the event handler for memory management"""
        import weakref
        self._event_handler_ref = weakref.ref(event_handler_ref)


class FileSystemMonitor:
    """Main filesystem monitor class"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.observer = Observer()
        self.event_handler = None
        self.resource_monitor = None
        self.is_running = False
        
        # Setup logging
        self._setup_logging()
        
        # Initialize components
        self._initialize()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_level = getattr(logging, self.config.get('output.log_level', 'INFO').upper())
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Setup file logging if specified
        log_file = self.config.get('output.log_file')
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    
    def _initialize(self):
        """Initialize monitor components"""
        # Create output handlers
        output_handlers = create_output_handlers(self.config)
        
        # Create event handler
        self.event_handler = EventHandler(self.config, output_handlers)
        
        # Setup resource monitoring
        memory_limit = self.config.get('performance.memory_limit_mb', 50)
        cpu_throttle = self.config.get('performance.cpu_throttle', False)
        self.resource_monitor = ResourceMonitor(memory_limit, cpu_throttle)
        
        # Connect event handler to resource monitor for memory management
        self.resource_monitor.set_event_handler_ref(self.event_handler)
        
        # Setup watchdog handlers for each path
        self._setup_watchers()
    
    def _setup_watchers(self):
        """Setup filesystem watchers for configured paths"""
        paths = self.config.monitoring_paths
        recursive = self.config.is_recursive
        
        handler = FilePulseHandler(self.event_handler)
        
        for path in paths:
            if not os.path.exists(path):
                logger.warning(f"Path does not exist: {path}")
                continue
            
            try:
                self.observer.schedule(handler, path, recursive=recursive)
                logger.info(f"Watching path: {path} (recursive: {recursive})")
            except Exception as e:
                logger.error(f"Failed to setup watcher for {path}: {e}")
    
    def start(self):
        """Start the filesystem monitor"""
        if self.is_running:
            logger.warning("Monitor is already running")
            return
        
        try:
            # Start resource monitoring
            self.resource_monitor.start_monitoring()
            
            # Start filesystem observer
            self.observer.start()
            self.is_running = True
            
            logger.info("FilePulse monitor started")
            logger.info(f"Monitoring paths: {self.config.monitoring_paths}")
            logger.info(f"Monitoring events: {self.config.monitoring_events}")
            
        except Exception as e:
            logger.error(f"Failed to start monitor: {e}")
            raise
    
    def stop(self):
        """Stop the filesystem monitor"""
        if not self.is_running:
            return
        
        logger.info("Stopping FilePulse monitor...")
        
        # Stop observer
        self.observer.stop()
        self.observer.join()
        
        # Stop resource monitoring
        self.resource_monitor.stop_monitoring()
        
        # Flush any pending events
        if self.event_handler:
            self.event_handler.flush()
        
        self.is_running = False
        logger.info("FilePulse monitor stopped")
    
    def run(self):
        """Run the monitor (blocking)"""
        self.start()
        try:
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        finally:
            self.stop()
    
    def get_status(self) -> dict:
        """Get monitor status information"""
        return {
            'is_running': self.is_running,
            'monitored_paths': self.config.monitoring_paths,
            'monitored_events': self.config.monitoring_events,
            'memory_usage_mb': psutil.Process().memory_info().rss / 1024 / 1024,
            'cpu_percent': psutil.Process().cpu_percent()
        }
    
    def reload_config(self, config_path: Optional[str] = None):
        """Reload configuration"""
        if self.is_running:
            logger.info("Stopping monitor for configuration reload...")
            self.stop()
        
        # Reload configuration
        self.config = Config(config_path) if config_path else Config()
        
        # Reinitialize components
        self._initialize()
        
        logger.info("Configuration reloaded")
    
    def add_path(self, path: str, recursive: bool = None):
        """Add a path to monitor"""
        if recursive is None:
            recursive = self.config.is_recursive
        
        if not os.path.exists(path):
            raise ValueError(f"Path does not exist: {path}")
        
        handler = FilePulseHandler(self.event_handler)
        self.observer.schedule(handler, path, recursive=recursive)
        
        # Update config
        paths = self.config.monitoring_paths.copy()
        if path not in paths:
            paths.append(path)
            self.config.set('monitoring.paths', paths)
        
        logger.info(f"Added monitoring path: {path}")
    
    def remove_path(self, path: str):
        """Remove a path from monitoring"""
        # Remove from observer (this is tricky with watchdog, might need restart)
        logger.warning("Removing paths requires monitor restart")
        
        # Update config
        paths = self.config.monitoring_paths.copy()
        if path in paths:
            paths.remove(path)
            self.config.set('monitoring.paths', paths)
        
        logger.info(f"Removed monitoring path: {path}")


def create_monitor(config_path: Optional[str] = None) -> FileSystemMonitor:
    """Create a FileSystemMonitor instance"""
    config = Config(config_path) if config_path else Config()
    return FileSystemMonitor(config)
