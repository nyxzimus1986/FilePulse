#!/usr/bin/env python3
"""
FilePulse Splash Screen Generator
Creates custom splash screens for the FilePulse application
"""

import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox, font
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageFilter
import os
import json
from pathlib import Path

class SplashScreenGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("FilePulse Splash Screen Generator")
        self.root.geometry("1000x700")
        
        # Splash screen settings
        self.width = 600
        self.height = 400
        self.bg_gradient_start = "#2c3e50"
        self.bg_gradient_end = "#3498db"
        self.logo_color = "#ffffff"
        self.title_color = "#ffffff"
        self.subtitle_color = "#bdc3c7"
        self.progress_color = "#3498db"
        self.progress_bg_color = "#34495e"
        
        # Text settings
        self.title_text = "FilePulse"
        self.subtitle_text = "Real-time Filesystem Monitor"
        self.loading_text = "Loading..."
        
        # Animation settings
        self.enable_animations = True
        self.animation_style = "Pulse"
        self.show_progress_bar = True
        self.show_logo = True
        
        # Custom background image settings
        self.custom_bg_image = None
        self.use_custom_bg = False
        self.bg_image_opacity = 50
        self.bg_image_blur = 0
        self.bg_image_scale = 100
        
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
        main_frame.rowconfigure(0, weight=1)
        
        # Left panel - Controls
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Create notebook for organized settings
        notebook = ttk.Notebook(controls_frame)
        notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Size & Layout Tab
        layout_frame = ttk.Frame(notebook, padding="10")
        notebook.add(layout_frame, text="Size & Layout")
        
        # Dimensions
        ttk.Label(layout_frame, text="Width:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.width_var = tk.StringVar(value=str(self.width))
        ttk.Entry(layout_frame, textvariable=self.width_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        ttk.Label(layout_frame, text="Height:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.height_var = tk.StringVar(value=str(self.height))
        ttk.Entry(layout_frame, textvariable=self.height_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Quick size presets
        ttk.Label(layout_frame, text="Quick Sizes:").grid(row=2, column=0, sticky=tk.W, pady=5)
        size_frame = ttk.Frame(layout_frame)
        size_frame.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        ttk.Button(size_frame, text="400x300", width=8,
                  command=lambda: self.set_size(400, 300)).grid(row=0, column=0, padx=2)
        ttk.Button(size_frame, text="600x400", width=8,
                  command=lambda: self.set_size(600, 400)).grid(row=0, column=1, padx=2)
        ttk.Button(size_frame, text="800x600", width=8,
                  command=lambda: self.set_size(800, 600)).grid(row=0, column=2, padx=2)
        
        # Layout options
        self.show_logo_var = tk.BooleanVar(value=self.show_logo)
        ttk.Checkbutton(layout_frame, text="Show Logo", variable=self.show_logo_var,
                       command=self.on_setting_change).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        self.show_progress_var = tk.BooleanVar(value=self.show_progress_bar)
        ttk.Checkbutton(layout_frame, text="Show Progress Bar", variable=self.show_progress_var,
                       command=self.on_setting_change).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Colors Tab
        colors_frame = ttk.Frame(notebook, padding="10")
        notebook.add(colors_frame, text="Colors")
        
        # Background gradient
        ttk.Label(colors_frame, text="Background Start:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.bg_start_btn = tk.Button(colors_frame, text="Choose", width=10,
                                     command=lambda: self.choose_color('bg_gradient_start'),
                                     bg=self.bg_gradient_start)
        self.bg_start_btn.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        ttk.Label(colors_frame, text="Background End:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.bg_end_btn = tk.Button(colors_frame, text="Choose", width=10,
                                   command=lambda: self.choose_color('bg_gradient_end'),
                                   bg=self.bg_gradient_end)
        self.bg_end_btn.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Text colors
        ttk.Label(colors_frame, text="Title Color:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.title_color_btn = tk.Button(colors_frame, text="Choose", width=10,
                                        command=lambda: self.choose_color('title_color'),
                                        bg=self.title_color)
        self.title_color_btn.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        ttk.Label(colors_frame, text="Subtitle Color:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.subtitle_color_btn = tk.Button(colors_frame, text="Choose", width=10,
                                           command=lambda: self.choose_color('subtitle_color'),
                                           bg=self.subtitle_color)
        self.subtitle_color_btn.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        ttk.Label(colors_frame, text="Logo Color:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.logo_color_btn = tk.Button(colors_frame, text="Choose", width=10,
                                       command=lambda: self.choose_color('logo_color'),
                                       bg=self.logo_color)
        self.logo_color_btn.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Progress bar colors
        ttk.Label(colors_frame, text="Progress Color:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.progress_color_btn = tk.Button(colors_frame, text="Choose", width=10,
                                           command=lambda: self.choose_color('progress_color'),
                                           bg=self.progress_color)
        self.progress_color_btn.grid(row=5, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Color presets
        ttk.Label(colors_frame, text="Color Themes:").grid(row=6, column=0, sticky=tk.W, pady=(15, 5))
        theme_frame = ttk.Frame(colors_frame)
        theme_frame.grid(row=6, column=1, sticky=tk.W, padx=(10, 0), pady=(15, 5))
        
        ttk.Button(theme_frame, text="Blue", width=8,
                  command=lambda: self.apply_theme("blue")).grid(row=0, column=0, padx=2)
        ttk.Button(theme_frame, text="Dark", width=8,
                  command=lambda: self.apply_theme("dark")).grid(row=0, column=1, padx=2)
        ttk.Button(theme_frame, text="Green", width=8,
                  command=lambda: self.apply_theme("green")).grid(row=1, column=0, padx=2, pady=2)
        ttk.Button(theme_frame, text="Purple", width=8,
                  command=lambda: self.apply_theme("purple")).grid(row=1, column=1, padx=2, pady=2)
        
        # Text Tab
        text_frame = ttk.Frame(notebook, padding="10")
        notebook.add(text_frame, text="Text")
        
        # Title text
        ttk.Label(text_frame, text="Title:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_var = tk.StringVar(value=self.title_text)
        ttk.Entry(text_frame, textvariable=self.title_var, width=20).grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        self.title_var.trace('w', lambda *args: self.on_setting_change())
        
        # Subtitle text
        ttk.Label(text_frame, text="Subtitle:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.subtitle_var = tk.StringVar(value=self.subtitle_text)
        ttk.Entry(text_frame, textvariable=self.subtitle_var, width=20).grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        self.subtitle_var.trace('w', lambda *args: self.on_setting_change())
        
        # Loading text
        ttk.Label(text_frame, text="Loading Text:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.loading_var = tk.StringVar(value=self.loading_text)
        ttk.Entry(text_frame, textvariable=self.loading_var, width=20).grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        self.loading_var.trace('w', lambda *args: self.on_setting_change())
        
        # Animation Tab
        animation_frame = ttk.Frame(notebook, padding="10")
        notebook.add(animation_frame, text="Animation")
        
        # Enable animations
        self.enable_animations_var = tk.BooleanVar(value=self.enable_animations)
        ttk.Checkbutton(animation_frame, text="Enable Animations", variable=self.enable_animations_var,
                       command=self.on_setting_change).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Animation style
        ttk.Label(animation_frame, text="Animation Style:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.animation_var = tk.StringVar(value=self.animation_style)
        animation_combo = ttk.Combobox(animation_frame, textvariable=self.animation_var,
                                      values=["Pulse", "Fade", "Slide", "Rotate", "Scale"],
                                      width=15)
        animation_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        animation_combo.bind('<<ComboboxSelected>>', self.on_setting_change)
        
        # Background Image Tab
        bg_image_frame = ttk.Frame(notebook, padding="10")
        notebook.add(bg_image_frame, text="Background Image")
        
        # Use custom background image
        self.use_custom_bg_var = tk.BooleanVar(value=self.use_custom_bg)
        ttk.Checkbutton(bg_image_frame, text="Use Custom Background Image", 
                       variable=self.use_custom_bg_var,
                       command=self.toggle_custom_bg).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Load image button
        self.load_bg_btn = ttk.Button(bg_image_frame, text="Load Background Image", 
                                     command=self.load_background_image,
                                     state="disabled")
        self.load_bg_btn.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Image info label
        self.bg_image_info_label = ttk.Label(bg_image_frame, text="No background image loaded", 
                                            foreground="gray")
        self.bg_image_info_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Opacity slider
        ttk.Label(bg_image_frame, text="Image Opacity:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.bg_opacity_var = tk.IntVar(value=self.bg_image_opacity)
        self.bg_opacity_scale = ttk.Scale(bg_image_frame, from_=0, to=100, 
                                         variable=self.bg_opacity_var,
                                         command=self.on_bg_opacity_change,
                                         state="disabled")
        self.bg_opacity_scale.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Blur slider
        ttk.Label(bg_image_frame, text="Image Blur:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.bg_blur_var = tk.IntVar(value=self.bg_image_blur)
        self.bg_blur_scale = ttk.Scale(bg_image_frame, from_=0, to=20, 
                                      variable=self.bg_blur_var,
                                      command=self.on_bg_blur_change,
                                      state="disabled")
        self.bg_blur_scale.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Scale slider
        ttk.Label(bg_image_frame, text="Image Scale:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.bg_scale_var = tk.IntVar(value=self.bg_image_scale)
        self.bg_scale_scale = ttk.Scale(bg_image_frame, from_=50, to=200, 
                                       variable=self.bg_scale_var,
                                       command=self.on_bg_scale_change,
                                       state="disabled")
        self.bg_scale_scale.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        
        bg_image_frame.columnconfigure(1, weight=1)
        
        # Control buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.grid(row=1, column=0, pady=20)
        
        ttk.Button(button_frame, text="Generate Preview", 
                  command=self.generate_preview).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Export Splash", 
                  command=self.export_splash).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Save Preset", 
                  command=self.save_preset).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Load Preset", 
                  command=self.load_preset).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Generate Code", 
                  command=self.generate_code).grid(row=1, column=1, padx=5, pady=5)
        
        # Right panel - Preview
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Preview canvas
        self.preview_canvas = tk.Canvas(preview_frame, width=600, height=400, 
                                       bg="white", relief="sunken", bd=2)
        self.preview_canvas.grid(row=0, column=0, padx=20, pady=20)
        
        # Preview controls
        preview_controls = ttk.Frame(preview_frame)
        preview_controls.grid(row=1, column=0, pady=10)
        
        ttk.Button(preview_controls, text="Animate Preview", 
                  command=self.animate_preview).grid(row=0, column=0, padx=5)
        
        # Dimensions info
        self.dims_label = ttk.Label(preview_frame, text=f"Size: {self.width}x{self.height}")
        self.dims_label.grid(row=2, column=0, pady=5)
    
    def choose_color(self, color_type):
        """Open color chooser dialog"""
        color = colorchooser.askcolor(title="Choose Color")[1]
        if color:
            setattr(self, color_type, color)
            
            # Update button color
            if hasattr(self, f"{color_type.replace('_', '_')}_btn"):
                btn = getattr(self, f"{color_type.replace('_', '_')}_btn")
                btn.config(bg=color)
            
            self.generate_preview()
    
    def set_size(self, width, height):
        """Set splash screen size"""
        self.width_var.set(str(width))
        self.height_var.set(str(height))
        self.width = width
        self.height = height
        self.dims_label.config(text=f"Size: {width}x{height}")
        self.generate_preview()
    
    def on_setting_change(self, *args):
        """Handle setting changes"""
        # Update variables
        try:
            self.width = int(self.width_var.get())
            self.height = int(self.height_var.get())
        except ValueError:
            pass
        
        self.title_text = self.title_var.get()
        self.subtitle_text = self.subtitle_var.get()
        self.loading_text = self.loading_var.get()
        self.show_logo = self.show_logo_var.get()
        self.show_progress_bar = self.show_progress_var.get()
        self.enable_animations = self.enable_animations_var.get()
        self.animation_style = self.animation_var.get()
        
        self.dims_label.config(text=f"Size: {self.width}x{self.height}")
        self.generate_preview()
    
    def toggle_custom_bg(self):
        """Toggle custom background image usage"""
        self.use_custom_bg = self.use_custom_bg_var.get()
        
        # Enable/disable custom background controls
        state = "normal" if self.use_custom_bg else "disabled"
        self.load_bg_btn.config(state=state)
        self.bg_opacity_scale.config(state=state)
        self.bg_blur_scale.config(state=state)
        self.bg_scale_scale.config(state=state)
        
        self.generate_preview()
    
    def load_background_image(self):
        """Load a custom background image"""
        file_path = filedialog.askopenfilename(
            title="Select Background Image",
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
                self.custom_bg_image = Image.open(file_path)
                
                # Convert to RGB if needed
                if self.custom_bg_image.mode not in ['RGB', 'RGBA']:
                    self.custom_bg_image = self.custom_bg_image.convert('RGB')
                
                # Update info label
                filename = os.path.basename(file_path)
                size = self.custom_bg_image.size
                self.bg_image_info_label.config(
                    text=f"{filename} ({size[0]}x{size[1]})", 
                    foreground="black"
                )
                
                self.generate_preview()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load background image:\n{str(e)}")
                self.custom_bg_image = None
                self.bg_image_info_label.config(text="No background image loaded", foreground="gray")
    
    def on_bg_opacity_change(self, value):
        """Handle background opacity change"""
        self.bg_image_opacity = int(float(value))
        self.generate_preview()
    
    def on_bg_blur_change(self, value):
        """Handle background blur change"""
        self.bg_image_blur = int(float(value))
        self.generate_preview()
    
    def on_bg_scale_change(self, value):
        """Handle background scale change"""
        self.bg_image_scale = int(float(value))
        self.generate_preview()
    
    def apply_theme(self, theme_name):
        """Apply a color theme"""
        themes = {
            "blue": {
                "bg_start": "#2c3e50", "bg_end": "#3498db",
                "title": "#ffffff", "subtitle": "#bdc3c7",
                "logo": "#ffffff", "progress": "#3498db"
            },
            "dark": {
                "bg_start": "#1a1a1a", "bg_end": "#2d3748",
                "title": "#ffffff", "subtitle": "#a0aec0",
                "logo": "#63b3ed", "progress": "#63b3ed"
            },
            "green": {
                "bg_start": "#1e3a2e", "bg_end": "#27ae60",
                "title": "#ffffff", "subtitle": "#a9dfbf",
                "logo": "#ffffff", "progress": "#2ecc71"
            },
            "purple": {
                "bg_start": "#2c1810", "bg_end": "#8e44ad",
                "title": "#ffffff", "subtitle": "#d7bde2",
                "logo": "#ffffff", "progress": "#9b59b6"
            }
        }
        
        if theme_name in themes:
            theme = themes[theme_name]
            self.bg_gradient_start = theme["bg_start"]
            self.bg_gradient_end = theme["bg_end"]
            self.title_color = theme["title"]
            self.subtitle_color = theme["subtitle"]
            self.logo_color = theme["logo"]
            self.progress_color = theme["progress"]
            
            # Update button colors
            self.bg_start_btn.config(bg=self.bg_gradient_start)
            self.bg_end_btn.config(bg=self.bg_gradient_end)
            self.title_color_btn.config(bg=self.title_color)
            self.subtitle_color_btn.config(bg=self.subtitle_color)
            self.logo_color_btn.config(bg=self.logo_color)
            self.progress_color_btn.config(bg=self.progress_color)
            
            self.generate_preview()
    
    def generate_preview(self):
        """Generate and display splash screen preview"""
        try:
            # Create the splash screen
            splash = self.create_splash_screen()
            
            # Resize for preview if needed
            canvas_width = 600
            canvas_height = 400
            
            if self.width > canvas_width or self.height > canvas_height:
                # Calculate scale factor
                scale_x = canvas_width / self.width
                scale_y = canvas_height / self.height
                scale = min(scale_x, scale_y)
                
                new_width = int(self.width * scale)
                new_height = int(self.height * scale)
                
                splash = splash.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            self.preview_image = ImageTk.PhotoImage(splash)
            
            # Display on canvas
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(canvas_width//2, canvas_height//2, image=self.preview_image)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate preview: {e}")
    
    def create_splash_screen(self):
        """Create the splash screen image"""
        # Create image
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)
        
        # Apply custom background image or gradient
        if self.use_custom_bg and self.custom_bg_image:
            self.apply_custom_background(img, draw)
        else:
            # Draw gradient background
            self.draw_gradient_background(img, draw)
        
        # Draw logo if enabled
        if self.show_logo:
            self.draw_logo(draw)
        
        # Draw text
        self.draw_text(draw)
        
        # Draw progress bar if enabled
        if self.show_progress_bar:
            self.draw_progress_bar(draw, progress=0.6)  # 60% for preview
        
        return img
    
    def apply_custom_background(self, img, draw):
        """Apply custom background image"""
        if not self.custom_bg_image:
            return
        
        # Calculate scaled size
        scale = self.bg_image_scale / 100.0
        orig_width, orig_height = self.custom_bg_image.size
        
        # Scale while maintaining aspect ratio or fill the screen
        width_scale = (self.width * scale) / orig_width
        height_scale = (self.height * scale) / orig_height
        
        # Use the larger scale to fill the background
        scale_factor = max(width_scale, height_scale)
        new_width = int(orig_width * scale_factor)
        new_height = int(orig_height * scale_factor)
        
        # Resize the background image
        bg_resized = self.custom_bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Apply blur if specified
        if self.bg_image_blur > 0:
            bg_resized = bg_resized.filter(ImageFilter.GaussianBlur(radius=self.bg_image_blur))
        
        # Center the image
        x = (self.width - new_width) // 2
        y = (self.height - new_height) // 2
        
        # Create a temporary image for blending
        temp_img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        
        # Crop if image is larger than canvas
        if new_width > self.width or new_height > self.height:
            crop_x = max(0, (new_width - self.width) // 2)
            crop_y = max(0, (new_height - self.height) // 2)
            crop_width = min(self.width, new_width)
            crop_height = min(self.height, new_height)
            
            bg_resized = bg_resized.crop((crop_x, crop_y, crop_x + crop_width, crop_y + crop_height))
            x = max(0, x)
            y = max(0, y)
        
        # Paste background image
        if bg_resized.mode == 'RGBA':
            temp_img.paste(bg_resized, (x, y), bg_resized)
        else:
            temp_img.paste(bg_resized, (x, y))
        
        # Apply opacity by blending with gradient background
        if self.bg_image_opacity < 100:
            # Create gradient background
            gradient_img = Image.new('RGB', (self.width, self.height))
            gradient_draw = ImageDraw.Draw(gradient_img)
            self.draw_gradient_background(gradient_img, gradient_draw)
            
            # Blend images
            alpha = self.bg_image_opacity / 100.0
            img.paste(Image.blend(gradient_img, temp_img, alpha))
        else:
            img.paste(temp_img)
    
    def draw_gradient_background(self, img, draw):
        """Draw gradient background"""
        # Simple vertical gradient
        start_color = self.hex_to_rgb(self.bg_gradient_start)
        end_color = self.hex_to_rgb(self.bg_gradient_end)
        
        for y in range(self.height):
            # Calculate color interpolation
            ratio = y / self.height
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
    
    def draw_logo(self, draw):
        """Draw the FilePulse logo"""
        center_x = self.width // 2
        logo_y = self.height // 3
        logo_size = min(80, self.width // 8)
        
        # Draw folder icon
        folder_width = logo_size
        folder_height = logo_size // 2
        folder_x = center_x - folder_width // 2
        folder_y = logo_y - folder_height // 2
        
        # Folder body
        draw.rectangle([folder_x, folder_y, folder_x + folder_width, folder_y + folder_height],
                      fill=self.logo_color, outline=self.logo_color)
        
        # Folder tab
        tab_width = folder_width // 3
        draw.rectangle([folder_x, folder_y - folder_height//3, folder_x + tab_width, folder_y],
                      fill=self.logo_color, outline=self.logo_color)
        
        # Pulse rings around logo
        pulse_color = self.logo_color
        if pulse_color == "#ffffff":
            # Make pulse visible on white
            pulse_color = self.hex_to_rgb(self.progress_color)
            pulse_color = f"#{pulse_color[0]:02x}{pulse_color[1]:02x}{pulse_color[2]:02x}"
        
        for i, radius in enumerate([logo_size//2 + 10, logo_size//2 + 20, logo_size//2 + 30]):
            alpha = 150 - i * 50
            # Draw pulse ring (simplified as circle outline)
            draw.ellipse([center_x - radius, logo_y - radius, center_x + radius, logo_y + radius],
                        outline=pulse_color, width=2)
    
    def draw_text(self, draw):
        """Draw title and subtitle text"""
        center_x = self.width // 2
        
        try:
            # Try to get fonts
            title_size = max(24, self.width // 20)
            subtitle_size = max(14, self.width // 40)
            loading_size = max(12, self.width // 50)
            
            try:
                title_font = ImageFont.truetype("arial.ttf", title_size)
                subtitle_font = ImageFont.truetype("arial.ttf", subtitle_size)
                loading_font = ImageFont.truetype("arial.ttf", loading_size)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                loading_font = ImageFont.load_default()
            
            # Title
            title_y = self.height // 2
            title_bbox = draw.textbbox((0, 0), self.title_text, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            draw.text((center_x - title_width//2, title_y), self.title_text, 
                     fill=self.title_color, font=title_font)
            
            # Subtitle
            subtitle_y = title_y + 40
            subtitle_bbox = draw.textbbox((0, 0), self.subtitle_text, font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            draw.text((center_x - subtitle_width//2, subtitle_y), self.subtitle_text,
                     fill=self.subtitle_color, font=subtitle_font)
            
            # Loading text
            loading_y = self.height - 60
            loading_bbox = draw.textbbox((0, 0), self.loading_text, font=loading_font)
            loading_width = loading_bbox[2] - loading_bbox[0]
            draw.text((center_x - loading_width//2, loading_y), self.loading_text,
                     fill=self.subtitle_color, font=loading_font)
            
        except Exception:
            # Fallback text drawing
            draw.text((center_x - 50, self.height//2), self.title_text, fill=self.title_color)
            draw.text((center_x - 80, self.height//2 + 30), self.subtitle_text, fill=self.subtitle_color)
    
    def draw_progress_bar(self, draw, progress=0.0):
        """Draw progress bar"""
        bar_width = self.width // 2
        bar_height = 6
        bar_x = (self.width - bar_width) // 2
        bar_y = self.height - 40
        
        # Background
        draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height],
                      fill=self.progress_bg_color)
        
        # Progress
        progress_width = int(bar_width * progress)
        if progress_width > 0:
            draw.rectangle([bar_x, bar_y, bar_x + progress_width, bar_y + bar_height],
                          fill=self.progress_color)
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def animate_preview(self):
        """Show animated preview"""
        if not self.enable_animations:
            messagebox.showinfo("Info", "Animations are disabled")
            return
        
        # Simple animation simulation
        for progress in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
            splash = self.create_splash_screen()
            draw = ImageDraw.Draw(splash)
            
            if self.show_progress_bar:
                self.draw_progress_bar(draw, progress)
            
            # Show current frame
            if self.width > 600 or self.height > 400:
                scale_x = 600 / self.width
                scale_y = 400 / self.height
                scale = min(scale_x, scale_y)
                new_width = int(self.width * scale)
                new_height = int(self.height * scale)
                splash = splash.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            self.preview_image = ImageTk.PhotoImage(splash)
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(300, 200, image=self.preview_image)
            self.root.update()
            
            # Delay
            self.root.after(300)
    
    def save_preset(self):
        """Save current settings as preset"""
        # Default to assets/presets directory
        assets_dir = Path(__file__).parent.parent / "assets" / "presets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        
        filename = filedialog.asksaveasfilename(
            title="Save Preset",
            initialdir=str(assets_dir),
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                preset = {
                    'width': self.width,
                    'height': self.height,
                    'bg_gradient_start': self.bg_gradient_start,
                    'bg_gradient_end': self.bg_gradient_end,
                    'logo_color': self.logo_color,
                    'title_color': self.title_color,
                    'subtitle_color': self.subtitle_color,
                    'progress_color': self.progress_color,
                    'progress_bg_color': self.progress_bg_color,
                    'title_text': self.title_text,
                    'subtitle_text': self.subtitle_text,
                    'loading_text': self.loading_text,
                    'enable_animations': self.enable_animations,
                    'animation_style': self.animation_style,
                    'show_progress_bar': self.show_progress_bar,
                    'show_logo': self.show_logo
                }
                
                with open(filename, 'w') as f:
                    json.dump(preset, f, indent=2)
                
                messagebox.showinfo("Success", f"Preset saved as {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save preset: {e}")
    
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
                with open(filename, 'r') as f:
                    preset = json.load(f)
                
                # Apply settings
                self.width = preset.get('width', self.width)
                self.height = preset.get('height', self.height)
                self.bg_gradient_start = preset.get('bg_gradient_start', self.bg_gradient_start)
                self.bg_gradient_end = preset.get('bg_gradient_end', self.bg_gradient_end)
                self.logo_color = preset.get('logo_color', self.logo_color)
                self.title_color = preset.get('title_color', self.title_color)
                self.subtitle_color = preset.get('subtitle_color', self.subtitle_color)
                self.progress_color = preset.get('progress_color', self.progress_color)
                self.title_text = preset.get('title_text', self.title_text)
                self.subtitle_text = preset.get('subtitle_text', self.subtitle_text)
                self.loading_text = preset.get('loading_text', self.loading_text)
                self.enable_animations = preset.get('enable_animations', self.enable_animations)
                self.animation_style = preset.get('animation_style', self.animation_style)
                self.show_progress_bar = preset.get('show_progress_bar', self.show_progress_bar)
                self.show_logo = preset.get('show_logo', self.show_logo)
                
                # Update UI
                self.width_var.set(str(self.width))
                self.height_var.set(str(self.height))
                self.title_var.set(self.title_text)
                self.subtitle_var.set(self.subtitle_text)
                self.loading_var.set(self.loading_text)
                self.animation_var.set(self.animation_style)
                self.enable_animations_var.set(self.enable_animations)
                self.show_progress_var.set(self.show_progress_bar)
                self.show_logo_var.set(self.show_logo)
                
                # Update color buttons
                self.bg_start_btn.config(bg=self.bg_gradient_start)
                self.bg_end_btn.config(bg=self.bg_gradient_end)
                self.title_color_btn.config(bg=self.title_color)
                self.subtitle_color_btn.config(bg=self.subtitle_color)
                self.logo_color_btn.config(bg=self.logo_color)
                self.progress_color_btn.config(bg=self.progress_color)
                
                self.dims_label.config(text=f"Size: {self.width}x{self.height}")
                self.generate_preview()
                
                messagebox.showinfo("Success", "Preset loaded successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load preset: {e}")
    
    def export_splash(self):
        """Export splash screen image"""
        try:
            # Default to assets/splash directory
            assets_dir = Path(__file__).parent.parent / "assets" / "splash"
            assets_dir.mkdir(parents=True, exist_ok=True)
            
            filename = filedialog.asksaveasfilename(
                title="Save Splash Screen",
                initialdir=str(assets_dir),
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("All files", "*.*")
                ]
            )
            
            if filename:
                splash = self.create_splash_screen()
                splash.save(filename)
                
                # Also save theme variant
                base_name = filename.rsplit('.', 1)[0]
                ext = filename.rsplit('.', 1)[1] if '.' in filename else 'png'
                theme_filename = f"{base_name}-theme.{ext}"
                splash.save(theme_filename)
                
                messagebox.showinfo("Success", f"Splash screen saved as {filename}\nTheme variant saved as {theme_filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export splash screen: {e}")
    
    def generate_code(self):
        """Generate Python code for the splash screen"""
        try:
            # Default to assets/splash directory
            assets_dir = Path(__file__).parent.parent / "assets" / "splash"
            assets_dir.mkdir(parents=True, exist_ok=True)
            
            filename = filedialog.asksaveasfilename(
                title="Save Splash Screen Code",
                initialdir=str(assets_dir),
                defaultextension=".py",
                filetypes=[("Python files", "*.py"), ("All files", "*.*")]
            )
            
            if filename:
                code = self.create_splash_code()
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(code)
                messagebox.showinfo("Success", f"Splash screen code saved as {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate code: {e}")
    
    def create_splash_code(self):
        """Create Python code for the splash screen"""
        return f'''#!/usr/bin/env python3
"""
Generated Splash Screen for FilePulse
Created with FilePulse Splash Screen Generator
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from PIL import Image, ImageDraw, ImageFont, ImageTk

class CustomSplashScreen:
    def __init__(self, callback=None):
        self.callback = callback
        self.splash_window = None
        self.progress_var = None
        self.canvas = None
        
        # Settings
        self.width = {self.width}
        self.height = {self.height}
        self.bg_gradient_start = "{self.bg_gradient_start}"
        self.bg_gradient_end = "{self.bg_gradient_end}"
        self.logo_color = "{self.logo_color}"
        self.title_color = "{self.title_color}"
        self.subtitle_color = "{self.subtitle_color}"
        self.progress_color = "{self.progress_color}"
        self.progress_bg_color = "{self.progress_bg_color}"
        
        # Text
        self.title_text = "{self.title_text}"
        self.subtitle_text = "{self.subtitle_text}"
        self.loading_text = "{self.loading_text}"
        
        # Options
        self.show_logo = {self.show_logo}
        self.show_progress_bar = {self.show_progress_bar}
        self.enable_animations = {self.enable_animations}
        
        self.create_splash()
    
    def create_splash(self):
        """Create splash screen window"""
        self.splash_window = tk.Toplevel()
        self.splash_window.title("")
        self.splash_window.geometry(f"{{self.width}}x{{self.height}}")
        self.splash_window.resizable(False, False)
        self.splash_window.overrideredirect(True)
        
        # Center window
        self.splash_window.update_idletasks()
        x = (self.splash_window.winfo_screenwidth() // 2) - (self.width // 2)
        y = (self.splash_window.winfo_screenheight() // 2) - (self.height // 2)
        self.splash_window.geometry(f"{{self.width}}x{{self.height}}+{{x}}+{{y}}")
        
        # Create canvas
        self.canvas = tk.Canvas(self.splash_window, width=self.width, height=self.height, 
                               highlightthickness=0)
        self.canvas.pack()
        
        # Draw splash screen
        self.draw_splash_screen()
        
        # Start animation if enabled
        if self.enable_animations:
            self.animate_splash()
        
        # Auto-close after delay or when callback completes
        if self.callback:
            threading.Thread(target=self.run_callback_and_close, daemon=True).start()
        else:
            self.splash_window.after(3000, self.close)
    
    def draw_splash_screen(self):
        """Draw the splash screen content"""
        # Create background image
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)
        
        # Draw gradient background
        start_color = self.hex_to_rgb(self.bg_gradient_start)
        end_color = self.hex_to_rgb(self.bg_gradient_end)
        
        for y in range(self.height):
            ratio = y / self.height
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        
        # Convert to PhotoImage and display
        self.bg_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(self.width//2, self.height//2, image=self.bg_image)
        
        # Draw logo
        if self.show_logo:
            self.draw_logo()
        
        # Draw text
        self.draw_text()
        
        # Draw progress bar
        if self.show_progress_bar:
            self.draw_progress_bar(0)
    
    def draw_logo(self):
        """Draw the FilePulse logo"""
        center_x = self.width // 2
        logo_y = self.height // 3
        logo_size = min(80, self.width // 8)
        
        # Folder
        folder_width = logo_size
        folder_height = logo_size // 2
        
        self.canvas.create_rectangle(
            center_x - folder_width//2, logo_y - folder_height//2,
            center_x + folder_width//2, logo_y + folder_height//2,
            fill=self.logo_color, outline=self.logo_color
        )
        
        # Folder tab
        tab_width = folder_width // 3
        self.canvas.create_rectangle(
            center_x - folder_width//2, logo_y - folder_height//2 - folder_height//3,
            center_x - folder_width//2 + tab_width, logo_y - folder_height//2,
            fill=self.logo_color, outline=self.logo_color
        )
        
        # Pulse rings
        pulse_color = self.progress_color if self.logo_color == "#ffffff" else self.logo_color
        for i, radius in enumerate([logo_size//2 + 10, logo_size//2 + 20, logo_size//2 + 30]):
            self.canvas.create_oval(
                center_x - radius, logo_y - radius,
                center_x + radius, logo_y + radius,
                outline=pulse_color, width=2, fill=""
            )
    
    def draw_text(self):
        """Draw text elements"""
        center_x = self.width // 2
        
        # Title
        title_y = self.height // 2
        self.canvas.create_text(center_x, title_y, text=self.title_text,
                               fill=self.title_color, font=("Arial", 24, "bold"))
        
        # Subtitle
        subtitle_y = title_y + 40
        self.canvas.create_text(center_x, subtitle_y, text=self.subtitle_text,
                               fill=self.subtitle_color, font=("Arial", 14))
        
        # Loading text
        loading_y = self.height - 60
        self.canvas.create_text(center_x, loading_y, text=self.loading_text,
                               fill=self.subtitle_color, font=("Arial", 12))
    
    def draw_progress_bar(self, progress):
        """Draw progress bar"""
        if not self.show_progress_bar:
            return
            
        bar_width = self.width // 2
        bar_height = 6
        bar_x = (self.width - bar_width) // 2
        bar_y = self.height - 40
        
        # Clear previous progress bar
        self.canvas.delete("progress_bar")
        
        # Background
        self.canvas.create_rectangle(
            bar_x, bar_y, bar_x + bar_width, bar_y + bar_height,
            fill=self.progress_bg_color, outline="", tags="progress_bar"
        )
        
        # Progress
        progress_width = int(bar_width * progress)
        if progress_width > 0:
            self.canvas.create_rectangle(
                bar_x, bar_y, bar_x + progress_width, bar_y + bar_height,
                fill=self.progress_color, outline="", tags="progress_bar"
            )
    
    def animate_splash(self):
        """Animate the splash screen"""
        def animate():
            for i in range(100):
                progress = i / 100
                self.splash_window.after(0, lambda p=progress: self.draw_progress_bar(p))
                time.sleep(0.03)
        
        threading.Thread(target=animate, daemon=True).start()
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def run_callback_and_close(self):
        """Run callback and close splash"""
        if self.callback:
            self.callback()
        time.sleep(1)  # Minimum display time
        self.splash_window.after(0, self.close)
    
    def close(self):
        """Close splash screen"""
        if self.splash_window:
            self.splash_window.destroy()


def show_splash(callback=None):
    """Show the splash screen"""
    return CustomSplashScreen(callback)


if __name__ == "__main__":
    # Test the splash screen
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    def test_callback():
        print("Loading complete!")
        time.sleep(2)  # Simulate loading
    
    splash = show_splash(test_callback)
    root.mainloop()
'''


def main():
    """Main entry point"""
    root = tk.Tk()
    app = SplashScreenGenerator(root)
    
    # Generate initial preview after UI is ready
    root.after(100, app.generate_preview)
    
    root.mainloop()


if __name__ == "__main__":
    main()
