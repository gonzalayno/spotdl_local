@echo off
echo === Instalador de SpotDL Music Downloader ===
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Python no está instalado. Descargando instalador...
    
    REM Crear directorio temporal para el instalador
    set INSTALLER_DIR=%TEMP%\python_installer
    if not exist "%INSTALLER_DIR%" mkdir "%INSTALLER_DIR%"
    
    REM Descargar el instalador de Python
    echo Descargando Python...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe' -OutFile '%INSTALLER_DIR%\python-installer.exe'}"
    
    REM Instalar Python
    echo Instalando Python...
    start /wait "" "%INSTALLER_DIR%\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    REM Limpiar instalador
    rd /s /q "%INSTALLER_DIR%"
    
    REM Verificar si la instalación fue exitosa
    python --version >nul 2>&1
    if errorlevel 1 (
        echo Error: No se pudo instalar Python automáticamente.
        echo Por favor, instala Python manualmente desde https://www.python.org/downloads/
        pause
        exit /b 1
    )
)

REM Verificar si pip está instalado
pip --version >nul 2>&1
if errorlevel 1 (
    echo pip no está instalado. Instalando...
    
    REM Descargar get-pip.py
    echo Descargando pip...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'get-pip.py'}"
    
    REM Instalar pip
    echo Instalando pip...
    python get-pip.py --user
    
    REM Limpiar archivo de instalación
    del get-pip.py
    
    REM Verificar si la instalación fue exitosa
    pip --version >nul 2>&1
    if errorlevel 1 (
        echo Error: No se pudo instalar pip automáticamente.
        echo Por favor, instala pip manualmente desde https://pip.pypa.io/en/stable/installation/
        pause
        exit /b 1
    )
)

REM Verificar si Git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo Git no está instalado. Descargando instalador...
    
    REM Crear directorio temporal para el instalador
    set INSTALLER_DIR=%TEMP%\git_installer
    if not exist "%INSTALLER_DIR%" mkdir "%INSTALLER_DIR%"
    
    REM Descargar el instalador de Git
    echo Descargando Git...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.exe' -OutFile '%INSTALLER_DIR%\git-installer.exe'}"
    
    REM Instalar Git
    echo Instalando Git...
    start /wait "" "%INSTALLER_DIR%\git-installer.exe" /VERYSILENT /NORESTART
    
    REM Limpiar instalador
    rd /s /q "%INSTALLER_DIR%"
    
    REM Verificar si la instalación fue exitosa
    git --version >nul 2>&1
    if errorlevel 1 (
        echo Error: No se pudo instalar Git automáticamente.
        echo Por favor, instala Git manualmente desde https://git-scm.com/download/win
        pause
        exit /b 1
    )
)

REM Crear directorio temporal
set TEMP_DIR=%TEMP%\spotdl_install
if exist "%TEMP_DIR%" rd /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"

REM Clonar el repositorio
echo Clonando el repositorio...
git config --global http.postBuffer 524288000
git config --global core.compression 0
git config --global http.sslVerify false

echo Intentando clonar el repositorio...
git clone --depth 1 https://github.com/gonzalayno/spotdl_local.git "%TEMP_DIR%"
if errorlevel 1 (
    echo Error en el primer intento. Intentando método alternativo...
    git clone --depth 1 --single-branch https://github.com/gonzalayno/spotdl_local.git "%TEMP_DIR%"
    if errorlevel 1 (
        echo Error en el segundo intento. Intentando método alternativo...
        git clone --depth 1 --single-branch --no-checkout https://github.com/gonzalayno/spotdl_local.git "%TEMP_DIR%"
        if errorlevel 1 (
            echo Error: No se pudo clonar el repositorio.
            echo Por favor, verifica tu conexión a Internet y vuelve a intentarlo.
            echo Si el problema persiste, intenta:
            echo 1. Verificar tu conexión a Internet
            echo 2. Desactivar temporalmente tu firewall
            echo 3. Usar una VPN si estás detrás de un proxy
            pause
            exit /b 1
        )
    )
)

REM Cambiar al directorio del proyecto
cd /d "%TEMP_DIR%"

REM Crear entorno virtual
echo Creando entorno virtual...
python -m venv venv

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt

REM Instalar PyInstaller
echo Instalando PyInstaller...
pip install pyinstaller

REM Crear el ejecutable
echo Creando el ejecutable...
pyinstaller music_downloader.spec

REM Crear el archivo create_icon.py
echo Creando script para el icono...
(
echo from PIL import Image, ImageDraw, ImageFont
echo import os
echo.
echo def create_icon^(^):
echo     # Crear una imagen de 512x512 píxeles
echo     size = 512
echo     image = Image.new^('RGBA', ^(size, size^), ^(0, 0, 0, 0^)^)
echo     draw = ImageDraw.Draw^(image^)
echo     
echo     # Dibujar un círculo verde ^(color de Spotify^)
echo     circle_color = ^(29, 185, 84^)  # RGB para el verde de Spotify
echo     draw.ellipse^([0, 0, size, size], fill=circle_color^)
echo     
echo     # Dibujar un círculo blanco en el centro
echo     white_circle_size = int^(size * 0.8^)
echo     white_circle_pos = ^(size - white_circle_size^) // 2
echo     draw.ellipse^([white_circle_pos, white_circle_pos, 
echo                   white_circle_pos + white_circle_size, 
echo                   white_circle_pos + white_circle_size], 
echo                  fill='white'^)
echo     
echo     # Intentar usar una fuente del sistema o usar la predeterminada
echo     try:
echo         font_size = int^(size * 0.4^)
echo         font = ImageFont.truetype^("C:\\Windows\\Fonts\\arial.ttf", font_size^)
echo     except:
echo         font = ImageFont.load_default^(^)
echo     
echo     # Dibujar las letras "SD" en verde
echo     text = "SD"
echo     text_bbox = draw.textbbox^((0, 0^), text, font=font^)
echo     text_width = text_bbox[2] - text_bbox[0]
echo     text_height = text_bbox[3] - text_bbox[1]
echo     x = ^(size - text_width^) // 2
echo     y = ^(size - text_height^) // 2
echo     draw.text^((x, y^), text, fill=circle_color, font=font^)
echo     
echo     # Guardar el icono
echo     image.save^('spotdl.png', 'PNG'^)
echo.
echo if __name__ == '__main__':
echo     create_icon^(^)
) > create_icon.py

REM Generar el icono
echo Generando el icono...
python create_icon.py

REM Verificar si los archivos necesarios existen
if not exist "dist\spotdl.exe" (
    echo Error: No se pudo crear el ejecutable.
    pause
    exit /b 1
)

if not exist "spotdl.png" (
    echo Error: No se pudo crear el icono.
    pause
    exit /b 1
)

REM Crear acceso directo en el escritorio
echo Creando acceso directo en el escritorio...
set DESKTOP=%USERPROFILE%\Desktop
echo Set oWS = WScript.CreateObject^("WScript.Shell"^) > "%TEMP_DIR%\create_shortcut.vbs"
echo sLinkFile = "%DESKTOP%\SpotDL Music Downloader.lnk" >> "%TEMP_DIR%\create_shortcut.vbs"
echo Set oLink = oWS.CreateShortcut^(sLinkFile^) >> "%TEMP_DIR%\create_shortcut.vbs"
echo oLink.TargetPath = "%~dp0dist\spotdl.exe" >> "%TEMP_DIR%\create_shortcut.vbs"
echo oLink.IconLocation = "%~dp0spotdl.png" >> "%TEMP_DIR%\create_shortcut.vbs"
echo oLink.Save >> "%TEMP_DIR%\create_shortcut.vbs"
cscript //nologo "%TEMP_DIR%\create_shortcut.vbs"

REM Desactivar entorno virtual
deactivate

REM Limpiar archivos temporales
echo Limpiando archivos temporales...
rd /s /q "%TEMP_DIR%"

echo.
echo ¡Instalación completada!
echo Se ha creado un acceso directo en tu escritorio.
echo Puedes ejecutar la aplicación haciendo doble clic en el acceso directo.
echo.
pause