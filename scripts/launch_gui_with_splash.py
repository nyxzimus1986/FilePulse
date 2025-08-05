#!/usr/bin/env python3
"""
FilePulse GUI Launcher with Custom Splash Screen
Launches the FilePulse GUI with your custom splash screen from assets/splash/
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class CustomSplashScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window initially
        
        # Create splash window
        self.splash = tk.Toplevel()
        self.splash.title("FilePulse")
        self.splash.resizable(False, False)
        self.splash.overrideredirect(True)  # Remove window decorations
        
        # Configure progress bar style for better animation
        self.setup_styles()
        
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
    
    def setup_styles(self):
        """Setup custom styles for progress bar animation"""
        self.style = ttk.Style()
        
        # Configure progress bar for better animation
        self.style.theme_use('clam')  # Use a theme that supports better animation
        
        # Custom progress bar style
        self.style.configure("Animated.Horizontal.TProgressbar",
                           troughcolor='#34495e',
                           background='#3498db',
                           borderwidth=1,
                           lightcolor='#5dade2',
                           darkcolor='#2980b9')
        
        # Configure animation parameters
        self.style.configure("Animated.Horizontal.TProgressbar",
                           troughcolor='#34495e',
                           background='#3498db',
                           thickness=8)
    
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
        self.splash.geometry(f"{self.splash_width}x{self.splash_height}")
        
        # Main frame
        main_frame = tk.Frame(self.splash, bg="#000000")
        main_frame.pack(fill="both", expand=True)
        
        # Image label
        image_label = tk.Label(main_frame, image=self.splash_image, bd=0)
        image_label.pack()
        
        # Overlay frame for progress (semi-transparent effect)
        overlay_frame = tk.Frame(main_frame, bg="#2c3e50", height=60)
        overlay_frame.pack(side="bottom", fill="x")
        overlay_frame.pack_propagate(False)
        
        # Loading label
        self.loading_label = tk.Label(overlay_frame, text="Loading FilePulse...", 
                                     font=("Arial", 10, "bold"), 
                                     fg="#ecf0f1", bg="#2c3e50")
        self.loading_label.pack(pady=5)
        
        # Progress bar with custom style
        self.progress = ttk.Progressbar(overlay_frame, mode='indeterminate', 
                                       length=300, 
                                       style="Animated.Horizontal.TProgressbar")
        self.progress.pack(pady=8)
    
    def setup_default_splash(self):
        """Setup default splash if no custom image found"""
        self.splash.geometry("500x350")
        
        # Main frame with gradient-like background
        main_frame = tk.Frame(self.splash, bg="#2c3e50", bd=2, relief="raised")
        main_frame.pack(fill="both", expand=True)
        
        # Title section
        title_frame = tk.Frame(main_frame, bg="#2c3e50")
        title_frame.pack(pady=40)
        
        # App name
        title_label = tk.Label(title_frame, text="FilePulse", 
                              font=("Arial", 28, "bold"), 
                              fg="#ecf0f1", bg="#2c3e50")
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(title_frame, text="Real-time Filesystem Monitor", 
                                 font=("Arial", 12), 
                                 fg="#bdc3c7", bg="#2c3e50")
        subtitle_label.pack(pady=(8, 0))
        
        # Icon area
        icon_frame = tk.Frame(main_frame, bg="#2c3e50")
        icon_frame.pack(pady=30)
        
        # Animated pulse icon
        self.icon_label = tk.Label(icon_frame, text="📁", 
                                  font=("Arial", 64), 
                                  fg="#3498db", bg="#2c3e50")
        self.icon_label.pack()
        
        # Progress section
        progress_frame = tk.Frame(main_frame, bg="#2c3e50")
        progress_frame.pack(pady=30, padx=50, fill="x")
        
        # Loading label
        self.loading_label = tk.Label(progress_frame, text="Loading components...", 
                                     font=("Arial", 11), 
                                     fg="#95a5a6", bg="#2c3e50")
        self.loading_label.pack()
        
        # Progress bar with custom style
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate', 
                                       length=350,
                                       style="Animated.Horizontal.TProgressbar")
        self.progress.pack(pady=(15, 0))
        
        # Version info
        version_frame = tk.Frame(main_frame, bg="#2c3e50")
        version_frame.pack(side="bottom", pady=15)
        
        version_label = tk.Label(version_frame, text="v0.1.0 - With Custom Image Support", 
                                font=("Arial", 9), 
                                fg="#7f8c8d", bg="#2c3e50")
        version_label.pack()
    
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
        # Start progress bar animation with faster speed for better visibility
        self.progress.start(5)  # Faster animation speed (lower = faster)
        
        # Make sure splash is visible and updated
        self.splash.update()
        self.splash.lift()  # Bring to front
        
        # Loading sequence in separate thread
        def loading_sequence():
            loading_steps = [
                ("Initializing FilePulse...", 0.8),
                ("Loading configuration...", 0.6),
                ("Setting up file monitoring...", 0.7),
                ("Preparing user interface...", 0.6),
                ("Starting filesystem watchers...", 0.8),
                ("Finalizing startup...", 0.4),
                ("Ready!", 0.3)
            ]
            
            for step_text, delay in loading_steps:
                # Update on main thread
                self.splash.after(0, lambda text=step_text: self.loading_label.config(text=text))
                
                # Force update
                self.splash.after(0, self.splash.update)
                
                # Wait with small intervals to keep animation smooth
                elapsed = 0
                interval = 0.05  # 50ms intervals
                while elapsed < delay:
                    time.sleep(interval)
                    elapsed += interval
                    # Periodic updates to keep animation smooth
                    if elapsed % 0.2 < interval:  # Every 200ms
                        self.splash.after(0, self.splash.update)
            
            # Stop progress and close splash
            self.splash.after(0, self.progress.stop)
            self.splash.after(0, self.splash.update)
            time.sleep(0.3)
            self.splash.after(0, self.close_splash)
        
        # Start loading in background thread
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
    print("🚀 Starting FilePulse with Custom Splash Screen...")
    
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
