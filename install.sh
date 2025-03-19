#!/bin/bash

# Colores para los mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Instalador de SpotDL Music Downloader ===${NC}\n"

# Verificar si git está instalado
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}Git no está instalado. Instalando...${NC}"
    sudo apt update
    sudo apt install git -y
fi

# Crear directorio temporal
TEMP_DIR=$(mktemp -d)
echo -e "${YELLOW}Creando directorio temporal...${NC}"

# Función para intentar clonar con diferentes opciones
clone_repository() {
    local attempts=0
    local max_attempts=3
    
    while [ $attempts -lt $max_attempts ]; do
        attempts=$((attempts + 1))
        echo -e "${YELLOW}Intento $attempts de $max_attempts...${NC}"
        
        # Configurar git para usar HTTPS
        git config --global http.sslVerify false
        
        # Primer intento: clonado normal
        if [ $attempts -eq 1 ]; then
            if git clone https://github.com/gonzalayno/spotdl_local.git "$TEMP_DIR" 2>/dev/null; then
                return 0
            fi
        # Segundo intento: clonado superficial
        elif [ $attempts -eq 2 ]; then
            rm -rf "$TEMP_DIR"/*
            if git clone --depth 1 https://github.com/gonzalayno/spotdl_local.git "$TEMP_DIR" 2>/dev/null; then
                return 0
            fi
        # Tercer intento: usando el protocolo git
        else
            rm -rf "$TEMP_DIR"/*
            if git clone git://github.com/gonzalayno/spotdl_local.git "$TEMP_DIR" 2>/dev/null; then
                return 0
            fi
        fi
        
        echo -e "${RED}Intento $attempts falló. Esperando 5 segundos antes del siguiente intento...${NC}"
        sleep 5
    done
    
    return 1
}

# Intentar clonar el repositorio
echo -e "${YELLOW}Clonando el repositorio...${NC}"
if clone_repository; then
    echo -e "${GREEN}Repositorio clonado exitosamente.${NC}"
else
    echo -e "${RED}Error: No se pudo clonar el repositorio después de varios intentos.${NC}"
    echo -e "Por favor, verifica tu conexión a Internet y vuelve a intentarlo."
    rm -rf "$TEMP_DIR"
    exit 1
fi

# Cambiar al directorio del proyecto
cd "$TEMP_DIR"

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 no está instalado.${NC}"
    echo -e "Por favor, instala Python 3 primero:"
    echo -e "sudo apt update"
    echo -e "sudo apt install python3 python3-pip"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# Verificar si pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip3 no está instalado.${NC}"
    echo -e "Por favor, instala pip3 primero:"
    echo -e "sudo apt install python3-pip"
    rm -rf "$TEMP_DIR"
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
pyinstaller music_downloader.spec

# Crear el archivo create_icon.py
echo -e "${YELLOW}Creando script para el icono...${NC}"
cat > create_icon.py << 'EOL'
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Crear una imagen de 512x512 píxeles
    size = 512
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Dibujar un círculo verde (color de Spotify)
    circle_color = (29, 185, 84)  # RGB para el verde de Spotify
    draw.ellipse([0, 0, size, size], fill=circle_color)
    
    # Dibujar un círculo blanco en el centro
    white_circle_size = int(size * 0.8)
    white_circle_pos = (size - white_circle_size) // 2
    draw.ellipse([white_circle_pos, white_circle_pos, 
                  white_circle_pos + white_circle_size, 
                  white_circle_pos + white_circle_size], 
                 fill='white')
    
    # Intentar usar una fuente del sistema o usar la predeterminada
    try:
        font_size = int(size * 0.4)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Dibujar las letras "SD" en verde
    text = "SD"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    draw.text((x, y), text, fill=circle_color, font=font)
    
    # Guardar el icono
    image.save('spotdl.png', 'PNG')

if __name__ == '__main__':
    create_icon()
EOL

# Generar el icono
echo -e "${YELLOW}Generando el icono...${NC}"
python create_icon.py

# Crear el archivo .desktop
echo -e "${YELLOW}Creando archivo .desktop...${NC}"
cat > spotdl.desktop << 'EOL'
[Desktop Entry]
Version=1.0
Type=Application
Name=SpotDL Music Downloader
Comment=Descarga música desde Spotify y YouTube
Exec=/usr/local/bin/spotdl
Icon=/usr/share/icons/spotdl.png
Terminal=false
Categories=Audio;Music;Network;
Keywords=music;spotify;youtube;download;
EOL

# Verificar si los archivos necesarios existen
echo -e "${YELLOW}Verificando archivos necesarios...${NC}"
if [ ! -f "dist/music_downloader" ]; then
    echo -e "${RED}Error: No se encuentra el archivo dist/music_downloader${NC}"
fi
if [ ! -f "spotdl.png" ]; then
    echo -e "${RED}Error: No se encuentra el archivo spotdl.png${NC}"
fi
if [ ! -f "spotdl.desktop" ]; then
    echo -e "${RED}Error: No se encuentra el archivo spotdl.desktop${NC}"
fi

if [ ! -f "dist/music_downloader" ] || [ ! -f "spotdl.png" ] || [ ! -f "spotdl.desktop" ]; then
    echo -e "${RED}Error: No se pudieron crear todos los archivos necesarios.${NC}"
    echo -e "${YELLOW}Contenido del directorio actual:${NC}"
    ls -la
    echo -e "${YELLOW}Contenido del directorio dist (si existe):${NC}"
    if [ -d "dist" ]; then
        ls -la dist/
    else
        echo -e "${RED}El directorio dist no existe${NC}"
    fi
    rm -rf "$TEMP_DIR"
    exit 1
fi

# Solicitar contraseña de sudo
echo -e "${YELLOW}Se necesitan permisos de administrador para instalar la aplicación...${NC}"

# Crear directorios necesarios
sudo mkdir -p /usr/local/bin
sudo mkdir -p /usr/share/icons
sudo mkdir -p /usr/share/applications

# Crear archivo de caché
echo -e "${YELLOW}Creando archivo de caché...${NC}"
touch ~/.spotdl_cache.json
chmod 644 ~/.spotdl_cache.json

# Copiar archivos
echo -e "${YELLOW}Copiando archivos...${NC}"
sudo cp dist/music_downloader /usr/local/bin/spotdl
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

# Limpiar archivos temporales
echo -e "${YELLOW}Limpiando archivos temporales...${NC}"
rm -rf "$TEMP_DIR"

echo -e "\n${GREEN}¡Instalación completada!${NC}"
echo -e "La aplicación ahora está disponible en el menú de aplicaciones."
echo -e "También puedes ejecutarla desde la terminal escribiendo: ${YELLOW}spotdl${NC}"
echo -e "\n${YELLOW}Nota:${NC} Si la aplicación no aparece en el menú inmediatamente,"
echo -e "cierra sesión y vuelve a iniciar sesión en tu sistema."