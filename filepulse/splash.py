#!/usr/bin/env python3
"""
FilePulse Splash Screen
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from pathlib import Path

class FilePulseSplash:
    def __init__(self):
        self.splash = tk.Toplevel()
        self.splash.title("FilePulse")
        self.splash.geometry("400x300")
        self.splash.resizable(False, False)
        
        # Center the splash screen
        self.center_window()
        
        # Remove window decorations for a clean look
        self.splash.overrideredirect(True)
        
        # Configure the splash screen
        self.setup_splash()
        
        # Start the loading animation
        self.animate_loading()
    
    def center_window(self):
        """Center the splash screen on the screen"""
        self.splash.update_idletasks()
        width = 400
        height = 300
        
        # Get screen dimensions
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.splash.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_splash(self):
        """Setup the splash screen layout"""
        # Main frame with gradient-like background
        main_frame = tk.Frame(self.splash, bg="#2c3e50", bd=2, relief="raised")
        main_frame.pack(fill="both", expand=True)
        
        # Title section
        title_frame = tk.Frame(main_frame, bg="#2c3e50")
        title_frame.pack(pady=30)
        
        # App name
        title_label = tk.Label(title_frame, text="FilePulse", 
                              font=("Arial", 24, "bold"), 
                              fg="#ecf0f1", bg="#2c3e50")
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(title_frame, text="Filesystem Monitor", 
                                 font=("Arial", 12), 
                                 fg="#bdc3c7", bg="#2c3e50")
        subtitle_label.pack(pady=(5, 0))
        
        # Icon/Logo area (using text for now)
        icon_frame = tk.Frame(main_frame, bg="#2c3e50")
        icon_frame.pack(pady=20)
        
        # Create a simple icon using text
        icon_label = tk.Label(icon_frame, text="📁", 
                             font=("Arial", 48), 
                             fg="#3498db", bg="#2c3e50")
        icon_label.pack()
        
        # Progress section
        progress_frame = tk.Frame(main_frame, bg="#2c3e50")
        progress_frame.pack(pady=20, padx=40, fill="x")
        
        # Loading label
        self.loading_label = tk.Label(progress_frame, text="Loading...", 
                                     font=("Arial", 10), 
                                     fg="#95a5a6", bg="#2c3e50")
        self.loading_label.pack()
        
        # Progress bar
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate', 
                                       length=300, style="Custom.Horizontal.TProgressbar")
        self.progress.pack(pady=(10, 0))
        
        # Version info
        version_frame = tk.Frame(main_frame, bg="#2c3e50")
        version_frame.pack(side="bottom", pady=10)
        
        version_label = tk.Label(version_frame, text="Version 0.1.0", 
                                font=("Arial", 8), 
                                fg="#7f8c8d", bg="#2c3e50")
        version_label.pack()
        
        # Copyright
        copyright_label = tk.Label(version_frame, text="© 2025 FilePulse Project", 
                                  font=("Arial", 8), 
                                  fg="#7f8c8d", bg="#2c3e50")
        copyright_label.pack()
        
        # Configure progress bar style
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Custom.Horizontal.TProgressbar", 
                       background='#3498db',
                       troughcolor='#34495e',
                       borderwidth=0,
                       lightcolor='#3498db',
                       darkcolor='#3498db')
    
    def animate_loading(self):
        """Animate the loading process"""
        self.progress.start(10)  # Start the progress bar animation
        
        # Loading messages
        messages = [
            "Initializing FilePulse...",
            "Loading configuration...",
            "Setting up monitors...",
            "Preparing interface...",
            "Almost ready..."
        ]
        
        def update_message():
            for i, message in enumerate(messages):
                if hasattr(self, 'loading_label'):
                    self.loading_label.config(text=message)
                    self.splash.update()
                time.sleep(0.8)  # Show each message for 0.8 seconds
        
        # Run the message updates in a separate thread
        threading.Thread(target=update_message, daemon=True).start()
    
    def close_splash(self):
        """Close the splash screen"""
        try:
            self.progress.stop()
            self.splash.destroy()
        except:
            pass  # Ignore errors if already closed
    
    def show(self, duration=4.0):
        """Show splash screen for specified duration"""
        self.splash.lift()
        self.splash.focus_force()
        
        # Auto-close after duration
        def auto_close():
            time.sleep(duration)
            self.close_splash()
        
        threading.Thread(target=auto_close, daemon=True).start()
        
        return self.splash


def show_splash_screen(duration=4.0):
    """Convenience function to show splash screen"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    splash = FilePulseSplash()
    splash_window = splash.show(duration)
    
    return splash, root


if __name__ == "__main__":
    # Test the splash screen
    splash, root = show_splash_screen(5.0)
    root.mainloop()
