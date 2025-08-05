import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk

class SplashScreen:
    def __init__(self, text="Loading FilePulse...", bg="#23272e", fg="#ffffff", image_path=None, duration=2000):
        self.root = tk.Toplevel()
        self.root.overrideredirect(True)
        self.root.configure(bg=bg)
        self.root.attributes("-topmost", True)
        self.duration = duration
        self.image_label = None
        self.text_label = None
        self.image = None
        self._setup_ui(text, fg, bg, image_path)

    def _setup_ui(self, text, fg, bg, image_path):
        frame = tk.Frame(self.root, bg=bg, padx=24, pady=18)
        frame.pack()
        if image_path and Path(image_path).exists():
            img = Image.open(image_path)
            img = img.resize((80, 80))
            self.image = ImageTk.PhotoImage(img)
            self.image_label = tk.Label(frame, image=self.image, bg=bg)
            self.image_label.pack(pady=(0, 10))
        self.text_label = tk.Label(frame, text=text, font=("Segoe UI", 16, "bold"), fg=fg, bg=bg)
        self.text_label.pack()
        self.progress = ttk.Progressbar(frame, mode="indeterminate", length=180)
        self.progress.pack(pady=(16, 0))
        self.progress.start(10)

    def show(self, on_close=None):
        self.root.after(self.duration, lambda: self.close(on_close))
        self.center()
        self.root.mainloop()

    def close(self, on_close=None):
        self.progress.stop()
        self.root.destroy()
        if on_close:
            on_close()

    def center(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

# Example usage:
if __name__ == "__main__":
    def launch_main():
        print("Main app would launch here!")
    splash = SplashScreen(text="Welcome to FilePulse!", image_path=None, duration=2000)
    splash.show(on_close=launch_main)
