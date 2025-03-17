#!/bin/bash

# Colores para los mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Instalador de SpotDL Music Downloader ===${NC}\n"

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 no está instalado.${NC}"
    echo -e "Por favor, instala Python 3 primero:"
    echo -e "sudo apt update"
    echo -e "sudo apt install python3 python3-pip"
    exit 1
fi

# Verificar si pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip3 no está instalado.${NC}"
    echo -e "Por favor, instala pip3 primero:"
    echo -e "sudo apt install python3-pip"
    exit 1
fi

# Verificar si virtualenv está instalado
if ! command -v virtualenv &> /dev/null; then
    echo -e "${YELLOW}Instalando virtualenv...${NC}"
    sudo pip3 install virtualenv
fi

# Crear entorno virtual
echo -e "${YELLOW}Creando entorno virtual...${NC}"
python3 -m venv venv

# Activar entorno virtual
echo -e "${YELLOW}Activando entorno virtual...${NC}"
source venv/bin/activate

# Instalar dependencias
echo -e "${YELLOW}Instalando dependencias...${NC}"
pip install -r requirements.txt

# Instalar PyInstaller
echo -e "${YELLOW}Instalando PyInstaller...${NC}"
pip install pyinstaller

# Crear el ejecutable
echo -e "${YELLOW}Creando el ejecutable...${NC}"
pyinstaller --clean --onefile music_downloader.spec

# Generar el icono
echo -e "${YELLOW}Generando el icono...${NC}"
python create_icon.py

# Verificar si los archivos necesarios existen
if [ ! -f "dist/spotdl" ] || [ ! -f "spotdl.png" ] || [ ! -f "spotdl.desktop" ]; then
    echo -e "${RED}Error: No se pudieron crear todos los archivos necesarios.${NC}"
    exit 1
fi

# Solicitar contraseña de sudo
echo -e "${YELLOW}Se necesitan permisos de administrador para instalar la aplicación...${NC}"

# Crear directorios necesarios
sudo mkdir -p /usr/local/bin
sudo mkdir -p /usr/share/icons
sudo mkdir -p /usr/share/applications

# Copiar archivos
echo -e "${YELLOW}Copiando archivos...${NC}"
sudo cp dist/spotdl /usr/local/bin/
sudo cp spotdl.png /usr/share/icons/
sudo cp spotdl.desktop /usr/share/applications/

# Establecer permisos
echo -e "${YELLOW}Estableciendo permisos...${NC}"
sudo chmod +x /usr/local/bin/spotdl
sudo chmod 644 /usr/share/icons/spotdl.png
sudo chmod 644 /usr/share/applications/spotdl.desktop

# Actualizar base de datos de aplicaciones
echo -e "${YELLOW}Actualizando base de datos de aplicaciones...${NC}"
sudo update-desktop-database

# Desactivar entorno virtual
deactivate

echo -e "\n${GREEN}¡Instalación completada!${NC}"
echo -e "La aplicación ahora está disponible en el menú de aplicaciones."
echo -e "También puedes ejecutarla desde la terminal escribiendo: ${YELLOW}spotdl${NC}"
echo -e "\n${YELLOW}Nota:${NC} Si la aplicación no aparece en el menú inmediatamente,"
echo -e "cierra sesión y vuelve a iniciar sesión en tu sistema."