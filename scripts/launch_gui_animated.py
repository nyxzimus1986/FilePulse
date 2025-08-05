#!/usr/bin/env python3
"""
FilePulse GUI Launcher with Animated Custom Progress Bar
Alternative version with guaranteed animated progress bar
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
import sys
import os
from pathlib import Path
import math

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class AnimatedProgressBar:
    """Custom animated progress bar widget"""
    def __init__(self, parent, width=300, height=20, bg_color="#34495e", fg_color="#3498db"):
        self.canvas = tk.Canvas(parent, width=width, height=height, 
                               bg=bg_color, highlightthickness=0)
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.fg_color = fg_color
        
        # Animation state
        self.is_running = False
        self.position = 0
        self.direction = 1
        self.bar_width = 80
        
    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)
    
    def start(self):
        """Start the animation"""
        self.is_running = True
        self.animate()
    
    def stop(self):
        """Stop the animation"""
        self.is_running = False
    
    def animate(self):
        """Animate the progress bar"""
        if not self.is_running:
            return
        
        # Clear canvas
        self.canvas.delete("all")
        
        # Calculate animated bar position
        self.position += self.direction * 3
        
        # Bounce effect
        if self.position >= self.width - self.bar_width:
            self.direction = -1
        elif self.position <= 0:
            self.direction = 1
        
        # Draw background
        self.canvas.create_rectangle(0, 0, self.width, self.height, 
                                   fill=self.bg_color, outline="")
        
        # Draw animated bar with gradient effect
        bar_x1 = self.position
        bar_x2 = self.position + self.bar_width
        
        # Create gradient effect with multiple rectangles
        for i in range(self.bar_width):
            alpha = 1.0 - (abs(i - self.bar_width/2) / (self.bar_width/2)) * 0.5
            color_intensity = int(255 * alpha)
            
            # Calculate color
            r, g, b = 52, 152, 219  # #3498db in RGB
            gradient_color = f"#{r:02x}{g:02x}{b:02x}"
            
            x = bar_x1 + i
            if 0 <= x < self.width:
                self.canvas.create_rectangle(x, 2, x+1, self.height-2, 
                                           fill=gradient_color, outline="")
        
        # Schedule next frame
        if self.is_running:
            self.canvas.after(16, self.animate)  # ~60 FPS

class CustomSplashScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window initially
        
        # Create splash window
        self.splash = tk.Toplevel()
        self.splash.title("FilePulse")
        self.splash.resizable(False, False)
        self.splash.overrideredirect(True)  # Remove window decorations
        
        # Try to load custom splash screen
        self.splash_image = None
        self.load_custom_splash()
        
        # Setup splash based on whether image was loaded
        if self.splash_image:
            self.setup_image_splash()
        else:
            self.setup_default_splash()
        
        # Center the splash
        self.center_splash()
        
        # Start loading sequence
        self.start_loading()
    
    def load_custom_splash(self):
        """Load custom splash screen image from assets/splash/"""
        splash_paths = [
            "assets/splash/Splash.png",
            "assets/splash/Splash-theme.png", 
            "assets/splash/splash.png",
            "assets/splash/splash-theme.png"
        ]
        
        for splash_path in splash_paths:
            if Path(splash_path).exists():
                try:
                    # Load and resize the splash image
                    img = Image.open(splash_path)
                    
                    # Resize to reasonable splash size while maintaining aspect ratio
                    max_width, max_height = 600, 400
                    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                    
                    self.splash_image = ImageTk.PhotoImage(img)
                    self.splash_width = img.width
                    self.splash_height = img.height
                    
                    print(f"✓ Loaded custom splash: {splash_path} ({img.width}x{img.height})")
                    return
                    
                except Exception as e:
                    print(f"✗ Failed to load {splash_path}: {e}")
                    continue
        
        print("ℹ No custom splash found, using default")
    
    def setup_image_splash(self):
        """Setup splash with custom image"""
        # Add padding for progress overlay
        total_height = self.splash_height + 80
        self.splash.geometry(f"{self.splash_width}x{total_height}")
        
        # Main frame
        main_frame = tk.Frame(self.splash, bg="#000000")
        main_frame.pack(fill="both", expand=True)
        
        # Image label
        image_label = tk.Label(main_frame, image=self.splash_image, bd=0)
        image_label.pack()
        
        # Overlay frame for progress
        overlay_frame = tk.Frame(main_frame, bg="#2c3e50", height=80)
        overlay_frame.pack(side="bottom", fill="x")
        overlay_frame.pack_propagate(False)
        
        # Loading label
        self.loading_label = tk.Label(overlay_frame, text="Loading FilePulse...", 
                                     font=("Arial", 11, "bold"), 
                                     fg="#ecf0f1", bg="#2c3e50")
        self.loading_label.pack(pady=(10, 5))
        
        # Custom animated progress bar
        self.progress = AnimatedProgressBar(overlay_frame, width=350, height=16)
        self.progress.pack(pady=(5, 15))
    
    def setup_default_splash(self):
        """Setup default splash if no custom image found"""
        self.splash.geometry("520x380")
        
        # Main frame with gradient-like background
        main_frame = tk.Frame(self.splash, bg="#2c3e50", bd=2, relief="raised")
        main_frame.pack(fill="both", expand=True)
        
        # Title section
        title_frame = tk.Frame(main_frame, bg="#2c3e50")
        title_frame.pack(pady=40)
        
        # App name with pulse effect
        self.title_label = tk.Label(title_frame, text="FilePulse", 
                                   font=("Arial", 32, "bold"), 
                                   fg="#ecf0f1", bg="#2c3e50")
        self.title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(title_frame, text="Real-time Filesystem Monitor", 
                                 font=("Arial", 13), 
                                 fg="#bdc3c7", bg="#2c3e50")
        subtitle_label.pack(pady=(10, 0))
        
        # Icon area with pulse animation
        icon_frame = tk.Frame(main_frame, bg="#2c3e50")
        icon_frame.pack(pady=25)
        
        self.icon_label = tk.Label(icon_frame, text="📁", 
                                  font=("Arial", 56), 
                                  fg="#3498db", bg="#2c3e50")
        self.icon_label.pack()
        
        # Progress section
        progress_frame = tk.Frame(main_frame, bg="#2c3e50")
        progress_frame.pack(pady=25, padx=50, fill="x")
        
        # Loading label
        self.loading_label = tk.Label(progress_frame, text="Initializing...", 
                                     font=("Arial", 11), 
                                     fg="#95a5a6", bg="#2c3e50")
        self.loading_label.pack()
        
        # Custom animated progress bar
        self.progress = AnimatedProgressBar(progress_frame, width=380, height=18)
        self.progress.pack(pady=(15, 0))
        
        # Version info
        version_frame = tk.Frame(main_frame, bg="#2c3e50")
        version_frame.pack(side="bottom", pady=15)
        
        version_label = tk.Label(version_frame, text="v0.1.0 - Enhanced Animation", 
                                font=("Arial", 9), 
                                fg="#7f8c8d", bg="#2c3e50")
        version_label.pack()
        
        # Start title pulse animation
        self.start_title_pulse()
    
    def start_title_pulse(self):
        """Animate the title with a subtle pulse effect"""
        def pulse_title():
            colors = ["#ecf0f1", "#3498db", "#ecf0f1"]
            for color in colors:
                if hasattr(self, 'title_label'):
                    self.title_label.config(fg=color)
                    self.splash.update()
                    time.sleep(0.3)
        
        def pulse_loop():
            while hasattr(self, 'splash') and self.splash.winfo_exists():
                try:
                    pulse_title()
                    time.sleep(2)  # Pause between pulses
                except:
                    break
        
        pulse_thread = threading.Thread(target=pulse_loop, daemon=True)
        pulse_thread.start()
    
    def center_splash(self):
        """Center splash on screen"""
        self.splash.update_idletasks()
        width = self.splash.winfo_width()
        height = self.splash.winfo_height()
        
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.splash.geometry(f"{width}x{height}+{x}+{y}")
    
    def start_loading(self):
        """Start the loading animation and sequence"""
        # Start custom progress bar animation
        self.progress.start()
        
        # Make sure splash is visible
        self.splash.update()
        self.splash.lift()
        self.splash.focus_force()
        
        # Loading sequence
        def loading_sequence():
            loading_steps = [
                ("🔧 Initializing FilePulse...", 0.8),
                ("📋 Loading configuration...", 0.7),
                ("👀 Setting up file monitoring...", 0.8),
                ("🖥️ Preparing user interface...", 0.7),
                ("🚀 Starting filesystem watchers...", 0.9),
                ("✨ Finalizing startup...", 0.6),
                ("🎉 Ready to monitor!", 0.4)
            ]
            
            for step_text, delay in loading_steps:
                # Update loading text
                self.loading_label.config(text=step_text)
                self.splash.update()
                
                # Wait with animation updates
                elapsed = 0
                interval = 0.05
                while elapsed < delay:
                    time.sleep(interval)
                    elapsed += interval
            
            # Stop animation and close
            self.progress.stop()
            time.sleep(0.4)
            self.close_splash()
        
        # Start loading thread
        loading_thread = threading.Thread(target=loading_sequence, daemon=True)
        loading_thread.start()
    
    def close_splash(self):
        """Close splash and launch main GUI"""
        try:
            self.splash.destroy()
        except:
            pass
        
        # Launch the main FilePulse GUI
        self.launch_main_gui()
    
    def launch_main_gui(self):
        """Launch the main FilePulse GUI application"""
        try:
            # Import and launch the main GUI
            from filepulse.gui import main as gui_main
            
            # Show the main window
            self.root.deiconify()
            self.root.withdraw()  # Hide it again, let GUI create its own
            
            # Launch GUI
            gui_main()
            
        except Exception as e:
            print(f"Error launching GUI: {e}")
            # Show error dialog
            import tkinter.messagebox as msgbox
            msgbox.showerror("Launch Error", 
                           f"Failed to launch FilePulse GUI:\n{str(e)}\n\n"
                           f"Try running: python launch_gui.py")
    
    def run(self):
        """Run the splash screen"""
        self.root.mainloop()

def main():
    """Main entry point"""
    print("🚀 Starting FilePulse with Animated Custom Splash Screen...")
    
    # Check if we're in the right directory
    if not Path("filepulse").exists():
        print("❌ Error: Please run this from the FilePulse project directory")
        print("   Expected structure: FilePulse/filepulse/")
        return 1
    
    # Create and run splash
    splash = CustomSplashScreen()
    splash.run()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
