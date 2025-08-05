#!/usr/bin/env python3
"""
FilePulse - Fixed Transparent Splash Screen
Uses proper window lifecycle management to avoid freezing
"""

import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

class FixedTransparentSplash:
    def __init__(self):
        # Create the main application root (hidden initially)
        self.app_root = tk.Tk()
        self.app_root.withdraw()  # Hide main window during splash
        self.app_root.title("FilePulse - Filesystem Monitor")
        self.app_root.geometry("900x700")
        self.app_root.minsize(800, 600)
        
        # Create splash as Toplevel of main window
        self.splash = tk.Toplevel(self.app_root)
        self.splash.title("FilePulse")
        self.splash.overrideredirect(True)
        self.splash.configure(bg="black")
        
        # Animation state
        self.bar_pos = 0
        self.bar_direction = 4
        self.step = 0
        self.is_running = True
        self.after_id = None
        
        # Load splash elements
        self.load_and_process_image()
        self.setup_ui()
        self.center()
        
        # Start splash sequence
        self.animate()
        self.schedule_main_gui()
        
    def load_and_process_image(self):
        """Load custom splash and add transparent bottom fade"""
        self.splash_image = None
        
        for path in ["assets/splash/Splash.png", "assets/splash/Splash-theme.png"]:
            if Path(path).exists():
                try:
                    # Load original image
                    img = Image.open(path)
                    img = img.convert("RGBA")
                    img.thumbnail((600, 400), Image.Resampling.LANCZOS)
                    
                    # Create transparency fade at bottom
                    self.add_bottom_fade(img)
                    
                    # Convert to PhotoImage
                    self.splash_image = ImageTk.PhotoImage(img)
                    self.img_width, self.img_height = img.size
                    
                    print(f"✓ Loaded with transparent fade: {path}")
                    return
                    
                except Exception as e:
                    print(f"✗ Failed to process {path}: {e}")
        
        # Create default with transparency
        self.create_default_with_fade()
    
    def add_bottom_fade(self, img):
        """Add a transparent fade effect to the bottom of the image"""
        width, height = img.size
        fade_height = min(100, height // 3)
        
        # Get the existing alpha channel or create one
        if img.mode == 'RGBA':
            r, g, b, a = img.split()
        else:
            img = img.convert('RGBA')
            r, g, b, a = img.split()
        
        # Create fade mask
        fade_mask = Image.new('L', (width, height), 255)
        
        # Create gradient fade at bottom
        for y in range(height - fade_height, height):
            fade_progress = (height - y) / fade_height
            alpha_value = int(255 * (1.0 - fade_progress))
            
            # Draw horizontal line with calculated alpha
            fade_draw = ImageDraw.Draw(fade_mask)
            fade_draw.line([(0, y), (width, y)], fill=alpha_value)
        
        # Apply the fade mask to the existing alpha channel
        new_alpha = Image.new('L', (width, height))
        for y in range(height):
            for x in range(width):
                original_alpha = a.getpixel((x, y))
                fade_alpha = fade_mask.getpixel((x, y))
                combined_alpha = int((original_alpha / 255.0) * (fade_alpha / 255.0) * 255)
                new_alpha.putpixel((x, y), combined_alpha)
        
        # Merge channels back
        return Image.merge('RGBA', (r, g, b, new_alpha))
    
    def create_default_with_fade(self):
        """Create a default splash image with transparent fade"""
        width, height = 500, 350
        img = Image.new('RGBA', (width, height), (44, 62, 80, 255))
        draw = ImageDraw.Draw(img)
        
        # Title area
        draw.rectangle([0, 0, width, 120], fill=(52, 73, 94, 255))
        
        # Icon area
        center_x, center_y = width // 2, 180
        draw.ellipse([center_x-40, center_y-40, center_x+40, center_y+40], 
                    fill=(52, 152, 219, 255))
        
        # Add transparent fade at bottom
        self.add_bottom_fade(img)
        
        self.splash_image = ImageTk.PhotoImage(img)
        self.img_width, self.img_height = width, height
        print("✓ Created default with transparent fade")
    
    def setup_ui(self):
        """Setup UI with transparent background"""
        # Set window size
        progress_height = 60
        total_height = self.img_height + progress_height
        self.splash.geometry(f"{self.img_width}x{total_height}")
        
        # Main container
        main_frame = tk.Frame(self.splash, bg="black")
        main_frame.pack(fill="both", expand=True)
        
        # Image with transparent fade
        image_label = tk.Label(main_frame, image=self.splash_image, 
                              bg="black", bd=0)
        image_label.pack()
        
        # Progress area
        progress_area = tk.Frame(main_frame, bg="black", height=progress_height)
        progress_area.pack(fill="x")
        progress_area.pack_propagate(False)
        
        # Status text
        status_bg = tk.Frame(progress_area, bg="#2c3e50", relief="flat")
        status_bg.pack(expand=True, fill="x", padx=40, pady=8)
        
        self.status_label = tk.Label(status_bg, text="Loading...", 
                                    fg="white", bg="#2c3e50", 
                                    font=("Arial", 10), pady=4)
        self.status_label.pack()
        
        # Progress bar
        bar_container = tk.Frame(progress_area, bg="black", height=20)
        bar_container.pack(fill="x", padx=60, pady=(0, 5))
        bar_container.pack_propagate(False)
        
        self.progress_canvas = tk.Canvas(bar_container, height=16, 
                                        bg="black", highlightthickness=0,
                                        relief="flat")
        self.progress_canvas.pack(fill="x")
        
        # Set transparency
        self.splash.attributes("-alpha", 0.95)
    
    def center(self):
        """Center splash on screen"""
        self.splash.update_idletasks()
        w, h = self.splash.winfo_width(), self.splash.winfo_height()
        x = (self.splash.winfo_screenwidth() - w) // 2
        y = (self.splash.winfo_screenheight() - h) // 2
        self.splash.geometry(f"{w}x{h}+{x}+{y}")
    
    def animate(self):
        """Animate progress bar"""
        if not self.is_running:
            return
        
        try:
            # Clear and redraw
            self.progress_canvas.delete("all")
            canvas_width = self.progress_canvas.winfo_width()
            
            if canvas_width > 1:
                # Animated bouncing bar
                bar_width = 80
                self.bar_pos += self.bar_direction
                
                # Bounce logic
                if self.bar_pos >= canvas_width - bar_width:
                    self.bar_direction = -4
                    self.bar_pos = canvas_width - bar_width
                elif self.bar_pos <= 0:
                    self.bar_direction = 4
                    self.bar_pos = 0
                
                # Draw track
                self.progress_canvas.create_rectangle(
                    0, 6, canvas_width, 10,
                    fill="#34495e", outline=""
                )
                
                # Draw animated bar with gradient
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
                            fill=color, outline=""
                        )
            
            # Update status text
            statuses = [
                "🔧 Initializing components...",
                "📋 Loading configuration...",
                "👁️ Setting up monitoring...",
                "🖥️ Preparing interface...",
                "🚀 Starting services...",
                "✨ Finalizing setup...",
                "🎉 Ready to monitor!"
            ]
            
            # Change status periodically
            if self.step % 45 == 0:
                status_index = (self.step // 45) % len(statuses)
                self.status_label.config(text=statuses[status_index])
                
                # Complete after full cycle
                if status_index == len(statuses) - 1 and self.step > 300:
                    self.complete_splash()
                    return
            
            self.step += 1
            
            # Continue animation
            if self.is_running:
                self.after_id = self.splash.after(33, self.animate)
                
        except tk.TclError:
            self.is_running = False
        except Exception as e:
            print(f"Animation error: {e}")
            self.is_running = False
    
    def schedule_main_gui(self):
        """Schedule main GUI to be ready"""
        def load_gui_in_background():
            """Load GUI components in background thread"""
            try:
                time.sleep(0.5)  # Give splash time to display
                print("🔄 Pre-loading GUI components...")
                
                # Import GUI module (this might take time)
                from filepulse.gui import FilePulseGUI
                self.gui_class = FilePulseGUI
                
                print("✅ GUI components loaded")
                
            except Exception as e:
                print(f"❌ Error pre-loading GUI: {e}")
                self.gui_class = None
        
        # Start background loading
        threading.Thread(target=load_gui_in_background, daemon=True).start()
    
    def complete_splash(self):
        """Complete splash sequence and show main GUI"""
        def fade_out(alpha=0.95):
            if alpha > 0 and self.is_running:
                try:
                    self.splash.attributes("-alpha", alpha)
                    self.splash.after(30, lambda: fade_out(alpha - 0.05))
                except tk.TclError:
                    self.show_main_gui()
            else:
                self.show_main_gui()
        
        # Start fade out
        fade_out()
    
    def show_main_gui(self):
        """Show the main GUI"""
        try:
            self.is_running = False
            
            # Clean up splash
            if self.after_id:
                try:
                    self.splash.after_cancel(self.after_id)
                except:
                    pass
            
            try:
                self.splash.destroy()
            except:
                pass
            
            print("🔄 Starting main GUI...")
            
            # Import and create GUI if not already loaded
            if not hasattr(self, 'gui_class') or self.gui_class is None:
                from filepulse.gui import FilePulseGUI
                self.gui_class = FilePulseGUI
            
            # Show main window and create GUI
            self.app_root.deiconify()
            app = self.gui_class(self.app_root)
            
            print("✅ Main GUI ready")
            
        except Exception as e:
            print(f"❌ Error showing main GUI: {e}")
            import traceback
            traceback.print_exc()
            
            try:
                tk.messagebox.showerror("Error", f"Failed to launch GUI: {e}")
            except:
                pass
            
            self.app_root.quit()
    
    def run(self):
        """Run the application"""
        self.app_root.mainloop()

if __name__ == "__main__":
    print("🚀 FilePulse - Fixed Transparent Splash Screen")
    app = FixedTransparentSplash()
    app.run()
