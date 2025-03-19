#!/bin/bash

# Verificar si se está ejecutando como root
if [ "$EUID" -ne 0 ]; then 
    echo "Por favor, ejecuta el script como root (usando sudo)"
    exit 1
fi

echo "Iniciando instalación..."

# Verificar que los archivos necesarios existan
if [ ! -f "dist/spotdl" ]; then
    echo "Error: No se encuentra el ejecutable en dist/spotdl"
    echo "Por favor, ejecuta primero: pyinstaller --clean --onefile music_downloader.spec"
    exit 1
fi

if [ ! -f "spotdl.png" ]; then
    echo "Error: No se encuentra el archivo spotdl.png"
    echo "Por favor, ejecuta primero: python create_icon.py"
    exit 1
fi

if [ ! -f "spotdl.desktop" ]; then
    echo "Error: No se encuentra el archivo spotdl.desktop"
    exit 1
fi

# Crear directorios necesarios
echo "Creando directorios..."
mkdir -p /usr/local/bin
mkdir -p /usr/share/icons
mkdir -p /usr/share/applications

# Copiar el ejecutable
echo "Copiando ejecutable..."
cp dist/spotdl /usr/local/bin/spotdl
chmod +x /usr/local/bin/spotdl

# Verificar que el ejecutable se copió correctamente
if [ ! -f "/usr/local/bin/spotdl" ]; then
    echo "Error: No se pudo copiar el ejecutable"
    exit 1
fi

# Copiar el icono
echo "Copiando icono..."
cp spotdl.png /usr/share/icons/

# Copiar el archivo .desktop
echo "Copiando archivo .desktop..."
cp spotdl.desktop /usr/share/applications/

# Actualizar la base de datos de aplicaciones
echo "Actualizando base de datos de aplicaciones..."
update-desktop-database

# Verificar permisos
echo "Verificando permisos..."
chmod 755 /usr/local/bin/spotdl
chmod 644 /usr/share/icons/spotdl.png
chmod 644 /usr/share/applications/spotdl.desktop

echo "Instalación completada. La aplicación ahora está disponible en el menú de aplicaciones."
echo "Para probar la aplicación, puedes ejecutar: spotdl"

sudo rm /usr/local/bin/spotdl
sudo rm /usr/share/icons/spotdl.png
sudo rm /usr/share/applications/spotdl.desktop

rm -rf build dist 