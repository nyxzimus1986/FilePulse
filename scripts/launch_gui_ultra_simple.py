#!/usr/bin/env python3
"""
FilePulse - Ultra Simple Animated Splash (Guaranteed to work!)
"""

import tkinter as tk
from PIL import Image, ImageTk
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

class UltraSimpleSplash:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        
        self.splash = tk.Toplevel()
        self.splash.title("FilePulse")
        self.splash.overrideredirect(True)
        
        # Animation state
        self.bar_pos = 0
        self.bar_direction = 5
        self.step = 0
        
        # Load custom image
        self.load_image()
        self.setup_ui()
        self.center()
        
        # Start animation immediately
        self.animate()
    
    def load_image(self):
        """Load custom splash image"""
        self.splash_image = None
        for path in ["assets/splash/Splash.png", "assets/splash/Splash-theme.png"]:
            if Path(path).exists():
                try:
                    img = Image.open(path)
                    img.thumbnail((500, 350), Image.Resampling.LANCZOS)
                    self.splash_image = ImageTk.PhotoImage(img)
                    self.img_width, self.img_height = img.size
                    print(f"✓ Loaded: {path}")
                    break
                except:
                    pass
    
    def setup_ui(self):
        """Setup the UI with transparent bottom"""
        if self.splash_image:
            # Custom image version with transparent bottom
            self.splash.geometry(f"{self.img_width}x{self.img_height + 80}")
            self.splash.configure(bg="")  # Transparent background
            self.splash.attributes("-transparentcolor", "magenta")  # Set transparent color
            
            # Image
            tk.Label(self.splash, image=self.splash_image, bd=0).pack()
            
            # Transparent progress area
            progress_frame = tk.Frame(self.splash, bg="magenta", height=80)  # Use transparent color
            progress_frame.pack(fill="x")
            progress_frame.pack_propagate(False)
            
            # Semi-transparent overlay for text readability
            overlay_frame = tk.Frame(progress_frame, bg="#2c3e50", height=40)
            overlay_frame.pack(fill="x", pady=5)
            overlay_frame.pack_propagate(False)
            
            self.status_label = tk.Label(overlay_frame, text="Loading...", 
                                        fg="white", bg="#2c3e50", font=("Arial", 10))
            self.status_label.pack(pady=8)
            
        else:
            # Default version with gradient transparency effect
            self.splash.geometry("400x300")
            self.splash.configure(bg="#2c3e50")
            
            main = tk.Frame(self.splash, bg="#2c3e50")
            main.pack(fill="both", expand=True)
            
            tk.Label(main, text="FilePulse", fg="white", bg="#2c3e50", 
                    font=("Arial", 24, "bold")).pack(pady=30)
            tk.Label(main, text="📁", fg="#3498db", bg="#2c3e50", 
                    font=("Arial", 40)).pack(pady=20)
            
            # Fade to transparent bottom
            fade_frame = tk.Frame(main, bg="#2c3e50")
            fade_frame.pack(fill="x", pady=10)
            
            self.status_label = tk.Label(fade_frame, text="Loading...", 
                                        fg="#bdc3c7", bg="#2c3e50", font=("Arial", 10))
            self.status_label.pack(pady=10)
        
        # Transparent progress bar area
        bar_container = tk.Frame(self.splash, bg="magenta", height=40)  # Transparent
        bar_container.pack(fill="x", padx=40)
        bar_container.pack_propagate(False)
        
        # Semi-transparent bar background
        bar_bg = tk.Frame(bar_container, bg="#34495e", height=16, relief="flat", bd=1)
        bar_bg.pack(expand=True, fill="x", pady=12)
        
        self.progress_canvas = tk.Canvas(bar_bg, height=16, bg="#34495e", 
                                        highlightthickness=0, relief="flat")
        self.progress_canvas.pack(fill="x")
    
    def center(self):
        self.splash.update_idletasks()
        w, h = self.splash.winfo_width(), self.splash.winfo_height()
        x = (self.splash.winfo_screenwidth() - w) // 2
        y = (self.splash.winfo_screenheight() - h) // 2
        self.splash.geometry(f"{w}x{h}+{x}+{y}")
    
    def animate(self):
        """Simple animation loop"""
        # Clear and redraw progress bar
        self.progress_canvas.delete("all")
        canvas_width = self.progress_canvas.winfo_width()
        
        if canvas_width > 1:  # Canvas is ready
            # Moving bar animation
            bar_width = 60
            self.bar_pos += self.bar_direction
            
            # Bounce at edges
            if self.bar_pos >= canvas_width - bar_width:
                self.bar_direction = -5
            elif self.bar_pos <= 0:
                self.bar_direction = 5
            
            # Draw animated bar
            self.progress_canvas.create_rectangle(
                self.bar_pos, 2, self.bar_pos + bar_width, 14,
                fill="#3498db", outline="#2980b9"
            )
        
        # Update status text
        statuses = [
            "Loading components...",
            "Setting up monitoring...", 
            "Preparing interface...",
            "Starting services...",
            "Almost ready...",
            "Ready!"
        ]
        
        # Change status every 30 animation frames (about 1 second at 30fps)
        if self.step % 30 == 0:
            status_index = (self.step // 30) % len(statuses)
            self.status_label.config(text=statuses[status_index])
            
            # Exit after showing all statuses
            if status_index == len(statuses) - 1 and self.step > 180:  # 6 seconds total
                self.splash.after(500, self.finish)
                return
        
        self.step += 1
        
        # Schedule next frame (30 FPS)
        self.splash.after(33, self.animate)
    
    def finish(self):
        """Close splash and launch GUI"""
        self.splash.destroy()
        
        try:
            from filepulse.gui import main as gui_main
            gui_main()
        except Exception as e:
            print(f"GUI launch error: {e}")
            tk.messagebox.showerror("Error", f"Failed to launch GUI: {e}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("🚀 FilePulse - Ultra Simple Animated Splash")
    UltraSimpleSplash().run()
