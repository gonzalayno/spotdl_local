# SpotDL Music Downloader

Una aplicación gráfica para descargar música de Spotify y YouTube.

## Requisitos previos

- Ubuntu 20.04 o superior
- Python 3.8 o superior
- pip3 (gestor de paquetes de Python)
- Conexión a Internet

## Instalación

1. Descarga el instalador:
```bash
wget https://raw.githubusercontent.com/gonzalayno/spotdl_local/main/install.sh
```

2. Dale permisos de ejecución al script de instalación:
```bash
chmod +x install.sh
```

3. Ejecuta el script de instalación:
```bash
./install.sh
```

El script de instalación:
- Verificará que tengas Git instalado (lo instalará si es necesario)
- Clonará el repositorio en un directorio temporal
- Creará un entorno virtual
- Instalará todas las dependencias necesarias
- Creará el ejecutable
- Instalará la aplicación en tu sistema
- Limpiará los archivos temporales

Si encuentras algún error durante la instalación:
1. Verifica tu conexión a Internet
2. Asegúrate de tener suficiente espacio en disco
3. Intenta ejecutar el script nuevamente

## Uso

Una vez instalada, puedes:
1. Buscar "SpotDL Music Downloader" en el menú de aplicaciones
2. O ejecutar desde la terminal:
```bash
spotdl
```

## Características

- Interfaz gráfica moderna y fácil de usar
- Soporte para descargar de Spotify y YouTube
- Múltiples formatos de salida (mp3, flac, wav, opus, m4a)
- Selección personalizable de carpeta de descarga
- Registro de actividad en tiempo real
- Sistema de inicio de sesión para YouTube

## Desinstalación

Para desinstalar la aplicación:
```bash
sudo rm -f /usr/local/bin/spotdl
sudo rm -f /usr/share/icons/spotdl.png
sudo rm -f /usr/share/applications/spotdl.desktop
sudo update-desktop-database
```

## Solución de problemas

Si la aplicación no aparece en el menú después de la instalación:
1. Cierra sesión en tu sistema
2. Vuelve a iniciar sesión

Si encuentras algún error, por favor:
1. Verifica que tienes Python 3.8 o superior instalado
2. Asegúrate de tener una conexión a Internet estable
3. Revisa los mensajes de error en la terminal

## Soporte

Si necesitas ayuda o encuentras algún problema, por favor:
1. Revisa la sección de problemas (Issues) en GitHub
2. Crea un nuevo issue si el problema no está reportado
3. Incluye los mensajes de error que aparezcan en la terminal 