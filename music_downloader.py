import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import subprocess
import os
from PIL import Image, ImageTk
import requests
from io import BytesIO
import re
from ttkthemes import ThemedTk


class SpotifyDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spotify Music Downloader")
        self.root.geometry("800x600")
        self.root.minsize(700, 550)

        self.bg_color = "#121212"
        self.accent_color = "#1DB954"
        self.text_color = "#FFFFFF"
        self.secondary_bg = "#282828"

        self.style = ttk.Style()
        self.configure_styles()

        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="mp3")
        self.download_path = os.path.expanduser("~/Downloads")
        self.process = None

        self.create_header()
        self.create_main_frame()
        self.create_footer()

    def configure_styles(self):
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=("Segoe UI", 10))
        self.style.configure("TButton", background=self.accent_color, foreground=self.text_color,
                             font=("Segoe UI", 10, "bold"))

    def create_header(self):
        header_frame = ttk.Frame(self.root, style="TFrame")
        header_frame.pack(fill=tk.X)

        self.load_logo(header_frame)
        app_title = ttk.Label(header_frame, text="Spotify Music Downloader", style="TLabel")
        app_title.pack(side=tk.LEFT, padx=10, pady=15)

    def load_logo(self, parent):
        try:
            response = requests.get(
                "https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/232px-Spotify_icon.svg.png")
            img_data = BytesIO(response.content)
            img = Image.open(img_data).resize((32, 32), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            logo_label = ttk.Label(parent, image=self.logo_img, background=self.bg_color)
            logo_label.pack(side=tk.LEFT, padx=15, pady=15)
        except Exception:
            pass

    def create_main_frame(self):
        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        url_frame = ttk.Frame(main_frame, style="TFrame")
        url_frame.pack(fill=tk.X, pady=10)
        url_label = ttk.Label(url_frame, text="URL de Spotify:")
        url_label.pack(anchor=tk.W)
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=50)
        url_entry.pack(fill=tk.X, ipady=8)

        settings_frame = ttk.Frame(main_frame, style="TFrame")
        settings_frame.pack(fill=tk.X, pady=10)
        format_frame = ttk.Frame(settings_frame, style="TFrame")
        format_frame.pack(fill=tk.X, pady=5)
        format_label = ttk.Label(format_frame, text="Formato:")
        format_label.pack(side=tk.LEFT, padx=(0, 10))
        formats = ["mp3", "flac", "wav", "opus", "m4a"]
        format_combobox = ttk.Combobox(format_frame, textvariable=self.format_var, values=formats, state="readonly",
                                       width=15)
        format_combobox.pack(side=tk.LEFT)

        path_frame = ttk.Frame(settings_frame, style="TFrame")
        path_frame.pack(fill=tk.X, pady=10)
        path_label = ttk.Label(path_frame, text="Ruta de descarga:")
        path_label.pack(side=tk.LEFT, padx=(0, 10))
        self.path_display = ttk.Label(path_frame, text=self.download_path, foreground="#AAAAAA")
        self.path_display.pack(side=tk.LEFT, fill=tk.X, expand=True)
        path_button = ttk.Button(path_frame, text="Cambiar", command=self.select_path)
        path_button.pack(side=tk.RIGHT, padx=5)

        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.pack(pady=15)
        self.download_button = ttk.Button(button_frame, text="DESCARGAR", command=self.download_music, width=20)
        self.download_button.pack(side=tk.LEFT, padx=5)
        self.cancel_button = ttk.Button(button_frame, text="CANCELAR", command=self.cancel_download, width=20,
                                        state=tk.DISABLED)
        self.cancel_button.pack(side=tk.RIGHT, padx=5)

        log_frame = ttk.Frame(main_frame, style="TFrame")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        log_label = ttk.Label(log_frame, text="Registro de actividad:")
        log_label.pack(anchor=tk.W)
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, bg=self.secondary_bg, fg="#CCCCCC",
                                                  height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def create_footer(self):
        footer_frame = ttk.Frame(self.root, style="TFrame")
        footer_frame.pack(fill=tk.X)
        status_label = ttk.Label(footer_frame, text="Listo para descargar", foreground="#AAAAAA")
        status_label.pack(side=tk.LEFT, padx=15, pady=10)

    def select_path(self):
        path = filedialog.askdirectory(initialdir=self.download_path)
        if path:
            self.download_path = path
            self.path_display.config(text=path)

    def download_music(self):
        url = self.url_var.get().strip()
        if not url:
            self.log_message("Error: URL de Spotify no proporcionada")
            return


        formato = self.format_var.get()
        comando = ["spotdl", "--output", self.download_path, "--format", formato, "download", url]

        try:
            self.log_message("Iniciando descarga...")
            self.process = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            self.download_button.config(state=tk.DISABLED)
            self.cancel_button.config(state=tk.NORMAL)
            self.read_output()
        except Exception as e:
            self.log_message(f"Error: {e}")

    def read_output(self):
        if self.process:
            line = self.process.stdout.readline()
            if line:
                self.log_message(line.strip())
                self.root.after(100, self.read_output)
            elif self.process.poll() is not None:
                self.log_message("Descarga completada.")
                self.download_button.config(state=tk.NORMAL)
                self.cancel_button.config(state=tk.DISABLED)

    def cancel_download(self):
        if self.process:
            self.process.terminate()
            self.process = None
            self.log_message("Descarga cancelada.")
            self.download_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.DISABLED)

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)


if __name__ == "__main__":
    root = ThemedTk(theme="equilux")  # Usa un tema oscuro como base
    root.configure(bg="#121212")
    app = SpotifyDownloaderApp(root)
    root.mainloop()
