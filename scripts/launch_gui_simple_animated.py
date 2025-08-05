#!/usr/bin/env python3
"""
FilePulse GUI Launcher with Simple Animated Splash
Uses a simple, reliable animation approach that always works
"""

import tkinter as tk
from PIL import Image, ImageTk
import time
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class SimpleSplashScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide main window
        
        # Create splash window
        self.splash = tk.Toplevel()
        self.splash.title("FilePulse")
        self.splash.resizable(False, False)
        self.splash.overrideredirect(True)
        
        # Animation variables
        self.progress_value = 0
        self.loading_dots = ""
        self.animation_running = True
        
        # Load custom splash or create default
        self.splash_image = None
        self.load_custom_splash()
        
        if self.splash_image:
            self.setup_image_splash()
        else:
            self.setup_default_splash()
        
        # Center and show
        self.center_splash()
        self.splash.lift()
        self.splash.focus_force()
        
        # Start the loading sequence
        self.start_loading_sequence()
    
    def load_custom_splash(self):
        """Load custom splash screen image"""
        splash_paths = [
            "assets/splash/Splash.png",
            "assets/splash/Splash-theme.png"
        ]
        
        for splash_path in splash_paths:
            if Path(splash_path).exists():
                try:
                    img = Image.open(splash_path)
                    # Resize to max 600x400 while maintaining aspect ratio
                    img.thumbnail((600, 400), Image.Resampling.LANCZOS)
                    self.splash_image = ImageTk.PhotoImage(img)
                    self.splash_width = img.width
                    self.splash_height = img.height
                    print(f"✓ Loaded: {splash_path} ({img.width}x{img.height})")
                    return
                except Exception as e:
                    print(f"✗ Failed to load {splash_path}: {e}")
    
    def setup_image_splash(self):
        """Setup splash with custom image"""
        total_height = self.splash_height + 100
        self.splash.geometry(f"{self.splash_width}x{total_height}")
        
        # Main container
        main_frame = tk.Frame(self.splash, bg="#000000")
        main_frame.pack(fill="both", expand=True)
        
        # Custom image
        image_label = tk.Label(main_frame, image=self.splash_image, bd=0)
        image_label.pack()
        
        # Progress overlay
        progress_frame = tk.Frame(main_frame, bg="#2c3e50", height=100)
        progress_frame.pack(side="bottom", fill="x")
        progress_frame.pack_propagate(False)
        
        # Loading text
        self.loading_label = tk.Label(progress_frame, text="Loading FilePulse", 
                                     font=("Arial", 12, "bold"), 
                                     fg="#ecf0f1", bg="#2c3e50")
        self.loading_label.pack(pady=(15, 8))
        
        # Progress bar container
        bar_frame = tk.Frame(progress_frame, bg="#34495e", height=20, width=400)
        bar_frame.pack(pady=(0, 15))
        bar_frame.pack_propagate(False)
        
        # Animated progress bar
        self.progress_canvas = tk.Canvas(bar_frame, width=400, height=20, 
                                        bg="#34495e", highlightthickness=0)
        self.progress_canvas.pack()
    
    def setup_default_splash(self):
        """Setup default splash"""
        self.splash.geometry("500x350")
        
        main_frame = tk.Frame(self.splash, bg="#2c3e50")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_frame = tk.Frame(main_frame, bg="#2c3e50")
        title_frame.pack(pady=50)
        
        tk.Label(title_frame, text="FilePulse", 
                font=("Arial", 32, "bold"), 
                fg="#ecf0f1", bg="#2c3e50").pack()
        
        tk.Label(title_frame, text="Real-time Filesystem Monitor", 
                font=("Arial", 12), 
                fg="#bdc3c7", bg="#2c3e50").pack(pady=10)
        
        # Icon
        tk.Label(title_frame, text="📁", 
                font=("Arial", 48), 
                fg="#3498db", bg="#2c3e50").pack(pady=20)
        
        # Loading section
        loading_frame = tk.Frame(main_frame, bg="#2c3e50")
        loading_frame.pack(pady=30)
        
        self.loading_label = tk.Label(loading_frame, text="Loading", 
                                     font=("Arial", 11), 
                                     fg="#95a5a6", bg="#2c3e50")
        self.loading_label.pack()
        
        # Progress bar
        bar_frame = tk.Frame(loading_frame, bg="#34495e", height=20, width=350)
        bar_frame.pack(pady=15)
        bar_frame.pack_propagate(False)
        
        self.progress_canvas = tk.Canvas(bar_frame, width=350, height=20, 
                                        bg="#34495e", highlightthickness=0)
        self.progress_canvas.pack()
    
    def center_splash(self):
        """Center splash on screen"""
        self.splash.update_idletasks()
        width = self.splash.winfo_width()
        height = self.splash.winfo_height()
        
        x = (self.splash.winfo_screenwidth() - width) // 2
        y = (self.splash.winfo_screenheight() - height) // 2
        
        self.splash.geometry(f"{width}x{height}+{x}+{y}")
    
    def animate_progress(self):
        """Animate the progress bar - this runs continuously"""
        if not self.animation_running:
            return
        
        # Clear canvas
        self.progress_canvas.delete("all")
        
        # Calculate moving bar position
        bar_width = 80
        canvas_width = int(self.progress_canvas['width'])
        
        # Create a smooth back-and-forth motion
        cycle_time = 2.0  # 2 seconds for full cycle
        current_time = time.time() % cycle_time
        progress = current_time / cycle_time
        
        # Smooth sine wave motion
        import math
        position = (math.sin(progress * 2 * math.pi) + 1) / 2  # 0 to 1
        bar_x = int(position * (canvas_width - bar_width))
        
        # Draw the animated bar with gradient effect
        for i in range(bar_width):
            # Create gradient effect
            alpha = 1.0 - abs(i - bar_width/2) / (bar_width/2) * 0.6
            
            # Blue gradient
            blue_intensity = int(52 + (152-52) * alpha)  # From dark to light blue
            color = f"#{blue_intensity:02x}{int(152*alpha):02x}{int(219*alpha):02x}"
            
            x = bar_x + i
            if 0 <= x < canvas_width:
                self.progress_canvas.create_rectangle(
                    x, 2, x+1, 18, 
                    fill=color, outline=""
                )
        
        # Schedule next animation frame (smooth 60fps)
        self.splash.after(16, self.animate_progress)
    
    def animate_loading_text(self):
        """Animate the loading text with dots"""
        if not self.animation_running:
            return
        
        # Cycle through loading dots
        dots_cycle = ["", ".", "..", "..."]
        self.loading_dots = dots_cycle[(int(time.time() * 2) % len(dots_cycle))]
        
        # Update text
        base_text = "Loading FilePulse" if hasattr(self, 'splash_image') and self.splash_image else "Loading"
        self.loading_label.config(text=f"{base_text}{self.loading_dots}")
        
        # Schedule next update
        self.splash.after(500, self.animate_loading_text)  # Update every 500ms
    
    def start_loading_sequence(self):
        """Start all animations and loading sequence"""
        # Start animations
        self.animate_progress()
        self.animate_loading_text()
        
        # Start loading sequence
        def loading_steps():
            steps = [
                "Initializing components...",
                "Loading configuration...", 
                "Setting up monitoring...",
                "Preparing interface...",
                "Starting watchers...",
                "Finalizing setup...",
                "Ready!"
            ]
            
            for i, step in enumerate(steps):
                # Update loading text
                self.loading_label.config(text=step)
                self.splash.update()
                
                # Wait between steps
                delay = 0.8 if i < len(steps)-1 else 0.4
                start_time = time.time()
                while time.time() - start_time < delay:
                    self.splash.update()
                    time.sleep(0.02)  # Small sleep to prevent high CPU
            
            # Stop animations and close
            self.animation_running = False
            self.splash.after(300, self.close_splash)
        
        # Start loading sequence after a short delay
        self.splash.after(100, loading_steps)
    
    def close_splash(self):
        """Close splash and launch main GUI"""
        try:
            self.splash.destroy()
        except:
            pass
        
        # Launch main GUI
        try:
            from filepulse.gui import main as gui_main
            self.root.deiconify()
            self.root.withdraw()
            gui_main()
        except Exception as e:
            print(f"Error launching GUI: {e}")
            import tkinter.messagebox as msgbox
            msgbox.showerror("Launch Error", f"Failed to launch FilePulse GUI:\n{str(e)}")
    
    def run(self):
        """Run the splash screen"""
        self.root.mainloop()

def main():
    print("🚀 FilePulse - Simple Animated Splash Screen")
    
    if not Path("filepulse").exists():
        print("❌ Please run from FilePulse project directory")
        return 1
    
    splash = SimpleSplashScreen()
    splash.run()
    return 0

if __name__ == "__main__":
    sys.exit(main())
