#!/usr/bin/env python3
"""
FilePulse - Simple Splash Launcher
Simplified approach to avoid tkinter root window conflicts
"""

import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

class SimpleSplashLauncher:
    def __init__(self):
        self.root = None
        self.splash = None
        self.is_running = True
        self.step = 0
        self.bar_pos = 0
        self.bar_direction = 4
        
    def create_splash(self):
        """Create and show splash screen"""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide root window
        
        # Create splash window
        self.splash = tk.Toplevel(self.root)
        self.splash.title("FilePulse")
        self.splash.overrideredirect(True)
        self.splash.configure(bg="black")
        
        # Load splash image
        self.load_splash_image()
        self.setup_splash_ui()
        self.center_splash()
        
        # Start splash animation and auto-close
        self.animate_splash()
        self.schedule_close()
        
    def load_splash_image(self):
        """Load and prepare splash image"""
        self.splash_image = None
        
        for path in ["assets/splash/Splash.png", "assets/splash/Splash-theme.png"]:
            if Path(path).exists():
                try:
                    img = Image.open(path)
                    img = img.convert("RGBA")
                    img.thumbnail((600, 400), Image.Resampling.LANCZOS)
                    
                    # Add transparency fade
                    self.add_fade_effect(img)
                    
                    self.splash_image = ImageTk.PhotoImage(img)
                    self.img_width, self.img_height = img.size
                    print(f"✓ Loaded splash: {path}")
                    return
                except Exception as e:
                    print(f"✗ Failed to load {path}: {e}")
        
        # Create default splash
        self.create_default_splash()
        
    def add_fade_effect(self, img):
        """Add transparent fade to bottom of image"""
        width, height = img.size
        fade_height = min(80, height // 4)
        
        # Create fade mask
        if img.mode == 'RGBA':
            r, g, b, a = img.split()
        else:
            img = img.convert('RGBA')
            r, g, b, a = img.split()
        
        # Apply fade to alpha channel
        fade_mask = Image.new('L', (width, height), 255)
        draw = ImageDraw.Draw(fade_mask)
        
        for y in range(height - fade_height, height):
            fade_alpha = int(255 * (1.0 - (height - y) / fade_height))
            draw.line([(0, y), (width, y)], fill=fade_alpha)
        
        # Combine with existing alpha
        new_alpha = Image.new('L', (width, height))
        for y in range(height):
            for x in range(width):
                orig_a = a.getpixel((x, y))
                fade_a = fade_mask.getpixel((x, y))
                new_alpha.putpixel((x, y), int((orig_a / 255.0) * (fade_a / 255.0) * 255))
        
        return Image.merge('RGBA', (r, g, b, new_alpha))
        
    def create_default_splash(self):
        """Create default splash if no image found"""
        width, height = 500, 350
        img = Image.new('RGBA', (width, height), (44, 62, 80, 255))
        draw = ImageDraw.Draw(img)
        
        # Add title area
        draw.rectangle([0, 0, width, 100], fill=(52, 73, 94, 255))
        
        # Add icon circle
        center_x, center_y = width // 2, 180
        draw.ellipse([center_x-40, center_y-40, center_x+40, center_y+40], 
                    fill=(52, 152, 219, 255))
        
        self.add_fade_effect(img)
        self.splash_image = ImageTk.PhotoImage(img)
        self.img_width, self.img_height = width, height
        print("✓ Created default splash")
        
    def setup_splash_ui(self):
        """Setup splash UI elements"""
        total_height = self.img_height + 80
        self.splash.geometry(f"{self.img_width}x{total_height}")
        
        # Main container
        main_frame = tk.Frame(self.splash, bg="black")
        main_frame.pack(fill="both", expand=True)
        
        # Splash image
        image_label = tk.Label(main_frame, image=self.splash_image, bg="black", bd=0)
        image_label.pack()
        
        # Progress area
        progress_frame = tk.Frame(main_frame, bg="black", height=80)
        progress_frame.pack(fill="x")
        progress_frame.pack_propagate(False)
        
        # Status label
        self.status_label = tk.Label(progress_frame, text="🔧 Initializing...", 
                                    fg="white", bg="#2c3e50", font=("Arial", 10), pady=8)
        self.status_label.pack(pady=10)
        
        # Progress canvas
        canvas_frame = tk.Frame(progress_frame, bg="black", height=20)
        canvas_frame.pack(fill="x", padx=60)
        canvas_frame.pack_propagate(False)
        
        self.progress_canvas = tk.Canvas(canvas_frame, height=16, bg="black", 
                                        highlightthickness=0)
        self.progress_canvas.pack(fill="x")
        
        # Set transparency
        self.splash.attributes("-alpha", 0.95)
        
    def center_splash(self):
        """Center splash on screen"""
        self.splash.update_idletasks()
        w, h = self.splash.winfo_width(), self.splash.winfo_height()
        x = (self.splash.winfo_screenwidth() - w) // 2
        y = (self.splash.winfo_screenheight() - h) // 2
        self.splash.geometry(f"{w}x{h}+{x}+{y}")
        
    def animate_splash(self):
        """Animate the splash screen"""
        if not self.is_running:
            return
            
        try:
            # Clear and redraw progress bar
            self.progress_canvas.delete("all")
            canvas_width = self.progress_canvas.winfo_width()
            
            if canvas_width > 1:
                # Animated progress bar
                bar_width = 80
                self.bar_pos += self.bar_direction
                
                # Bounce animation
                if self.bar_pos >= canvas_width - bar_width:
                    self.bar_direction = -4
                    self.bar_pos = canvas_width - bar_width
                elif self.bar_pos <= 0:
                    self.bar_direction = 4
                    self.bar_pos = 0
                
                # Draw progress bar
                self.progress_canvas.create_rectangle(0, 6, canvas_width, 10, 
                                                    fill="#34495e", outline="")
                
                # Animated bar segments
                colors = ["#3498db", "#5dade2", "#85c1e9", "#5dade2", "#3498db"]
                segment_width = bar_width // len(colors)
                
                for i, color in enumerate(colors):
                    x1 = self.bar_pos + i * segment_width
                    x2 = x1 + segment_width
                    if x2 > self.bar_pos + bar_width:
                        x2 = self.bar_pos + bar_width
                    
                    if x1 < canvas_width and x2 > 0:
                        self.progress_canvas.create_rectangle(
                            max(0, x1), 4, min(canvas_width, x2), 12,
                            fill=color, outline="")
            
            # Update status
            statuses = [
                "🔧 Initializing components...",
                "📋 Loading configuration...", 
                "👁️ Setting up monitoring...",
                "🖥️ Preparing interface...",
                "🚀 Starting services...",
                "✨ Finalizing setup...",
                "🎉 Ready to launch!"
            ]
            
            if self.step % 40 == 0:
                status_index = (self.step // 40) % len(statuses)
                self.status_label.config(text=statuses[status_index])
            
            self.step += 1
            
            # Continue animation
            if self.is_running:
                self.splash.after(35, self.animate_splash)
                
        except tk.TclError:
            self.is_running = False
            
    def schedule_close(self):
        """Schedule splash to close and launch GUI"""
        def close_and_launch():
            time.sleep(3.0)  # Show splash for 3 seconds
            if self.is_running:
                self.root.after(0, self.close_splash_and_launch_gui)
        
        # Run in background thread
        threading.Thread(target=close_and_launch, daemon=True).start()
        
    def close_splash_and_launch_gui(self):
        """Close splash and launch main GUI"""
        try:
            # Fade out effect
            self.fade_out_splash()
        except:
            self.launch_main_gui()
            
    def fade_out_splash(self):
        """Fade out splash with alpha transition"""
        def fade_step(alpha=0.95):
            try:
                if alpha > 0 and self.splash and self.splash.winfo_exists():
                    self.splash.attributes("-alpha", alpha)
                    self.splash.after(30, lambda: fade_step(alpha - 0.05))
                else:
                    self.launch_main_gui()
            except tk.TclError:
                self.launch_main_gui()
        
        fade_step()
        
    def launch_main_gui(self):
        """Launch the main FilePulse GUI"""
        try:
            self.is_running = False
            
            # Close splash
            if self.splash:
                try:
                    self.splash.destroy()
                except:
                    pass
            
            print("🔄 Launching main GUI...")
            
            # Import GUI components
            from filepulse.gui import FilePulseGUI
            print("✅ GUI module imported")
            
            # Configure root window for main GUI
            self.root.deiconify()
            self.root.title("FilePulse - Filesystem Monitor")
            self.root.geometry("900x700")
            self.root.minsize(800, 600)
            
            # Create main GUI
            app = FilePulseGUI(self.root)
            print("✅ Main GUI created successfully")
            
        except Exception as e:
            print(f"❌ GUI launch error: {e}")
            import traceback
            traceback.print_exc()
            try:
                tk.messagebox.showerror("Error", f"Failed to launch GUI: {e}")
            except:
                pass
            self.root.quit()
            
    def run(self):
        """Run the splash launcher"""
        self.create_splash()
        self.root.mainloop()

if __name__ == "__main__":
    print("🚀 FilePulse - Simple Splash Launcher")
    launcher = SimpleSplashLauncher()
    launcher.run()
