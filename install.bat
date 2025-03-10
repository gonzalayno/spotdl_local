@echo off
echo Instalando dependencias...
python -m pip install -r requirements.txt
echo Dependencias instaladas.
echo Ejecutando la aplicación...
python music_downloader.py
pause