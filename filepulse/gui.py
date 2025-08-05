"""
GUI interface for FilePulse filesystem monitor
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import sys
import os
import time
from pathlib import Path
from datetime import datetime
import json

# Add current directory to path for imports
sys.path.insert(0, '.')

from filepulse.config import Config
from filepulse.monitor import FileSystemMonitor
from filepulse.events import FileSystemEvent
from filepulse.output import create_statistics_collector


class FilePulseGUI:
    """Main GUI application for FilePulse"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("FilePulse - Filesystem Monitor")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Application state
        self.monitor = None
        self.is_monitoring = False
        self.config = Config()
        self.stats_collector = None
        self.event_queue = queue.Queue()
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        self.setup_menu()
        
        # Start event processing
        self.process_events()
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Add some initial status
        self.update_status("FilePulse GUI ready - click 'Start Monitoring' to begin")
    
    def setup_styles(self):
        """Configure GUI styles"""
        style = ttk.Style()
        
        # Configure notebook tabs
        style.configure('TNotebook.Tab', padding=[12, 8])
        
        # Configure buttons
        style.configure('Start.TButton', foreground='green')
        style.configure('Stop.TButton', foreground='red')
        style.configure('Clear.TButton', foreground='orange')
    
    def create_widgets(self):
        """Create and layout GUI widgets"""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="FilePulse Filesystem Monitor", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs
        self.create_monitor_tab()
        self.create_config_tab()
        self.create_stats_tab()
        self.create_about_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_monitor_tab(self):
        """Create the main monitoring tab"""
        monitor_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(monitor_frame, text="Monitor")
        
        # Path selection
        path_frame = ttk.LabelFrame(monitor_frame, text="Monitoring Paths", padding="10")
        path_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        path_frame.columnconfigure(0, weight=1)
        
        self.paths_listbox = tk.Listbox(path_frame, height=3)
        self.paths_listbox.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Populate with current paths
        for path in self.config.monitoring_paths:
            self.paths_listbox.insert(tk.END, path)
        
        ttk.Button(path_frame, text="Add Path", command=self.add_path).grid(row=1, column=0, padx=(0, 5))
        ttk.Button(path_frame, text="Remove Path", command=self.remove_path).grid(row=1, column=1, padx=5)
        ttk.Button(path_frame, text="Clear All", command=self.clear_paths).grid(row=1, column=2, padx=(5, 0))
        
        # Event types
        events_frame = ttk.LabelFrame(monitor_frame, text="Events to Monitor", padding="10")
        events_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.event_vars = {}
        events = ['created', 'modified', 'deleted', 'moved']
        for i, event in enumerate(events):
            var = tk.BooleanVar(value=event in self.config.monitoring_events)
            self.event_vars[event] = var
            ttk.Checkbutton(events_frame, text=event.capitalize(), variable=var).grid(
                row=0, column=i, padx=10, sticky=tk.W)
        
        # Control buttons
        control_frame = ttk.Frame(monitor_frame)
        control_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        self.start_button = ttk.Button(control_frame, text="Start Monitoring", 
                                      command=self.start_monitoring, style='Start.TButton')
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_button = ttk.Button(control_frame, text="Stop Monitoring", 
                                     command=self.stop_monitoring, style='Stop.TButton', 
                                     state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=10)
        
        ttk.Button(control_frame, text="Clear Log", command=self.clear_log, 
                  style='Clear.TButton').grid(row=0, column=2, padx=(10, 0))
        
        ttk.Button(control_frame, text="Test Events", command=self.create_test_events, 
                  style='Clear.TButton').grid(row=0, column=3, padx=(10, 0))
        
        # Event log - Split into two tabs
        log_frame = ttk.LabelFrame(monitor_frame, text="Event Monitoring", padding="10")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(1, weight=1)
        monitor_frame.rowconfigure(3, weight=1)
        
        # Event counters
        counter_frame = ttk.Frame(log_frame)
        counter_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        counter_frame.columnconfigure(2, weight=1)
        
        self.user_count_var = tk.StringVar(value="User: 0")
        self.system_count_var = tk.StringVar(value="System: 0")
        self.total_count_var = tk.StringVar(value="Total: 0")
        
        ttk.Label(counter_frame, textvariable=self.user_count_var, 
                 foreground="green").grid(row=0, column=0, padx=(0, 10))
        ttk.Label(counter_frame, textvariable=self.system_count_var, 
                 foreground="orange").grid(row=0, column=1, padx=(0, 10))
        ttk.Label(counter_frame, textvariable=self.total_count_var, 
                 foreground="blue").grid(row=0, column=2, sticky=tk.E)
        
        # Initialize counters
        self.user_event_count = 0
        self.system_event_count = 0
        self.total_event_count = 0
        
        # Create notebook for different event types
        self.log_notebook = ttk.Notebook(log_frame)
        self.log_notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # User Events Tab
        user_frame = ttk.Frame(self.log_notebook, padding="5")
        self.log_notebook.add(user_frame, text="👤 User Changes")
        user_frame.columnconfigure(0, weight=1)
        user_frame.rowconfigure(0, weight=1)
        
        self.user_log_text = scrolledtext.ScrolledText(user_frame, height=10, wrap=tk.WORD)
        self.user_log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # System Events Tab
        system_frame = ttk.Frame(self.log_notebook, padding="5")
        self.log_notebook.add(system_frame, text="⚙️ System Changes")
        system_frame.columnconfigure(0, weight=1)
        system_frame.rowconfigure(0, weight=1)
        
        self.system_log_text = scrolledtext.ScrolledText(system_frame, height=10, wrap=tk.WORD)
        self.system_log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # All Events Tab (combined view)
        all_frame = ttk.Frame(self.log_notebook, padding="5")
        self.log_notebook.add(all_frame, text="📋 All Events")
        all_frame.columnconfigure(0, weight=1)
        all_frame.rowconfigure(0, weight=1)
        
        self.all_log_text = scrolledtext.ScrolledText(all_frame, height=10, wrap=tk.WORD)
        self.all_log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for colored output (for all text widgets)
        for text_widget in [self.user_log_text, self.system_log_text, self.all_log_text]:
            text_widget.tag_configure("created", foreground="green")
            text_widget.tag_configure("modified", foreground="blue")
            text_widget.tag_configure("deleted", foreground="red")
            text_widget.tag_configure("moved", foreground="purple")
            text_widget.tag_configure("timestamp", foreground="gray")
            text_widget.tag_configure("user_event", background="#f0fff0")  # Light green background
            text_widget.tag_configure("system_event", background="#fff8f0")  # Light orange background
    
    def create_config_tab(self):
        """Create the configuration tab"""
        config_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(config_frame, text="Configuration")
        
        # Filters section
        filters_frame = ttk.LabelFrame(config_frame, text="File Filters", padding="10")
        filters_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        filters_frame.columnconfigure(1, weight=1)
        
        ttk.Label(filters_frame, text="Include Patterns:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.include_entry = ttk.Entry(filters_frame, width=40)
        self.include_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        self.include_entry.insert(0, ", ".join(self.config.include_patterns))
        
        ttk.Label(filters_frame, text="Exclude Patterns:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.exclude_entry = ttk.Entry(filters_frame, width=40)
        self.exclude_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        self.exclude_entry.insert(0, ", ".join(self.config.exclude_patterns))
        
        # Options section
        options_frame = ttk.LabelFrame(config_frame, text="Options", padding="10")
        options_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.recursive_var = tk.BooleanVar(value=self.config.is_recursive)
        ttk.Checkbutton(options_frame, text="Monitor subdirectories recursively", 
                       variable=self.recursive_var).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.batch_var = tk.BooleanVar(value=self.config.get('performance.batch_events', True))
        ttk.Checkbutton(options_frame, text="Batch events to reduce noise", 
                       variable=self.batch_var).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.system_wide_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="System-wide monitoring (user directories)", 
                       variable=self.system_wide_var).grid(row=2, column=0, sticky=tk.W, pady=2)
        
        # Performance section
        perf_frame = ttk.LabelFrame(config_frame, text="Performance", padding="10")
        perf_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        perf_frame.columnconfigure(1, weight=1)
        
        ttk.Label(perf_frame, text="Memory Limit (MB):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.memory_var = tk.StringVar(value=str(self.config.get('performance.memory_limit_mb', 50)))
        memory_spinbox = ttk.Spinbox(perf_frame, from_=10, to=500, textvariable=self.memory_var, width=10)
        memory_spinbox.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # Buttons
        button_frame = ttk.Frame(config_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Apply Settings", command=self.apply_config).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Save Config", command=self.save_config).grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="Load Config", command=self.load_config).grid(row=0, column=2, padx=(10, 0))
        
        # Help text
        help_frame = ttk.LabelFrame(config_frame, text="Pattern Help", padding="10")
        help_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        help_text = """• Leave Include Patterns empty to monitor all files/folders
• Exclude Patterns use wildcards: *.tmp, temp*, *cache*
• Directories are monitored regardless of file extension patterns
• Use comma-separated patterns: *.log, *.tmp, temp*"""
        
        ttk.Label(help_frame, text=help_text, font=('Arial', 8), 
                 justify=tk.LEFT, foreground="gray").grid(row=0, column=0, sticky=tk.W)
    
    def create_stats_tab(self):
        """Create the statistics tab"""
        stats_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(stats_frame, text="Statistics")
        
        # Statistics display
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=20, width=60)
        self.stats_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.rowconfigure(0, weight=1)
        
        # Refresh button
        ttk.Button(stats_frame, text="Refresh Statistics", 
                  command=self.refresh_stats).grid(row=1, column=0, pady=10)
    
    def create_about_tab(self):
        """Create the about tab"""
        about_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(about_frame, text="About")
        
        about_text = """
FilePulse - Filesystem Monitor v0.1.0

A lightweight system-wide filesystem monitor with minimal resource usage.

Features:
• Real-time filesystem monitoring
• Configurable event filtering  
• Multiple output formats
• Low resource usage
• Cross-platform support

Built with Python and Tkinter
        """
        
        ttk.Label(about_frame, text=about_text, font=('Arial', 10), 
                 justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
    
    def setup_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Configuration...", command=self.load_config)
        file_menu.add_command(label="Save Configuration...", command=self.save_config)
        file_menu.add_separator()
        file_menu.add_command(label="Export Log...", command=self.export_log)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Clear Log", command=self.clear_log)
        view_menu.add_command(label="Refresh Statistics", command=self.refresh_stats)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=lambda: self.notebook.select(3))
    
    def add_path(self):
        """Add a path to monitor"""
        path = filedialog.askdirectory(title="Select Directory to Monitor")
        if path:
            self.paths_listbox.insert(tk.END, path)
    
    def remove_path(self):
        """Remove selected path"""
        selection = self.paths_listbox.curselection()
        if selection:
            self.paths_listbox.delete(selection[0])
    
    def clear_paths(self):
        """Clear all paths"""
        self.paths_listbox.delete(0, tk.END)
    
    def apply_config(self):
        """Apply current configuration settings"""
        
        # Check if system-wide monitoring is enabled
        if self.system_wide_var.get():
            try:
                from .system_monitor import create_system_wide_config
                system_config = create_system_wide_config(user_paths_only=True, include_drives=False)
                
                # Apply system-wide configuration
                for key, value in system_config.items():
                    if isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            self.config.set(f"{key}.{sub_key}", sub_value)
                    else:
                        self.config.set(key, value)
                
                # Update paths display
                self.paths_listbox.delete(0, tk.END)
                for path in self.config.monitoring_paths:
                    self.paths_listbox.insert(tk.END, path)
                
                messagebox.showinfo("System-wide Monitoring", 
                                  f"Enabled system-wide monitoring for {len(self.config.monitoring_paths)} locations")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to enable system-wide monitoring: {e}")
                return
        else:
            # Update paths
            paths = [self.paths_listbox.get(i) for i in range(self.paths_listbox.size())]
            self.config.set('monitoring.paths', paths or ['.'])
        
        # Update events
        events = [event for event, var in self.event_vars.items() if var.get()]
        self.config.set('monitoring.events', events or ['created', 'modified', 'deleted', 'moved'])
        
        # Update filters
        include_patterns = [p.strip() for p in self.include_entry.get().split(',') if p.strip()]
        exclude_patterns = [p.strip() for p in self.exclude_entry.get().split(',') if p.strip()]
        self.config.set('monitoring.filters.include_patterns', include_patterns)
        self.config.set('monitoring.filters.exclude_patterns', exclude_patterns)
        
        # Update options
        self.config.set('monitoring.recursive', self.recursive_var.get())
        self.config.set('performance.batch_events', self.batch_var.get())
        
        # Validate and set memory limit
        try:
            memory_limit = int(self.memory_var.get())
            if memory_limit < 10:
                memory_limit = 10
                self.memory_var.set("10")
                messagebox.showwarning("Invalid Memory Limit", "Memory limit must be at least 10 MB. Set to 10 MB.")
            elif memory_limit > 1000:
                memory_limit = 1000
                self.memory_var.set("1000")
                messagebox.showwarning("Invalid Memory Limit", "Memory limit cannot exceed 1000 MB. Set to 1000 MB.")
            
            self.config.set('performance.memory_limit_mb', memory_limit)
        except ValueError:
            messagebox.showerror("Invalid Memory Limit", "Memory limit must be a valid number. Using default of 50 MB.")
            self.memory_var.set("50")
            self.config.set('performance.memory_limit_mb', 50)
        
        messagebox.showinfo("Configuration", "Settings applied successfully!")
        self.update_status("Configuration updated")
    
    def save_config(self):
        """Save configuration to file"""
        filename = filedialog.asksaveasfilename(
            title="Save Configuration",
            defaultextension=".yaml",
            filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.apply_config()  # Apply current settings first
                self.config.save(filename)
                messagebox.showinfo("Save", f"Configuration saved to {filename}")
                self.update_status(f"Configuration saved to {Path(filename).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save configuration: {e}")
    
    def load_config(self):
        """Load configuration from file"""
        filename = filedialog.askopenfilename(
            title="Load Configuration",
            filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.config = Config(filename)
                self.refresh_config_ui()
                messagebox.showinfo("Load", f"Configuration loaded from {filename}")
                self.update_status(f"Configuration loaded from {Path(filename).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load configuration: {e}")
    
    def refresh_config_ui(self):
        """Refresh UI with current configuration"""
        # Update paths
        self.paths_listbox.delete(0, tk.END)
        for path in self.config.monitoring_paths:
            self.paths_listbox.insert(tk.END, path)
        
        # Update events
        for event, var in self.event_vars.items():
            var.set(event in self.config.monitoring_events)
        
        # Update filters
        self.include_entry.delete(0, tk.END)
        self.include_entry.insert(0, ", ".join(self.config.include_patterns))
        self.exclude_entry.delete(0, tk.END)
        self.exclude_entry.insert(0, ", ".join(self.config.exclude_patterns))
        
        # Update options
        self.recursive_var.set(self.config.is_recursive)
        self.batch_var.set(self.config.get('performance.batch_events', True))
        self.memory_var.set(str(self.config.get('performance.memory_limit_mb', 50)))
    
    def start_monitoring(self):
        """Start filesystem monitoring"""
        if self.is_monitoring:
            return
        
        try:
            # Apply current configuration
            self.apply_config()
            
            # Debug: Print the memory limit that will be used
            memory_limit = self.config.get('performance.memory_limit_mb', 50)
            print(f"[GUI] Starting monitor with memory limit: {memory_limit} MB")
            
            # Optimize for GUI responsiveness
            self.config.set('performance.batch_timeout', 0.3)  # Faster batching for GUI
            self.config.set('performance.max_events_per_batch', 25)  # Reasonable batch size
            
            # Create GUI output handler
            def gui_output_handler(events):
                for event in events:
                    self.event_queue.put(event)
            
            # Create monitor with GUI output
            self.monitor = FileSystemMonitor(self.config)
            
            # Debug: Verify the resource monitor got the right limit
            if self.monitor.resource_monitor:
                print(f"[GUI] ResourceMonitor created with limit: {self.monitor.resource_monitor.memory_limit_mb} MB")
            else:
                print("[GUI] WARNING: No ResourceMonitor created!")
            
            self.monitor.event_handler.add_output_handler(gui_output_handler)
            
            # Add statistics collector
            self.stats_collector = create_statistics_collector()
            self.monitor.event_handler.add_output_handler(self.stats_collector)
            
            # Start monitoring in separate thread
            def monitor_thread():
                try:
                    self.monitor.start()
                    self.event_queue.put("MONITOR_STARTED")
                    self.monitor.run()
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    self.event_queue.put(f"ERROR: {e}")
            
            self.monitor_thread = threading.Thread(target=monitor_thread, daemon=True)
            self.monitor_thread.start()
            
            # Update UI
            self.is_monitoring = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.update_status("Monitoring started...")
            
            # Set up periodic event handler flushing for responsive GUI
            def flush_events():
                if self.is_monitoring and self.monitor and self.monitor.event_handler:
                    self.monitor.event_handler.flush()
                if self.is_monitoring:
                    self.root.after(500, flush_events)  # Flush every 500ms for better responsiveness
            
            # Set up periodic stats refresh
            def refresh_stats_periodically():
                if self.is_monitoring:
                    # Check if statistics tab is currently visible
                    current_tab = self.notebook.index(self.notebook.select())
                    if current_tab == 2:  # Statistics tab
                        self.refresh_stats()
                    self.root.after(3000, refresh_stats_periodically)  # Refresh every 3 seconds
            
            self.root.after(500, flush_events)
            self.root.after(3000, refresh_stats_periodically)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start monitoring: {e}")
            self.update_status(f"Error: {e}")
    
    def stop_monitoring(self):
        """Stop filesystem monitoring"""
        if not self.is_monitoring:
            return
        
        try:
            if self.monitor:
                self.monitor.stop()
            
            self.is_monitoring = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.update_status("Monitoring stopped")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop monitoring: {e}")
    
    def clear_log(self):
        """Clear all event logs"""
        self.user_log_text.delete(1.0, tk.END)
        self.system_log_text.delete(1.0, tk.END)
        self.all_log_text.delete(1.0, tk.END)
        
        # Reset counters
        self.user_event_count = 0
        self.system_event_count = 0
        self.total_event_count = 0
        self.update_counters()
        
        self.update_status("All logs cleared")
    
    def create_test_events(self):
        """Create test files and folders to verify event detection"""
        import tempfile
        import time
        from pathlib import Path
        
        try:
            base_path = Path('.')
            timestamp = int(time.time())
            
            # Create test folder
            test_folder = base_path / f"test_folder_{timestamp}"
            test_folder.mkdir(exist_ok=True)
            
            # Create test file
            test_file = base_path / f"test_file_{timestamp}.txt"
            test_file.write_text(f"Test file created at {time.ctime()}")
            
            # Create file inside folder
            inner_file = test_folder / "inner_test.txt"
            inner_file.write_text("File inside test folder")
            
            messagebox.showinfo("Test Events", 
                              f"Created test events:\n"
                              f"• Folder: {test_folder.name}\n"
                              f"• File: {test_file.name}\n"
                              f"• Inner file: {inner_file.name}\n\n"
                              f"Check the event logs to see if they appear!")
            
            self.update_status(f"Created test events - check logs")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create test events: {e}")
    
    def refresh_stats(self):
        """Refresh statistics display"""
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, "FilePulse Statistics\n")
        self.stats_text.insert(tk.END, "=" * 30 + "\n\n")
        
        # Show current memory usage
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            memory_limit = self.config.get('performance.memory_limit_mb', 50)
            
            self.stats_text.insert(tk.END, f"Memory Usage: {memory_mb:.1f} MB\n")
            self.stats_text.insert(tk.END, f"Memory Limit: {memory_limit} MB\n")
            self.stats_text.insert(tk.END, f"Memory Usage: {(memory_mb/memory_limit)*100:.1f}% of limit\n")
            
            # Show resource monitor status
            if self.is_monitoring and self.monitor and self.monitor.resource_monitor:
                rm = self.monitor.resource_monitor
                self.stats_text.insert(tk.END, f"Resource Monitor: ACTIVE\n")
                self.stats_text.insert(tk.END, f"Resource Monitor Limit: {rm.memory_limit_mb} MB\n")
                self.stats_text.insert(tk.END, f"Resource Monitor Thread: {'Running' if rm._monitoring else 'Stopped'}\n")
            else:
                self.stats_text.insert(tk.END, f"Resource Monitor: NOT AVAILABLE\n")
            
            self.stats_text.insert(tk.END, "\n")
        except Exception as e:
            self.stats_text.insert(tk.END, f"Memory info unavailable: {e}\n\n")
        
        # Show monitoring status
        if self.is_monitoring:
            self.stats_text.insert(tk.END, "Monitoring Status: ACTIVE\n")
            self.stats_text.insert(tk.END, f"Monitored Paths: {len(self.config.monitoring_paths)}\n")
            self.stats_text.insert(tk.END, f"Event Types: {', '.join(self.config.monitoring_events)}\n\n")
        else:
            self.stats_text.insert(tk.END, "Monitoring Status: STOPPED\n\n")
        
        # Show event counts
        self.stats_text.insert(tk.END, f"User Events: {self.user_event_count}\n")
        self.stats_text.insert(tk.END, f"System Events: {self.system_event_count}\n")
        self.stats_text.insert(tk.END, f"Total Events: {self.total_event_count}\n\n")
        
        if self.stats_collector:
            stats = self.stats_collector.get_stats()
            
            for key, value in stats.items():
                if isinstance(value, dict):
                    self.stats_text.insert(tk.END, f"{key.replace('_', ' ').title()}:\n")
                    for sub_key, sub_value in value.items():
                        self.stats_text.insert(tk.END, f"  {sub_key}: {sub_value}\n")
                    self.stats_text.insert(tk.END, "\n")
                else:
                    self.stats_text.insert(tk.END, f"{key.replace('_', ' ').title()}: {value}\n")
        else:
            self.stats_text.insert(tk.END, "Additional statistics available when monitoring is active.\n")
    
    def export_log(self):
        """Export current logs to files"""
        from tkinter import messagebox
        
        # Ask user which log to export
        export_choice = messagebox.askyesnocancel(
            "Export Logs",
            "Export which logs?\n\nYes = All logs\nNo = Current tab only\nCancel = Cancel"
        )
        
        if export_choice is None:  # Cancel
            return
        
        if export_choice:  # Yes - Export all logs
            # Export all logs to separate files
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            
            logs_to_export = [
                (self.user_log_text, f"filepulse_user_events_{timestamp}.txt", "User Events"),
                (self.system_log_text, f"filepulse_system_events_{timestamp}.txt", "System Events"),
                (self.all_log_text, f"filepulse_all_events_{timestamp}.txt", "All Events")
            ]
            
            exported_files = []
            for text_widget, filename, description in logs_to_export:
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"FilePulse {description} Log\n")
                        f.write(f"Exported on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write("=" * 50 + "\n\n")
                        f.write(text_widget.get(1.0, tk.END))
                    exported_files.append(filename)
                except Exception as e:
                    messagebox.showerror("Export Error", f"Failed to export {description}: {e}")
                    return
            
            messagebox.showinfo("Export Complete", 
                              f"Exported logs to:\n" + "\n".join([f"• {f}" for f in exported_files]))
            self.update_status(f"Exported {len(exported_files)} log files")
            
        else:  # No - Export current tab only
            # Get current tab
            current_tab = self.log_notebook.index(self.log_notebook.select())
            
            if current_tab == 0:
                text_widget = self.user_log_text
                default_name = "filepulse_user_events.txt"
                log_type = "User Events"
            elif current_tab == 1:
                text_widget = self.system_log_text
                default_name = "filepulse_system_events.txt"
                log_type = "System Events"
            else:
                text_widget = self.all_log_text
                default_name = "filepulse_all_events.txt"
                log_type = "All Events"
            
            filename = filedialog.asksaveasfilename(
                title=f"Export {log_type} Log",
                defaultextension=".txt",
                initialvalue=default_name,
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if filename:
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"FilePulse {log_type} Log\n")
                        f.write(f"Exported on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write("=" * 50 + "\n\n")
                        f.write(text_widget.get(1.0, tk.END))
                    messagebox.showinfo("Export", f"{log_type} log exported to {filename}")
                    self.update_status(f"{log_type} log exported to {Path(filename).name}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to export log: {e}")
    
    def process_events(self):
        """Process events from the queue"""
        try:
            while True:
                try:
                    event = self.event_queue.get_nowait()
                    
                    if isinstance(event, FileSystemEvent):
                        self.add_event_to_log(event)
                    elif event == "MONITOR_STARTED":
                        self.update_status("Monitoring active - watching for filesystem events")
                    elif isinstance(event, str) and event.startswith("ERROR:"):
                        self.update_status(event)
                        messagebox.showerror("Monitor Error", event[6:])
                        self.stop_monitoring()
                        
                except queue.Empty:
                    break
                    
        except Exception as e:
            self.update_status(f"Event processing error: {e}")
        
        # Schedule next check
        self.root.after(100, self.process_events)
    
    def update_counters(self):
        """Update the event counters display"""
        self.user_count_var.set(f"👤 User: {self.user_event_count}")
        self.system_count_var.set(f"⚙️ System: {self.system_event_count}")
        self.total_count_var.set(f"📊 Total: {self.total_event_count}")
    
    def is_user_event(self, event: FileSystemEvent) -> bool:
        """Determine if an event is likely user-initiated or system-generated"""
        import time
        from pathlib import Path
        
        # Get the path components
        path = Path(event.src_path)
        path_str = str(path).lower()
        filename = path.name.lower()
        
        # System-generated patterns (these go to system log)
        system_patterns = [
            # Windows system files
            'thumbs.db', 'desktop.ini', '.ds_store', 'hiberfil.sys', 'pagefile.sys',
            # Temporary files
            '.tmp', '.temp', '~$', '.swp', '.swo', '.log~',
            # Cache and metadata
            '.cache', '__pycache__', '.pyc', '.pyo',
            # System directories
            'system volume information', '$recycle.bin', '.trashes',
            # Application logs and temp files
            '.lock', '.pid', '.sock',
            # Browser and app caches
            'cache', 'cookies', 'history', 'sessions'
        ]
        
        # Check if filename matches system patterns
        for pattern in system_patterns:
            if pattern in filename:
                return False
        
        # Check if path contains system directories
        system_dirs = [
            'appdata', 'temp', 'tmp', 'cache', 'logs', 'system32',
            'windows', 'program files', 'programdata'
        ]
        
        for sys_dir in system_dirs:
            if sys_dir in path_str:
                return False
        
        # User directories (these are more likely user events)
        user_dirs = [
            'desktop', 'documents', 'downloads', 'pictures', 'videos', 'music',
            'onedrive', 'dropbox', 'google drive'
        ]
        
        for user_dir in user_dirs:
            if user_dir in path_str:
                return True
        
        # File extensions that are typically user files
        user_extensions = [
            '.txt', '.doc', '.docx', '.pdf', '.jpg', '.jpeg', '.png', '.gif',
            '.mp4', '.mp3', '.zip', '.rar', '.exe', '.msi', '.py', '.js',
            '.html', '.css', '.json', '.xml', '.csv', '.xlsx'
        ]
        
        if path.suffix.lower() in user_extensions:
            return True
        
        # Default to user event if we can't classify it
        return True
    
    def add_event_to_log(self, event: FileSystemEvent):
        """Add an event to the appropriate log display"""
        timestamp = event.datetime.strftime('%H:%M:%S')
        
        # Update total count
        self.total_event_count += 1
        
        # Determine if this is a user or system event
        is_user = self.is_user_event(event)
        
        # Update specific counters
        if is_user:
            self.user_event_count += 1
        else:
            self.system_event_count += 1
        
        # Create the log entry
        def create_log_entry(text_widget, tag_suffix=""):
            # Insert timestamp
            text_widget.insert(tk.END, f"[{timestamp}] ", "timestamp")
            
            # Insert event type with color
            event_text = f"{event.event_type.upper()}: "
            text_widget.insert(tk.END, event_text, event.event_type)
            
            # Insert path
            if event.event_type == 'moved' and event.dest_path:
                text_widget.insert(tk.END, f"{event.src_path} -> {event.dest_path}")
            else:
                text_widget.insert(tk.END, f"{event.src_path}")
            
            # Add event type background
            if tag_suffix:
                # Get the line we just added
                line_start = text_widget.index("end-2l linestart")
                line_end = text_widget.index("end-1l lineend")
                text_widget.tag_add(tag_suffix, line_start, line_end)
            
            text_widget.insert(tk.END, "\n")
            # Auto-scroll to bottom
            text_widget.see(tk.END)
        
        # Add to appropriate specific log
        if is_user:
            create_log_entry(self.user_log_text, "user_event")
        else:
            create_log_entry(self.system_log_text, "system_event")
        
        # Always add to combined log
        create_log_entry(self.all_log_text, "user_event" if is_user else "system_event")
        
        # Update counter displays
        self.update_counters()
    
    def update_status(self, message):
        """Update status bar"""
        self.status_var.set(message)
    
    def on_closing(self):
        """Handle application closing"""
        if self.is_monitoring:
            if messagebox.askokcancel("Quit", "Monitoring is active. Stop monitoring and quit?"):
                self.stop_monitoring()
                self.root.after(500, self.root.destroy)  # Give time for cleanup
        else:
            self.root.destroy()


def main():
    """Main entry point for GUI"""
    root = tk.Tk()
    app = FilePulseGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
