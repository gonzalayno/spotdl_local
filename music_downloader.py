import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import subprocess
import threading
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

        # Configurar colores
        self.bg_color = "#121212"
        self.accent_color = "#1DB954"  # Verde Spotify
        self.text_color = "#FFFFFF"
        self.secondary_bg = "#282828"

        # Configurar estilo
        self.style = ttk.Style()
        self.configure_styles()

        # Variables
        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="mp3")
        self.download_path = os.path.expanduser("~/Downloads")

        # Crear widgets
        self.create_header()
        self.create_main_frame()
        self.create_footer()

    def configure_styles(self):
        # Configurar estilos personalizados para los widgets
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Header.TFrame", background=self.secondary_bg)
        self.style.configure("Footer.TFrame", background=self.secondary_bg)

        self.style.configure("TLabel",
                             background=self.bg_color,
                             foreground=self.text_color,
                             font=("Segoe UI", 10))

        self.style.configure("Header.TLabel",
                             background=self.secondary_bg,
                             foreground=self.text_color,
                             font=("Segoe UI", 16, "bold"))

        self.style.configure("TEntry",
                             fieldbackground=self.secondary_bg,
                             foreground=self.text_color,
                             borderwidth=0,
                             font=("Segoe UI", 10))

        self.style.map("TEntry",
                       fieldbackground=[("focus", self.secondary_bg)])

        self.style.configure("TButton",
                             background=self.accent_color,
                             foreground=self.text_color,
                             borderwidth=0,
                             font=("Segoe UI", 10, "bold"))

        self.style.map("TButton",
                       background=[("active", "#1ed760")],
                       relief=[("pressed", "flat")])

        self.style.configure("Secondary.TButton",
                             background=self.secondary_bg,
                             foreground=self.text_color)

        self.style.map("Secondary.TButton",
                       background=[("active", "#3E3E3E")])

        self.style.configure("TCombobox",
                             fieldbackground=self.secondary_bg,
                             background=self.bg_color,
                             foreground=self.text_color,
                             arrowcolor=self.text_color)

        self.style.map("TCombobox",
                       fieldbackground=[("readonly", self.secondary_bg)],
                       selectbackground=[("readonly", self.secondary_bg)])

    def create_header(self):
        header_frame = ttk.Frame(self.root, style="Header.TFrame")
        header_frame.pack(fill=tk.X, padx=0, pady=0)

        # Título de la aplicación con ícono
        self.load_logo(header_frame)

        app_title = ttk.Label(header_frame,
                              text="Spotify Music Downloader",
                              style="Header.TLabel")
        app_title.pack(side=tk.LEFT, padx=10, pady=15)

    def load_logo(self, parent):
        try:
            # Intenta cargar el logo de Spotify desde una URL (o usa un archivo local)
            response = requests.get(
                "https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/232px-Spotify_icon.svg.png")
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img = img.resize((32, 32), Image.LANCZOS)

            self.logo_img = ImageTk.PhotoImage(img)
            logo_label = ttk.Label(parent, image=self.logo_img, background=self.secondary_bg)
            logo_label.pack(side=tk.LEFT, padx=15, pady=15)
        except Exception:
            pass  # Si no se puede cargar el logo, simplemente continuar sin él

    def create_main_frame(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # URL Frame
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=10)

        url_label = ttk.Label(url_frame, text="URL de Spotify:")
        url_label.pack(anchor=tk.W, pady=(0, 5))

        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=50)
        url_entry.pack(fill=tk.X, ipady=8)

        # Settings Frame
        settings_frame = ttk.Frame(main_frame)
        settings_frame.pack(fill=tk.X, pady=10)

        # Fila para formato
        format_frame = ttk.Frame(settings_frame)
        format_frame.pack(fill=tk.X, pady=5)

        format_label = ttk.Label(format_frame, text="Formato:")
        format_label.pack(side=tk.LEFT, padx=(0, 10))

        formats = ["mp3", "flac", "wav", "opus", "m4a"]
        format_combobox = ttk.Combobox(format_frame,
                                       textvariable=self.format_var,
                                       values=formats,
                                       state="readonly",
                                       width=15)
        format_combobox.pack(side=tk.LEFT)

        # Fila para ruta
        path_frame = ttk.Frame(settings_frame)
        path_frame.pack(fill=tk.X, pady=10)

        path_label = ttk.Label(path_frame, text="Ruta de descarga:")
        path_label.pack(side=tk.LEFT, padx=(0, 10))

        self.path_display = ttk.Label(path_frame,
                                      text=self.download_path,
                                      foreground="#AAAAAA")
        self.path_display.pack(side=tk.LEFT, fill=tk.X, expand=True)

        path_button = ttk.Button(path_frame,
                                 text="Cambiar",
                                 command=self.select_path,
                                 style="Secondary.TButton",
                                 width=10)
        path_button.pack(side=tk.RIGHT, padx=5)

        # Botón de descarga
        download_button = ttk.Button(main_frame,
                                     text="DESCARGAR",
                                     command=self.download_music,
                                     width=20)
        download_button.pack(pady=15, ipady=8)

        # Log Frame
        log_frame = ttk.Frame(main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        log_label = ttk.Label(log_frame, text="Registro de actividad:")
        log_label.pack(anchor=tk.W, pady=(0, 5))

        # Personalizar el área de log
        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                  wrap=tk.WORD,
                                                  bg=self.secondary_bg,
                                                  fg="#CCCCCC",
                                                  insertbackground=self.text_color,
                                                  font=("Consolas", 9),
                                                  height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def create_footer(self):
        footer_frame = ttk.Frame(self.root, style="Footer.TFrame")
        footer_frame.pack(fill=tk.X, padx=0, pady=0)

        # Información de estado y versión
        status_label = ttk.Label(footer_frame,
                                 text="Listo para descargar",
                                 style="TLabel",
                                 background=self.secondary_bg,
                                 foreground="#AAAAAA")
        status_label.pack(side=tk.LEFT, padx=15, pady=10)

        version_label = ttk.Label(footer_frame,
                                  text="v1.0.0",
                                  style="TLabel",
                                  background=self.secondary_bg,
                                  foreground="#AAAAAA")
        version_label.pack(side=tk.RIGHT, padx=15, pady=10)

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


        # Preparar el comando
        comando = ["spotdl", "--cookie-file", "youtube_cookies.txt", "--output", self.download_path, "--format",
                   formato, "download", url]

        try:
            self.log_message(f"Iniciando descarga: {url}")
            self.log_message(f"Formato: {formato}")
            self.log_message(f"Ruta de descarga: {self.download_path}")
            self.log_message("Procesando... (puede tardar unos momentos)")

            # Ejecutar en un hilo separado para no bloquear la interfaz
            threading.Thread(target=self.execute_download, args=(comando,), daemon=True).start()

        except Exception as e:
            self.log_message(f"Error inesperado: {e}")

    def execute_download(self, comando):
        try:
            proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

            for linea in proceso.stdout:
                self.log_message(linea.strip())

            proceso.wait()

            if proceso.returncode == 0:
                self.log_message("\n✅ Descarga completada exitosamente")
            else:
                self.log_message(f"\n❌ Error: Proceso terminado con código {proceso.returncode}")

        except Exception as e:
            self.log_message(f"Error en la ejecución: {e}")

    def log_message(self, message):
        # Asegurarse de que los mensajes de log se muestren en el hilo principal
        self.root.after(0, self._append_log, message)

    def _append_log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)


# Iniciar la aplicación
if __name__ == "__main__":
    root = ThemedTk(theme="equilux")  # Usa un tema oscuro como base
    root.configure(bg="#121212")
    app = SpotifyDownloaderApp(root)
    root.mainloop()