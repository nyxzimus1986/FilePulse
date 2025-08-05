#!/usr/bin/env python3
"""
FilePulse Icon Generator
Creates custom icons for the FilePulse application
"""

import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
from pathlib import Path

class IconGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("FilePulse Icon Generator")
        self.root.geometry("800x600")
        
        # Icon settings
        self.bg_color = "#3498db"
        self.folder_color = "#2980b9"
        self.pulse_color = "#e74c3c"
        self.text_color = "#ffffff"
        self.icon_size = 256
        
        # Custom image settings
        self.custom_image = None
        self.use_custom_image = False
        self.custom_image_opacity = 100
        self.custom_image_scale = 100
        
        # Create UI
        self.setup_ui()
        
        # Generate initial preview
        self.generate_preview()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="FilePulse Icon Generator", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Left panel - Controls
        controls_frame = ttk.LabelFrame(main_frame, text="Icon Settings", padding="10")
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Color settings
        ttk.Label(controls_frame, text="Background Color:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.bg_color_btn = tk.Button(controls_frame, text="Choose", 
                                     command=lambda: self.choose_color('bg_color'),
                                     bg=self.bg_color, width=10)
        self.bg_color_btn.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        ttk.Label(controls_frame, text="Folder Color:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.folder_color_btn = tk.Button(controls_frame, text="Choose", 
                                         command=lambda: self.choose_color('folder_color'),
                                         bg=self.folder_color, width=10)
        self.folder_color_btn.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        ttk.Label(controls_frame, text="Pulse Color:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.pulse_color_btn = tk.Button(controls_frame, text="Choose", 
                                        command=lambda: self.choose_color('pulse_color'),
                                        bg=self.pulse_color, width=10)
        self.pulse_color_btn.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Size settings
        ttk.Label(controls_frame, text="Icon Size:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.size_var = tk.StringVar(value="256")
        size_combo = ttk.Combobox(controls_frame, textvariable=self.size_var, 
                                 values=["16", "32", "48", "64", "128", "256", "512"],
                                 width=10)
        size_combo.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        size_combo.bind('<<ComboboxSelected>>', self.on_size_change)
        
        # Style options
        ttk.Label(controls_frame, text="Icon Style:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.style_var = tk.StringVar(value="Modern")
        style_combo = ttk.Combobox(controls_frame, textvariable=self.style_var,
                                  values=["Modern", "Classic", "Minimal", "3D"],
                                  width=10)
        style_combo.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        style_combo.bind('<<ComboboxSelected>>', self.on_style_change)
        
        # Text overlay
        ttk.Label(controls_frame, text="Add Text:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.text_var = tk.StringVar(value="FP")
        text_entry = ttk.Entry(controls_frame, textvariable=self.text_var, width=12)
        text_entry.grid(row=5, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        text_entry.bind('<KeyRelease>', self.on_text_change)
        
        # Custom Image Section
        image_frame = ttk.LabelFrame(controls_frame, text="Custom Image", padding="5")
        image_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Use custom image checkbox
        self.use_custom_var = tk.BooleanVar()
        self.custom_check = ttk.Checkbutton(image_frame, text="Use Custom Image", 
                                           variable=self.use_custom_var,
                                           command=self.toggle_custom_image)
        self.custom_check.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Load image button
        self.load_image_btn = ttk.Button(image_frame, text="Load Image", 
                                        command=self.load_custom_image,
                                        state="disabled")
        self.load_image_btn.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Image info label
        self.image_info_label = ttk.Label(image_frame, text="No image loaded", 
                                         foreground="gray")
        self.image_info_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Opacity slider
        ttk.Label(image_frame, text="Opacity:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.opacity_var = tk.IntVar(value=100)
        self.opacity_scale = ttk.Scale(image_frame, from_=0, to=100, 
                                      variable=self.opacity_var,
                                      command=self.on_opacity_change,
                                      state="disabled")
        self.opacity_scale.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Scale slider
        ttk.Label(image_frame, text="Scale:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.scale_var = tk.IntVar(value=100)
        self.scale_scale = ttk.Scale(image_frame, from_=10, to=200, 
                                    variable=self.scale_var,
                                    command=self.on_scale_change,
                                    state="disabled")
        self.scale_scale.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        
        image_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Generate Preview", 
                  command=self.generate_preview).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Export Icon", 
                  command=self.export_icon).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Load Preset", 
                  command=self.load_preset).grid(row=0, column=2, padx=5)
        
        # Presets
        preset_frame = ttk.LabelFrame(controls_frame, text="Quick Presets", padding="5")
        preset_frame.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(preset_frame, text="Default Blue", 
                  command=lambda: self.apply_preset("blue")).grid(row=0, column=0, padx=2)
        ttk.Button(preset_frame, text="Forest Green", 
                  command=lambda: self.apply_preset("green")).grid(row=0, column=1, padx=2)
        ttk.Button(preset_frame, text="Sunset Orange", 
                  command=lambda: self.apply_preset("orange")).grid(row=0, column=2, padx=2)
        ttk.Button(preset_frame, text="Deep Purple", 
                  command=lambda: self.apply_preset("purple")).grid(row=1, column=0, padx=2, pady=2)
        ttk.Button(preset_frame, text="Dark Mode", 
                  command=lambda: self.apply_preset("dark")).grid(row=1, column=1, padx=2, pady=2)
        
        # Right panel - Preview
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Preview canvas
        self.preview_canvas = tk.Canvas(preview_frame, width=400, height=400, 
                                       bg="white", relief="sunken", bd=2)
        self.preview_canvas.grid(row=0, column=0, padx=20, pady=20)
        
        # Size info
        self.size_info_label = ttk.Label(preview_frame, text="Size: 256x256 pixels")
        self.size_info_label.grid(row=1, column=0, pady=10)
    
    def choose_color(self, color_type):
        """Open color chooser dialog"""
        color = colorchooser.askcolor(title="Choose Color")[1]
        if color:
            setattr(self, color_type, color)
            
            # Update button color
            if color_type == 'bg_color':
                self.bg_color_btn.config(bg=color)
            elif color_type == 'folder_color':
                self.folder_color_btn.config(bg=color)
            elif color_type == 'pulse_color':
                self.pulse_color_btn.config(bg=color)
            
            self.generate_preview()
    
    def on_size_change(self, event=None):
        """Handle size change"""
        self.icon_size = int(self.size_var.get())
        self.size_info_label.config(text=f"Size: {self.icon_size}x{self.icon_size} pixels")
        self.generate_preview()
    
    def on_style_change(self, event=None):
        """Handle style change"""
        self.generate_preview()
    
    def on_text_change(self, event=None):
        """Handle text change"""
        self.generate_preview()
    
    def toggle_custom_image(self):
        """Toggle custom image usage"""
        self.use_custom_image = self.use_custom_var.get()
        
        # Enable/disable custom image controls
        state = "normal" if self.use_custom_image else "disabled"
        self.load_image_btn.config(state=state)
        self.opacity_scale.config(state=state)
        self.scale_scale.config(state=state)
        
        self.generate_preview()
    
    def load_custom_image(self):
        """Load a custom image"""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Load and validate image
                self.custom_image = Image.open(file_path)
                
                # Convert to RGBA if needed
                if self.custom_image.mode != 'RGBA':
                    self.custom_image = self.custom_image.convert('RGBA')
                
                # Update info label
                filename = os.path.basename(file_path)
                size = self.custom_image.size
                self.image_info_label.config(
                    text=f"{filename} ({size[0]}x{size[1]})", 
                    foreground="black"
                )
                
                self.generate_preview()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
                self.custom_image = None
                self.image_info_label.config(text="No image loaded", foreground="gray")
    
    def on_opacity_change(self, value):
        """Handle opacity change"""
        self.custom_image_opacity = int(float(value))
        self.generate_preview()
    
    def on_scale_change(self, value):
        """Handle scale change"""
        self.custom_image_scale = int(float(value))
        self.generate_preview()
    
    def apply_preset(self, preset_name):
        """Apply a color preset"""
        presets = {
            "blue": {"bg": "#3498db", "folder": "#2980b9", "pulse": "#e74c3c"},
            "green": {"bg": "#27ae60", "folder": "#229954", "pulse": "#f39c12"},
            "orange": {"bg": "#e67e22", "folder": "#d35400", "pulse": "#e74c3c"},
            "purple": {"bg": "#8e44ad", "folder": "#732d91", "pulse": "#f1948a"},
            "dark": {"bg": "#2c3e50", "folder": "#34495e", "pulse": "#3498db"}
        }
        
        if preset_name in presets:
            preset = presets[preset_name]
            self.bg_color = preset["bg"]
            self.folder_color = preset["folder"]
            self.pulse_color = preset["pulse"]
            
            # Update button colors
            self.bg_color_btn.config(bg=self.bg_color)
            self.folder_color_btn.config(bg=self.folder_color)  
            self.pulse_color_btn.config(bg=self.pulse_color)
            
            self.generate_preview()
    
    def generate_preview(self):
        """Generate and display icon preview"""
        try:
            # Create the icon
            icon = self.create_icon()
            
            # Resize for preview (max 300x300)
            preview_size = min(300, self.icon_size)
            if self.icon_size > preview_size:
                icon = icon.resize((preview_size, preview_size), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage for display
            self.preview_image = ImageTk.PhotoImage(icon)
            
            # Clear canvas and display
            self.preview_canvas.delete("all")
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:  # Canvas is initialized
                x = canvas_width // 2
                y = canvas_height // 2
                self.preview_canvas.create_image(x, y, image=self.preview_image)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate preview: {e}")
    
    def create_icon(self):
        """Create the actual icon"""
        # Create image
        img = Image.new('RGBA', (self.icon_size, self.icon_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # If using custom image as background/base
        if self.use_custom_image and self.custom_image:
            self.apply_custom_image(img)
        else:
            # Draw standard icon styles
            style = self.style_var.get()
            center = self.icon_size // 2
            
            if style == "Modern":
                self.draw_modern_icon(draw, center)
            elif style == "Classic":
                self.draw_classic_icon(draw, center)
            elif style == "Minimal":
                self.draw_minimal_icon(draw, center)
            elif style == "3D":
                self.draw_3d_icon(draw, center)
        
        # Add text overlay if specified
        text = self.text_var.get().strip()
        if text:
            self.add_text_overlay(img, text)
        
        return img
    
    def apply_custom_image(self, base_img):
        """Apply custom image to the base image"""
        if not self.custom_image:
            return
        
        # Calculate scaled size
        scale = self.custom_image_scale / 100.0
        new_size = int(self.icon_size * scale)
        
        # Resize custom image
        custom_resized = self.custom_image.resize((new_size, new_size), Image.Resampling.LANCZOS)
        
        # Apply opacity
        if self.custom_image_opacity < 100:
            alpha = int(255 * (self.custom_image_opacity / 100.0))
            # Create alpha mask
            if custom_resized.mode != 'RGBA':
                custom_resized = custom_resized.convert('RGBA')
            
            # Apply opacity to alpha channel
            r, g, b, a = custom_resized.split()
            a = a.point(lambda x: min(x, alpha))
            custom_resized = Image.merge('RGBA', (r, g, b, a))
        
        # Center the image
        x = (self.icon_size - new_size) // 2
        y = (self.icon_size - new_size) // 2
        
        # Paste onto base image
        base_img.paste(custom_resized, (x, y), custom_resized)
    
    def add_text_overlay(self, img, text):
        """Add text overlay to the image"""
        draw = ImageDraw.Draw(img)
        
        # Try to load a font
        try:
            font_size = max(12, self.icon_size // 8)
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center text
        x = (self.icon_size - text_width) // 2
        y = (self.icon_size - text_height) // 2
        
        # Draw text with outline for better visibility
        outline_color = "#000000" if self.text_color == "#ffffff" else "#ffffff"
        
        # Draw outline
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
        
        # Draw main text
        draw.text((x, y), text, font=font, fill=self.text_color)
    
    def draw_modern_icon(self, draw, center):
        """Draw modern style icon"""
        size = self.icon_size
        
        # Background circle with gradient effect
        for i in range(20):
            alpha = 255 - i * 10
            radius = center - i * 2
            if radius > 0:
                color = self.hex_to_rgba(self.bg_color, alpha)
                draw.ellipse([center-radius, center-radius, center+radius, center+radius], 
                           fill=color)
        
        # Main folder
        folder_size = size // 4
        folder_x = center - folder_size
        folder_y = center - folder_size // 2
        
        # Folder body
        draw.rectangle([folder_x, folder_y, folder_x + folder_size*2, folder_y + folder_size*1.5],
                      fill=self.folder_color)
        
        # Folder tab
        tab_width = folder_size // 2
        draw.rectangle([folder_x, folder_y - folder_size//4, folder_x + tab_width, folder_y],
                      fill=self.folder_color)
        
        # Pulse rings
        for i, radius in enumerate([size//6, size//4, size//3]):
            alpha = 100 - i * 30
            color = self.hex_to_rgba(self.pulse_color, alpha)
            draw.ellipse([center-radius, center-radius, center+radius, center+radius],
                        outline=color, width=3)
        
        # Add text if specified
        text = self.text_var.get().strip()
        if text:
            self.draw_text(draw, center, text)
    
    def draw_classic_icon(self, draw, center):
        """Draw classic style icon"""
        size = self.icon_size
        
        # Simple background
        draw.ellipse([5, 5, size-5, size-5], fill=self.bg_color)
        
        # Folder
        folder_size = size // 3
        folder_x = center - folder_size
        folder_y = center - folder_size // 2
        
        draw.rectangle([folder_x, folder_y, folder_x + folder_size*2, folder_y + folder_size],
                      fill=self.folder_color, outline="#34495e", width=2)
        
        # Simple pulse dot
        dot_radius = size // 20
        draw.ellipse([center-dot_radius, center-dot_radius, center+dot_radius, center+dot_radius],
                    fill=self.pulse_color)
    
    def draw_minimal_icon(self, draw, center):
        """Draw minimal style icon"""
        size = self.icon_size
        
        # Simple shapes
        line_width = max(2, size // 64)
        
        # Folder outline
        folder_size = size // 3
        folder_x = center - folder_size
        folder_y = center - folder_size // 2
        
        draw.rectangle([folder_x, folder_y, folder_x + folder_size*2, folder_y + folder_size],
                      outline=self.folder_color, width=line_width)
        
        # Minimal pulse
        pulse_radius = size // 8
        draw.circle([center, center], pulse_radius, outline=self.pulse_color, width=line_width)
    
    def draw_3d_icon(self, draw, center):
        """Draw 3D style icon"""
        size = self.icon_size
        
        # 3D background with shadow
        shadow_offset = size // 32
        draw.ellipse([shadow_offset, shadow_offset, size-5+shadow_offset, size-5+shadow_offset], 
                    fill="#95a5a6")
        draw.ellipse([5, 5, size-5, size-5], fill=self.bg_color)
        
        # 3D folder
        folder_size = size // 4
        folder_x = center - folder_size
        folder_y = center - folder_size // 2
        
        # Folder shadow
        shadow_x = folder_x + shadow_offset
        shadow_y = folder_y + shadow_offset
        draw.rectangle([shadow_x, shadow_y, shadow_x + folder_size*2, shadow_y + folder_size*1.5],
                      fill="#7f8c8d")
        
        # Folder body with highlights
        draw.rectangle([folder_x, folder_y, folder_x + folder_size*2, folder_y + folder_size*1.5],
                      fill=self.folder_color)
        
        # Highlight
        highlight_color = self.lighten_color(self.folder_color, 40)
        draw.rectangle([folder_x, folder_y, folder_x + folder_size*2, folder_y + folder_size//4],
                      fill=highlight_color)
    
    def draw_text(self, draw, center, text):
        """Draw text overlay on icon"""
        try:
            # Try to use a nice font
            font_size = max(12, self.icon_size // 8)
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Get text size
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Position text at bottom
            text_x = center - text_width // 2
            text_y = center + self.icon_size // 4
            
            # Draw text shadow
            draw.text((text_x + 1, text_y + 1), text, fill="#000000", font=font)
            # Draw text
            draw.text((text_x, text_y), text, fill=self.text_color, font=font)
            
        except Exception:
            pass  # Ignore font errors
    
    def hex_to_rgba(self, hex_color, alpha=255):
        """Convert hex color to RGBA tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) + (alpha,)
    
    def lighten_color(self, hex_color, amount):
        """Lighten a hex color by amount"""
        hex_color = hex_color.lstrip('#')
        rgb = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
        rgb = [min(255, c + amount) for c in rgb]
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def export_icon(self):
        """Export the icon to files"""
        try:
            # Default to assets/icons directory
            assets_dir = Path(__file__).parent.parent / "assets" / "icons"
            assets_dir.mkdir(parents=True, exist_ok=True)
            
            # Ask for save location
            filename = filedialog.asksaveasfilename(
                title="Save Icon As",
                initialdir=str(assets_dir),
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("ICO files", "*.ico"),
                    ("All files", "*.*")
                ]
            )
            
            if filename:
                # Create the icon
                icon = self.create_icon()
                
                if filename.lower().endswith('.ico'):
                    # Save as ICO with multiple sizes
                    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
                    icon_images = []
                    
                    for size in sizes:
                        if size[0] <= self.icon_size:
                            resized = icon.resize(size, Image.Resampling.LANCZOS)
                            icon_images.append(resized)
                    
                    # Save ICO file
                    icon_images[0].save(filename, format='ICO', sizes=[(img.size[0], img.size[1]) for img in icon_images])
                    
                    # Also save individual PNG sizes
                    base_name = filename.rsplit('.', 1)[0]
                    for size in [(16, 16), (32, 32), (48, 48), (64, 64)]:
                        if size[0] <= self.icon_size:
                            resized = icon.resize(size, Image.Resampling.LANCZOS)
                            size_filename = f"{base_name}-{size[0]}x{size[1]}.png"
                            resized.save(size_filename, format='PNG')
                else:
                    # Save as PNG
                    icon.save(filename, format='PNG')
                    
                    # Also save style variant
                    base_name = filename.rsplit('.', 1)[0]
                    style = self.style_var.get().lower()
                    style_filename = f"{base_name}-{style}.png"
                    if style_filename != filename:
                        icon.save(style_filename, format='PNG')
                
                messagebox.showinfo("Success", f"Icon saved as {filename}\nAdditional formats saved to assets/icons/")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export icon: {e}")
    
    def load_preset(self):
        """Load preset from file"""
        # Default to assets/presets directory
        assets_dir = Path(__file__).parent.parent / "assets" / "presets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        
        filename = filedialog.askopenfilename(
            title="Load Preset",
            initialdir=str(assets_dir),
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                import json
                with open(filename, 'r') as f:
                    preset = json.load(f)
                
                # Apply preset settings
                self.bg_color = preset.get('bg_color', self.bg_color)
                self.folder_color = preset.get('folder_color', self.folder_color)
                self.pulse_color = preset.get('pulse_color', self.pulse_color)
                self.text_var.set(preset.get('text', self.text_var.get()))
                self.style_var.set(preset.get('style', self.style_var.get()))
                self.size_var.set(str(preset.get('size', self.icon_size)))
                
                # Update UI
                self.bg_color_btn.config(bg=self.bg_color)
                self.folder_color_btn.config(bg=self.folder_color)
                self.pulse_color_btn.config(bg=self.pulse_color)
                
                self.on_size_change()
                self.generate_preview()
                
                messagebox.showinfo("Success", "Preset loaded successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load preset: {e}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = IconGenerator(root)
    
    # Generate initial preview after a short delay
    root.after(100, app.generate_preview)
    
    root.mainloop()


if __name__ == "__main__":
    main()
