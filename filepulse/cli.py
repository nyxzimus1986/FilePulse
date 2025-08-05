#!/usr/bin/env python3
"""
Command-line interface for FilePulse filesystem monitor
"""

import argparse
import sys
import os
from pathlib import Path
import logging

# Fix imports for standalone executables
try:
    from .config import Config
    from .monitor import FileSystemMonitor
except ImportError:
    # Fallback for standalone executables
    try:
        from filepulse.config import Config
        from filepulse.monitor import FileSystemMonitor
    except ImportError:
        # Last resort - add current directory to path
        current_dir = Path(__file__).parent
        sys.path.insert(0, str(current_dir.parent))
        from filepulse.config import Config
        from filepulse.monitor import FileSystemMonitor


def setup_logging(level='INFO'):
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def cmd_monitor(args):
    """Handle monitor command"""
    print("FilePulse Filesystem Monitor")
    print("=" * 40)
    
    # Create configuration
    config = Config()
    
    # Set monitoring paths
    paths = args.paths if args.paths else ['.']
    config.set('monitoring.paths', paths)
    
    # Set events to monitor
    if args.events:
        events = args.events.split(',')
        config.set('monitoring.events', events)
    
    # Enable stats if requested
    if args.stats:
        config.set('output.show_stats', True)
    
    print(f"Monitoring paths: {paths}")
    print(f"Events: {config.get('monitoring.events', ['created', 'modified', 'deleted'])}")
    if args.stats:
        print("Statistics: enabled")
    print("Press Ctrl+C to stop monitoring")
    print("-" * 40)
    
    # Create and start monitor
    monitor = FileSystemMonitor(config)
    
    try:
        monitor.run()
    except KeyboardInterrupt:
        print("\nStopping monitor...")
        monitor.stop()
        print("Monitor stopped.")


def cmd_init_config(args):
    """Handle init-config command"""
    config_file = args.config_file
    
    # Create default config
    config = Config()
    
    # Save to file
    config.save(config_file)
    print(f"Default configuration saved to: {config_file}")


def cmd_gui(args):
    """Handle GUI command"""
    try:
        from .gui import main as gui_main
        print("Launching FilePulse GUI...")
        gui_main()
    except ImportError as e:
        print(f"Error: GUI dependencies not available: {e}")
        print("GUI requires tkinter which should be included with Python.")
        sys.exit(1)
    except Exception as e:
        print(f"Error launching GUI: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='FilePulse - Lightweight filesystem monitor',
        prog='filepulse'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Set logging level'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Start filesystem monitoring')
    monitor_parser.add_argument(
        'paths',
        nargs='*',
        help='Paths to monitor (default: current directory)'
    )
    monitor_parser.add_argument(
        '--events',
        help='Comma-separated list of events to monitor (created,modified,deleted,moved)'
    )
    monitor_parser.add_argument(
        '--stats',
        action='store_true',
        help='Show monitoring statistics'
    )
    
    # Init config command
    init_parser = subparsers.add_parser('init-config', help='Create default configuration file')
    init_parser.add_argument(
        'config_file',
        help='Configuration file to create'
    )
    
    # GUI command
    gui_parser = subparsers.add_parser('gui', help='Launch GUI interface')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    
    # Handle commands
    if args.command == 'monitor':
        cmd_monitor(args)
    elif args.command == 'init-config':
        cmd_init_config(args)
    elif args.command == 'gui':
        cmd_gui(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()