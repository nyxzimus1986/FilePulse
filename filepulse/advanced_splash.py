#!/usr/bin/env python3
"""
Advanced FilePulse Splash Screen with custom graphics
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import math

class AdvancedFilePulseSplash:
    def __init__(self):
        self.splash = tk.Toplevel()
        self.splash.title("FilePulse")
        self.splash.geometry("500x350")
        self.splash.resizable(False, False)
        
        # Center the splash screen
        self.center_window()
        
        # Remove window decorations for a clean look
        self.splash.overrideredirect(True)
        
        # Make it always on top
        self.splash.attributes('-topmost', True)
        
        # Configure the splash screen
        self.setup_splash()
        
        # Animation variables
        self.animation_step = 0
        self.is_animating = True
        
        # Start the loading animation
        self.animate_loading()
    
    def center_window(self):
        """Center the splash screen on the screen"""
        self.splash.update_idletasks()
        width = 500
        height = 350
        
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
        main_frame = tk.Frame(self.splash, bg="#1a252f", bd=0)
        main_frame.pack(fill="both", expand=True)
        
        # Header with gradient effect
        header_frame = tk.Frame(main_frame, bg="#2c3e50", height=80)
        header_frame.pack(fill="x", pady=0)
        header_frame.pack_propagate(False)
        
        # Title section
        title_frame = tk.Frame(header_frame, bg="#2c3e50")
        title_frame.pack(expand=True)
        
        # App name with shadow effect
        shadow_label = tk.Label(title_frame, text="FilePulse", 
                               font=("Arial", 28, "bold"), 
                               fg="#1a252f", bg="#2c3e50")
        shadow_label.place(x=152, y=22)  # Shadow offset
        
        title_label = tk.Label(title_frame, text="FilePulse", 
                              font=("Arial", 28, "bold"), 
                              fg="#3498db", bg="#2c3e50")
        title_label.place(x=150, y=20)
        
        # Main content area
        content_frame = tk.Frame(main_frame, bg="#1a252f")
        content_frame.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Create canvas for custom graphics
        self.canvas = tk.Canvas(content_frame, width=400, height=120, 
                               bg="#1a252f", highlightthickness=0)
        self.canvas.pack(pady=20)
        
        # Draw custom logo/icon
        self.draw_custom_logo()
        
        # Subtitle
        subtitle_label = tk.Label(content_frame, text="Advanced Filesystem Monitoring", 
                                 font=("Arial", 12, "italic"), 
                                 fg="#bdc3c7", bg="#1a252f")
        subtitle_label.pack(pady=(10, 20))
        
        # Features list
        features_frame = tk.Frame(content_frame, bg="#1a252f")
        features_frame.pack(pady=10)
        
        features = ["🚀 Real-time monitoring", "🎯 Intelligent filtering", "📊 Resource optimization"]
        for feature in features:
            feature_label = tk.Label(features_frame, text=feature, 
                                   font=("Arial", 9), 
                                   fg="#95a5a6", bg="#1a252f")
            feature_label.pack(anchor="w")
        
        # Progress section
        progress_frame = tk.Frame(content_frame, bg="#1a252f")
        progress_frame.pack(pady=20, fill="x")
        
        # Loading label
        self.loading_label = tk.Label(progress_frame, text="Initializing...", 
                                     font=("Arial", 10, "bold"), 
                                     fg="#3498db", bg="#1a252f")
        self.loading_label.pack()
        
        # Custom progress bar
        self.progress_canvas = tk.Canvas(progress_frame, width=300, height=20, 
                                        bg="#1a252f", highlightthickness=0)
        self.progress_canvas.pack(pady=(10, 0))
        
        # Draw progress bar background
        self.progress_canvas.create_rectangle(0, 8, 300, 12, fill="#34495e", outline="")
        
        # Footer
        footer_frame = tk.Frame(main_frame, bg="#2c3e50", height=40)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)
        
        footer_content = tk.Frame(footer_frame, bg="#2c3e50")
        footer_content.pack(expand=True)
        
        version_label = tk.Label(footer_content, text="Version 0.1.0  •  © 2025 FilePulse Project", 
                                font=("Arial", 8), 
                                fg="#7f8c8d", bg="#2c3e50")
        version_label.pack(pady=12)
    
    def draw_custom_logo(self):
        """Draw a custom logo on the canvas"""
        # Draw folder icon with pulse effect
        center_x, center_y = 200, 60
        
        # Folder base
        self.canvas.create_rectangle(center_x-30, center_y-10, center_x+30, center_y+20, 
                                   fill="#3498db", outline="#2980b9", width=2)
        
        # Folder tab
        self.canvas.create_rectangle(center_x-30, center_y-15, center_x-10, center_y-5, 
                                   fill="#3498db", outline="#2980b9", width=2)
        
        # Pulse circles (will be animated)
        self.pulse_circles = []
        for i in range(3):
            circle = self.canvas.create_oval(center_x-5, center_y-5, center_x+5, center_y+5,
                                           outline="#e74c3c", width=2, state="hidden")
            self.pulse_circles.append(circle)
        
        # Monitor wave lines
        for i, y_offset in enumerate([-5, 0, 5]):
            self.canvas.create_line(center_x+40, center_y+y_offset, center_x+80, center_y+y_offset,
                                  fill="#2ecc71", width=2)
    
    def animate_loading(self):
        """Animate the loading process"""        
        # Loading messages
        messages = [
            "Initializing FilePulse...",
            "Loading configuration...",
            "Setting up filesystem monitors...",
            "Preparing user interface...",
            "Optimizing performance...",
            "Ready to monitor!"
        ]
        
        def update_animation():
            message_index = 0
            progress = 0
            
            while self.is_animating and message_index < len(messages):
                try:
                    # Update message
                    if hasattr(self, 'loading_label'):
                        self.loading_label.config(text=messages[message_index])
                    
                    # Update progress bar
                    progress = min(progress + 50, 300)
                    if hasattr(self, 'progress_canvas'):
                        self.progress_canvas.delete("progress")
                        self.progress_canvas.create_rectangle(0, 8, progress, 12, 
                                                            fill="#3498db", outline="", tags="progress")
                    
                    # Animate pulse circles
                    self.animate_pulse()
                    
                    # Update display
                    if hasattr(self, 'splash'):
                        self.splash.update()
                    
                    time.sleep(0.5)
                    message_index += 1
                    
                except:
                    break
        
        # Run the animation in a separate thread
        threading.Thread(target=update_animation, daemon=True).start()
    
    def animate_pulse(self):
        """Animate the pulse effect on the logo"""
        try:
            for i, circle in enumerate(self.pulse_circles):
                # Show/hide circles in sequence
                delay = i * 5
                if (self.animation_step + delay) % 30 < 10:
                    self.canvas.itemconfig(circle, state="normal")
                    
                    # Scale the circle
                    scale = 1 + (self.animation_step % 10) * 0.3
                    center_x, center_y = 200, 60
                    radius = 5 + i * 8
                    self.canvas.coords(circle, 
                                     center_x - radius * scale, center_y - radius * scale,
                                     center_x + radius * scale, center_y + radius * scale)
                else:
                    self.canvas.itemconfig(circle, state="hidden")
            
            self.animation_step += 1
        except:
            pass
    
    def close_splash(self):
        """Close the splash screen"""
        try:
            self.is_animating = False
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


if __name__ == "__main__":
    # Test the advanced splash screen
    root = tk.Tk()
    root.withdraw()
    
    splash = AdvancedFilePulseSplash()
    splash.show(6.0)
    
    root.mainloop()
