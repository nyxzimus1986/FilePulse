#!/usr/bin/env python3
"""
FilePulse - Transparent Bottom Splash Screen
Modern splash with transparent fade effect at the bottom
"""

import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import sys
from pathlib import Path

# Add both current directory and parent directory to path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))  # Main project directory
sys.path.insert(0, str(current_dir))  # Scripts directory

print(f"🔍 Script directory: {current_dir}")
print(f"🔍 Parent directory: {parent_dir}")
print(f"🔍 Looking for assets in: {parent_dir / 'assets/splash/'}")

class TransparentSplash:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        
        self.splash = tk.Toplevel()
        self.splash.title("FilePulse")
        self.splash.overrideredirect(True)
        
        # Enable transparency support
        self.splash.attributes("-alpha", 1.0)  # Full opacity initially
        self.splash.configure(bg="black")
        
        # Animation state
        self.bar_pos = 0
        self.bar_direction = 4
        self.step = 0
        self.is_running = True  # Flag to control animation
        self.after_id = None    # Track scheduled events
        
        # Bind cleanup to window close
        self.splash.protocol("WM_DELETE_WINDOW", self.safe_close)
        
        # Load and process custom image with transparency
        self.load_and_process_image()
        self.setup_ui()
        self.center()
        
        # Start animation
        self.animate()
    
    def load_and_process_image(self):
        """Load custom splash and add transparent bottom fade"""
        self.splash_image = None
        
        # Look for assets in parent directory since we're in scripts/
        parent_dir = Path(__file__).parent.parent
        asset_paths = [
            parent_dir / "assets/splash/Splash.png", 
            parent_dir / "assets/splash/Splash-theme.png"
        ]
        
        for path in asset_paths:
            if path.exists():
                try:
                    # Load original image
                    img = Image.open(path)
                    img = img.convert("RGBA")  # Ensure RGBA for transparency
                    
                    # Resize while maintaining aspect ratio
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
        
        # Create an alpha mask for the fade effect
        fade_height = min(100, height // 3)  # Fade bottom 1/3 or max 100px
        
        # Get the existing alpha channel or create one
        if img.mode == 'RGBA':
            r, g, b, a = img.split()
        else:
            img = img.convert('RGBA')
            r, g, b, a = img.split()
        
        # Create fade mask
        fade_mask = Image.new('L', (width, height), 255)  # Start with full opacity
        
        # Create gradient fade
        for y in range(height - fade_height, height):
            # Calculate fade alpha (1.0 at top of fade, 0.0 at bottom)
            fade_progress = (height - y) / fade_height
            alpha_value = int(255 * (1.0 - fade_progress))
            
            # Draw horizontal line with calculated alpha
            fade_draw = ImageDraw.Draw(fade_mask)
            fade_draw.line([(0, y), (width, y)], fill=alpha_value)
        
        # Apply the fade mask to the existing alpha channel
        # Multiply existing alpha with fade mask
        new_alpha = Image.new('L', (width, height))
        for y in range(height):
            for x in range(width):
                original_alpha = a.getpixel((x, y))
                fade_alpha = fade_mask.getpixel((x, y))
                # Multiply alphas (both normalized to 0-1, then back to 0-255)
                combined_alpha = int((original_alpha / 255.0) * (fade_alpha / 255.0) * 255)
                new_alpha.putpixel((x, y), combined_alpha)
        
        # Merge channels back
        img = Image.merge('RGBA', (r, g, b, new_alpha))
        return img
    
    def create_default_with_fade(self):
        """Create a default splash image with transparent fade"""
        # Create a gradient image
        width, height = 500, 350
        img = Image.new('RGBA', (width, height), (44, 62, 80, 255))  # Dark blue
        draw = ImageDraw.Draw(img)
        
        # Add some visual elements
        # Title area
        draw.rectangle([0, 0, width, 120], fill=(52, 73, 94, 255))
        
        # Icon area (simple representation)
        center_x, center_y = width // 2, 180
        draw.ellipse([center_x-40, center_y-40, center_x+40, center_y+40], 
                    fill=(52, 152, 219, 255))  # Blue circle
        
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
        
        # Main container with transparent background
        main_frame = tk.Frame(self.splash, bg="black")
        main_frame.pack(fill="both", expand=True)
        
        # Image with transparent fade
        image_label = tk.Label(main_frame, image=self.splash_image, 
                              bg="black", bd=0)
        image_label.pack()
        
        # Transparent progress area
        progress_area = tk.Frame(main_frame, bg="black", height=progress_height)
        progress_area.pack(fill="x")
        progress_area.pack_propagate(False)
        
        # Status text with semi-transparent background
        status_bg = tk.Frame(progress_area, bg="#2c3e50", relief="flat")
        status_bg.pack(expand=True, fill="x", padx=40, pady=8)
        
        self.status_label = tk.Label(status_bg, text="Loading...", 
                                    fg="white", bg="#2c3e50", 
                                    font=("Arial", 10), pady=4)
        self.status_label.pack()
        
        # Progress bar with transparent background
        bar_container = tk.Frame(progress_area, bg="black", height=20)
        bar_container.pack(fill="x", padx=60, pady=(0, 5))
        bar_container.pack_propagate(False)
        
        self.progress_canvas = tk.Canvas(bar_container, height=16, 
                                        bg="black", highlightthickness=0,
                                        relief="flat")
        self.progress_canvas.pack(fill="x")
        
        # Set transparency for the splash window
        self.splash.attributes("-alpha", 0.95)  # Slight transparency
        
        # Add proper window close handling
        self.splash.protocol("WM_DELETE_WINDOW", self.safe_close)
    
    def center(self):
        """Center splash on screen"""
        self.splash.update_idletasks()
        w, h = self.splash.winfo_width(), self.splash.winfo_height()
        x = (self.splash.winfo_screenwidth() - w) // 2
        y = (self.splash.winfo_screenheight() - h) // 2
        self.splash.geometry(f"{w}x{h}+{x}+{y}")
    
    def animate(self):
        """Animate progress bar with safe event handling"""
        # Check if we should continue animating
        if not self.is_running:
            print("❌ Animation stopped - not running", flush=True)
            return
        
        # Debug output every 30 frames (~1 second)
        if self.step % 30 == 0:
            print(f"Animation step: {self.step}", flush=True)
            
        try:
            # Update status text FIRST - simpler approach
            statuses = [
                "🔧 Initializing components...",
                "📋 Loading configuration...",
                "👁️ Setting up monitoring...",
                "🖥️ Preparing interface...",
                "🚀 Starting services...",
                "✨ Finalizing setup...",
                "🎉 Ready to monitor!"
            ]
            
            # Change status every 30 frames (1 second at 33ms per frame)
            if self.step % 30 == 0:
                status_index = (self.step // 30) % len(statuses)
                self.status_label.config(text=statuses[status_index])
                print(f"Status {status_index + 1}/7: {statuses[status_index]}", flush=True)
                
                # Exit after last status - MUCH SIMPLER
                if status_index == len(statuses) - 1 and self.step >= 180:  # 6 statuses * 30 = 180
                    print("✅ All statuses complete! Finishing...", flush=True)
                    self.is_running = False
                    # Use root.after instead of splash.after for reliability
                    self.root.after(500, self.finish)
                    return
            
            # Draw simple progress bar
            self.progress_canvas.delete("all")
            canvas_width = self.progress_canvas.winfo_width()
            
            if canvas_width > 1:
                # Simple moving bar
                bar_width = 60
                max_pos = canvas_width - bar_width
                progress = (self.step % 60) / 60.0  # Reset every 60 frames
                self.bar_pos = int(progress * max_pos)
                
                # Background track
                self.progress_canvas.create_rectangle(
                    0, 6, canvas_width, 10,
                    fill="#34495e", outline=""
                )
                
                # Simple blue bar
                self.progress_canvas.create_rectangle(
                    self.bar_pos, 4, self.bar_pos + bar_width, 12,
                    fill="#3498db", outline=""
                )
            
            # Force exit after reasonable time
            if self.step > 250:  # ~8 seconds
                print("⏰ Safety timeout - forcing finish", flush=True)
                self.is_running = False
                self.root.after(100, self.finish)
                return
            
            self.step += 1
            
            # Schedule next frame
            if self.is_running:
                self.after_id = self.splash.after(33, self.animate)
                
        except Exception as e:
            print(f"❌ Animation error: {e}", flush=True)
            self.is_running = False
            self.root.after(100, self.finish)
    
    def safe_close(self):
        """Safely close the splash screen with proper cleanup"""
        print("🔄 Safe close initiated...", flush=True)
        self.is_running = False
        
        # Cancel any pending after() calls
        if hasattr(self, 'after_id') and self.after_id:
            try:
                self.splash.after_cancel(self.after_id)
            except tk.TclError:
                pass  # Window may already be destroyed
        
        # Destroy splash window safely
        try:
            if self.splash and self.splash.winfo_exists():
                self.splash.destroy()
                print("🗑️ Splash window destroyed", flush=True)
        except tk.TclError:
            pass  # Window already destroyed
        
        print("✅ Splash screen closed safely", flush=True)
        
        # Schedule GUI launch after splash cleanup
        print("🚀 Scheduling GUI launch...", flush=True)
        self.root.after(100, self.launch_gui)
    
    def finish(self):
        """Simple finish - skip fade and go straight to GUI"""
        print("� Finishing splash screen...", flush=True)
        self.is_running = False
        
        # Cancel any pending animations
        if hasattr(self, 'after_id') and self.after_id:
            try:
                self.splash.after_cancel(self.after_id)
            except:
                pass
        
        # Simple direct close - no fade to avoid hanging
        try:
            if self.splash and self.splash.winfo_exists():
                self.splash.destroy()
                print("🗑️ Splash window closed", flush=True)
        except:
            pass
        
        # Launch GUI immediately
        print("🚀 Launching GUI now...", flush=True)
        self.launch_gui()
    
    def launch_gui(self):
        """Launch the main GUI with proper error handling"""
        try:
            print("🔄 Attempting to launch main GUI...", flush=True)
            
            # Check if filepulse module exists in parent directory
            parent_dir = Path(__file__).parent.parent
            filepulse_path = parent_dir / "filepulse"
            
            print(f"🔍 Looking for filepulse module at: {filepulse_path}", flush=True)
            
            if not filepulse_path.exists():
                print(f"❌ FilePulse module not found!", flush=True)
                import tkinter.messagebox as msgbox
                msgbox.showerror("Module Error", 
                               f"FilePulse module not found at:\n{filepulse_path}\n\n"
                               f"Please ensure the filepulse directory exists.")
                self.root.quit()
                return
            
            print("✓ FilePulse directory found", flush=True)
            
            # Import GUI components
            from filepulse.gui import FilePulseGUI
            print("✅ GUI module imported successfully", flush=True)
            
            # Show the main window
            self.root.deiconify()
            self.root.title("FilePulse - Filesystem Monitor")
            self.root.geometry("900x700")
            self.root.minsize(800, 600)
            
            # Create and run the GUI application
            app = FilePulseGUI(self.root)
            print("✅ GUI application created successfully", flush=True)
            
        except ImportError as e:
            print(f"❌ Import error: {e}", flush=True)
            import tkinter.messagebox as msgbox
            msgbox.showerror("Import Error", 
                           f"Failed to import FilePulse GUI:\n\n{e}\n\n"
                           f"Please check that the filepulse module is properly installed.")
            self.root.quit()
        except Exception as e:
            print(f"❌ GUI launch error: {e}", flush=True)
            import traceback
            traceback.print_exc()
            import tkinter.messagebox as msgbox
            msgbox.showerror("Error", f"Failed to launch GUI:\n\n{e}")
            self.root.quit()
    
    def run(self):
        """Run the splash screen"""
        self.root.mainloop()

if __name__ == "__main__":
    print("🚀 FilePulse - Transparent Bottom Splash Screen")
    TransparentSplash().run()
