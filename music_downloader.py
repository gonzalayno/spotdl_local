import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import subprocess
import os
from PIL import Image, ImageTk
import requests
from io import BytesIO
import re
from ttkthemes import ThemedTk
import random
import time
import webbrowser
import json
from pathlib import Path
from spotdl.utils.ffmpeg import is_ffmpeg_installed


class SpotifyDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Downloader")
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
        self.platform_var = tk.StringVar(value="spotify")
        self.download_path = os.path.expanduser("~/Downloads")
        self.process = None
        self.is_youtube_logged_in = False
        
        # Lista de User-Agents para rotación
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59"
        ]

        self.cache_file = Path.home() / '.spotdl_cache.json'
        self.cache_duration = 3600  # 1 hora en segundos
        
        # Verificar caché
        if self._check_cache():
            self._load_from_cache()
        else:
            self._initialize_app()
            self._save_to_cache()

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
        app_title = ttk.Label(header_frame, text="Music Downloader", style="TLabel")
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

        platform_frame = ttk.Frame(main_frame, style="TFrame")
        platform_frame.pack(fill=tk.X, pady=10)
        platform_label = ttk.Label(platform_frame, text="Plataforma:")
        platform_label.pack(side=tk.LEFT, padx=(0, 10))
        platforms = ["spotify", "youtube"]
        platform_combobox = ttk.Combobox(platform_frame, textvariable=self.platform_var, values=platforms, state="readonly",
                                       width=15)
        platform_combobox.pack(side=tk.LEFT)
        platform_combobox.bind('<<ComboboxSelected>>', self.update_url_label)

        # Agregar botón de inicio de sesión de YouTube
        self.youtube_login_button = ttk.Button(platform_frame, text="Iniciar sesión en YouTube", 
                                             command=self.youtube_login, width=20)
        self.youtube_login_button.pack(side=tk.RIGHT, padx=5)
        self.update_youtube_login_status()

        url_frame = ttk.Frame(main_frame, style="TFrame")
        url_frame.pack(fill=tk.X, pady=10)
        self.url_label = ttk.Label(url_frame, text="URL de Spotify:")
        self.url_label.pack(anchor=tk.W)
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

    def update_url_label(self, event=None):
        platform = self.platform_var.get()
        if platform == "spotify":
            self.url_label.config(text="URL de Spotify:")
        else:
            self.url_label.config(text="URL de YouTube:")

    def select_path(self):
        path = filedialog.askdirectory(initialdir=self.download_path)
        if path:
            self.download_path = path
            self.path_display.config(text=path)

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def youtube_login(self):
        """Abre YouTube en el navegador para iniciar sesión"""
        self.log_message("Abriendo YouTube para iniciar sesión...")
        webbrowser.open('https://accounts.google.com/signin/v2/identifier?service=youtube')
        
        # Mostrar instrucciones más detalladas
        messagebox.showinfo("Inicio de sesión en YouTube", 
                          "Sigue estos pasos:\n\n" +
                          "1. Se abrirá una ventana del navegador con la página de inicio de sesión de Google\n" +
                          "2. Inicia sesión con tu cuenta de Google\n" +
                          "3. Si aparece una pantalla de verificación de seguridad, completa los pasos\n" +
                          "4. Una vez que hayas iniciado sesión correctamente, cierra la ventana del navegador\n" +
                          "5. Vuelve aquí y haz clic en 'OK' para continuar\n\n" +
                          "Importante: Asegúrate de iniciar sesión completamente antes de cerrar el navegador.")
        
        self.is_youtube_logged_in = True
        self.update_youtube_login_status()
        self.log_message("Inicio de sesión en YouTube completado.")

    def update_youtube_login_status(self):
        """Actualiza el estado del botón de inicio de sesión"""
        if self.is_youtube_logged_in:
            self.youtube_login_button.config(text="✓ Sesión iniciada", state="disabled")
        else:
            self.youtube_login_button.config(text="Iniciar sesión en YouTube", state="normal")

    def download_music(self):
        url = self.url_var.get().strip()
        if not url:
            self.log_message("Error: URL no proporcionada")
            return

        formato = self.format_var.get()
        platform = self.platform_var.get()

        if platform == "spotify":
            comando = ["spotdl", "--output", self.download_path, "--format", formato, "download", url]
        else:  # youtube
            if not self.is_youtube_logged_in:
                respuesta = messagebox.askyesno("Inicio de sesión requerido", 
                                              "Para descargar de YouTube, necesitas iniciar sesión primero.\n" +
                                              "¿Deseas iniciar sesión ahora?")
                if respuesta:
                    self.youtube_login()
                    return
                else:
                    return

            # Crear directorio temporal para cookies si no existe
            temp_dir = os.path.join(os.path.expanduser("~"), ".yt-dlp")
            os.makedirs(temp_dir, exist_ok=True)
            
            # Generar un nombre de archivo temporal para las cookies
            cookie_file = os.path.join(temp_dir, f"cookies_{int(time.time())}.txt")
            
            comando = [
                "yt-dlp",
                "-x",
                "--audio-format", formato,
                "--audio-quality", "0",
                "--no-check-certificates",
                "--no-warnings",
                "--ignore-errors",
                "--extract-audio",
                "--add-header", f"User-Agent:{self.get_random_user_agent()}",
                "--no-playlist",
                "--cookies-from-browser", "chrome",  # Usar cookies del navegador Chrome
                "--sleep-interval", "2",
                "--max-sleep-interval", "5",
                "--retries", "10",
                "--fragment-retries", "10",
                "--file-access-retries", "10",
                "--extractor-retries", "10",
                "--socket-timeout", "30",
                "-o", os.path.join(self.download_path, "%(title)s.%(ext)s"),
                url
            ]

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

    def _check_cache(self):
        if not self.cache_file.exists():
            return False
            
        try:
            cache_data = json.loads(self.cache_file.read_text())
            if time.time() - cache_data.get('timestamp', 0) > self.cache_duration:
                return False
            return True
        except:
            return False
            
    def _load_from_cache(self):
        try:
            cache_data = json.loads(self.cache_file.read_text())
            # Cargar datos del caché
            self.spotify_client = cache_data.get('spotify_client')
            self.ffmpeg_installed = cache_data.get('ffmpeg_installed')
            self.ytm_connection = cache_data.get('ytm_connection')
        except:
            self._initialize_app()
            
    def _save_to_cache(self):
        try:
            cache_data = {
                'timestamp': time.time(),
                'spotify_client': self.spotify_client,
                'ffmpeg_installed': self.ffmpeg_installed,
                'ytm_connection': self.ytm_connection
            }
            self.cache_file.write_text(json.dumps(cache_data))
        except:
            pass
            
    def _initialize_app(self):
        # Inicializar la aplicación normalmente
        self.spotify_client = None
        self.ffmpeg_installed = False
        self.ytm_connection = False
        
        # Verificar ffmpeg
        if is_ffmpeg_installed():
            self.ffmpeg_installed = True
            
        # Verificar conexión YTM
        if check_ytmusic_connection():
            self.ytm_connection = True
            
        # Inicializar cliente Spotify
        try:
            self.spotify_client = SpotifyClient()
        except:
            pass
            
        # Resto de la inicialización...


if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    root.configure(bg="#121212")
    app = SpotifyDownloaderApp(root)
    root.mainloop()
