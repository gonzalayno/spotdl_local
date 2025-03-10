#!/bin/bash
echo "Instalando dependencias..."
python3 -m pip install -r requirements.txt
echo "Dependencias instaladas."
echo "Ejecutando la aplicación..."
python3 music_downloader.py