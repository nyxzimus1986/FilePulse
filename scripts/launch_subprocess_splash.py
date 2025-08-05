#!/usr/bin/env python3
"""
FilePulse - Subprocess Splash Launcher
Uses subprocess to completely separate splash from main GUI
"""

import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import sys
import subprocess
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

class SubprocessSplashLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.configure(bg="black")
        
        # Animation state
        self.step = 0
        self.bar_pos = 0
        self.bar_direction = 4
        self.is_running = True
        
        # Setup splash
        self.load_splash_image()
        self.setup_ui()
        self.center_window()
        
        # Start animation and schedule GUI launch
        self.animate()
        self.schedule_gui_launch()
        
    def load_splash_image(self):
        """Load splash image with transparency"""
        self.splash_image = None
        
        for path in ["assets/splash/Splash.png", "assets/splash/Splash-theme.png"]:
            if Path(path).exists():
                try:
                    img = Image.open(path)
                    img = img.convert("RGBA")
                    img.thumbnail((600, 400), Image.Resampling.LANCZOS)
                    
                    # Add fade effect
                    self.add_transparency_fade(img)
                    
                    self.splash_image = ImageTk.PhotoImage(img)
                    self.img_width, self.img_height = img.size
                    print(f"✓ Loaded: {path}")
                    return
                except Exception as e:
                    print(f"✗ Error loading {path}: {e}")
        
        # Fallback to default
        self.create_default_image()
        
    def add_transparency_fade(self, img):
        """Add transparent fade effect to bottom"""
        width, height = img.size
        fade_height = min(100, height // 3)
        
        # Work with alpha channel
        if img.mode == 'RGBA':
            r, g, b, a = img.split()
        else:
            img = img.convert('RGBA')
            r, g, b, a = img.split()
        
        # Create fade
        new_alpha = Image.new('L', (width, height), 255)
        for y in range(height - fade_height, height):
            fade_factor = 1.0 - (height - y) / fade_height
            alpha_val = int(255 * fade_factor)
            for x in range(width):
                orig_alpha = a.getpixel((x, y))
                new_alpha.putpixel((x, y), int((orig_alpha / 255.0) * (alpha_val / 255.0) * 255))
        
        # Rebuild image
        img = Image.merge('RGBA', (r, g, b, new_alpha))
        
    def create_default_image(self):
        """Create default splash image"""
        width, height = 500, 350
        img = Image.new('RGBA', (width, height), (44, 62, 80, 255))
        draw = ImageDraw.Draw(img)
        
        # Header
        draw.rectangle([0, 0, width, 120], fill=(52, 73, 94, 255))
        
        # Icon
        cx, cy = width // 2, 180
        draw.ellipse([cx-40, cy-40, cx+40, cy+40], fill=(52, 152, 219, 255))
        
        self.add_transparency_fade(img)
        self.splash_image = ImageTk.PhotoImage(img)
        self.img_width, self.img_height = width, height
        print("✓ Created default splash")
        
    def setup_ui(self):
        """Setup splash UI"""
        total_height = self.img_height + 80
        self.root.geometry(f"{self.img_width}x{total_height}")
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="black")
        main_frame.pack(fill="both", expand=True)
        
        # Image
        img_label = tk.Label(main_frame, image=self.splash_image, bg="black", bd=0)
        img_label.pack()
        
        # Progress area
        progress_area = tk.Frame(main_frame, bg="black", height=80)
        progress_area.pack(fill="x")
        progress_area.pack_propagate(False)
        
        # Status
        self.status_label = tk.Label(progress_area, text="🔧 Starting FilePulse...",
                                    fg="white", bg="#2c3e50", font=("Arial", 10), pady=8)
        self.status_label.pack(pady=10)
        
        # Progress bar
        bar_frame = tk.Frame(progress_area, bg="black", height=20)
        bar_frame.pack(fill="x", padx=60)
        bar_frame.pack_propagate(False)
        
        self.progress_canvas = tk.Canvas(bar_frame, height=16, bg="black",
                                        highlightthickness=0)
        self.progress_canvas.pack(fill="x")
        
        # Transparency
        self.root.attributes("-alpha", 0.95)\n        \n    def center_window(self):\n        \"\"\"Center on screen\"\"\"\n        self.root.update_idletasks()\n        w, h = self.root.winfo_width(), self.root.winfo_height()\n        x = (self.root.winfo_screenwidth() - w) // 2\n        y = (self.root.winfo_screenheight() - h) // 2\n        self.root.geometry(f\"{w}x{h}+{x}+{y}\")\n        \n    def animate(self):\n        \"\"\"Animate progress bar\"\"\"\n        if not self.is_running:\n            return\n            \n        # Clear canvas\n        self.progress_canvas.delete(\"all\")\n        canvas_width = self.progress_canvas.winfo_width()\n        \n        if canvas_width > 1:\n            # Bouncing bar\n            bar_width = 80\n            self.bar_pos += self.bar_direction\n            \n            if self.bar_pos >= canvas_width - bar_width:\n                self.bar_direction = -4\n                self.bar_pos = canvas_width - bar_width\n            elif self.bar_pos <= 0:\n                self.bar_direction = 4\n                self.bar_pos = 0\n            \n            # Draw track\n            self.progress_canvas.create_rectangle(0, 6, canvas_width, 10,\n                                                fill=\"#34495e\", outline=\"\")\n            \n            # Draw animated bar\n            colors = [\"#3498db\", \"#5dade2\", \"#85c1e9\", \"#5dade2\", \"#3498db\"]\n            seg_width = bar_width // len(colors)\n            \n            for i, color in enumerate(colors):\n                x1 = self.bar_pos + i * seg_width\n                x2 = x1 + seg_width\n                if x2 > self.bar_pos + bar_width:\n                    x2 = self.bar_pos + bar_width\n                \n                if x1 < canvas_width and x2 > 0:\n                    self.progress_canvas.create_rectangle(\n                        max(0, x1), 4, min(canvas_width, x2), 12,\n                        fill=color, outline=\"\")\n        \n        # Update status\n        statuses = [\n            \"🔧 Initializing components...\",\n            \"📋 Loading configuration...\",\n            \"👁️ Setting up monitoring...\",\n            \"🖥️ Preparing interface...\",\n            \"🚀 Starting services...\",\n            \"✨ Finalizing setup...\",\n            \"🎉 Ready to launch!\"\n        ]\n        \n        if self.step % 35 == 0:\n            status_idx = (self.step // 35) % len(statuses)\n            self.status_label.config(text=statuses[status_idx])\n        \n        self.step += 1\n        \n        # Continue\n        if self.is_running:\n            self.root.after(30, self.animate)\n            \n    def schedule_gui_launch(self):\n        \"\"\"Schedule main GUI launch\"\"\"\n        # Launch after 3 seconds\n        self.root.after(3000, self.launch_gui_subprocess)\n        \n    def launch_gui_subprocess(self):\n        \"\"\"Launch GUI in subprocess and close splash\"\"\"\n        try:\n            print(\"🔄 Launching main GUI in subprocess...\")\n            \n            # Start main GUI as subprocess\n            gui_script = '''\nimport sys\nimport tkinter as tk\nfrom pathlib import Path\n\n# Add path\nsys.path.insert(0, str(Path(__file__).parent))\n\ntry:\n    from filepulse.gui import FilePulseGUI\n    \n    # Create GUI\n    root = tk.Tk()\n    root.title(\"FilePulse - Filesystem Monitor\")\n    root.geometry(\"900x700\")\n    root.minsize(800, 600)\n    \n    app = FilePulseGUI(root)\n    root.mainloop()\n    \nexcept Exception as e:\n    import traceback\n    print(f\"GUI Error: {e}\")\n    traceback.print_exc()\n    input(\"Press Enter to exit...\")\n'''\n            \n            # Write temp script\n            temp_script = Path(\"temp_gui_launcher.py\")\n            temp_script.write_text(gui_script)\n            \n            # Launch subprocess\n            subprocess.Popen([sys.executable, str(temp_script)], \n                           creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0)\n            \n            print(\"✅ GUI subprocess launched\")\n            \n            # Fade out and close splash\n            self.fade_and_close()\n            \n        except Exception as e:\n            print(f\"❌ Subprocess launch error: {e}\")\n            self.root.quit()\n            \n    def fade_and_close(self):\n        \"\"\"Fade out splash and close\"\"\"\n        def fade(alpha=0.95):\n            if alpha > 0:\n                try:\n                    self.root.attributes(\"-alpha\", alpha)\n                    self.root.after(30, lambda: fade(alpha - 0.05))\n                except:\n                    self.root.quit()\n            else:\n                self.root.quit()\n        \n        self.is_running = False\n        fade()\n        \n    def run(self):\n        \"\"\"Run splash\"\"\"\n        self.root.mainloop()\n\nif __name__ == \"__main__\":\n    print(\"🚀 FilePulse - Subprocess Splash Launcher\")\n    launcher = SubprocessSplashLauncher()\n    launcher.run()
