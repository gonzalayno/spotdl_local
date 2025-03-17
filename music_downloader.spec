# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_data_files

pykakasi_datas = collect_data_files('pykakasi')
spotdl_datas = collect_data_files('spotdl')

a = Analysis(
    ['music_downloader.py'],
    pathex=[],
    binaries=[],
    datas=pykakasi_datas + spotdl_datas,
    hiddenimports=['ttkthemes', 'PIL', 'requests', 'yt_dlp', 'random', 'time', 'pykakasi', 'spotdl'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='music_downloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
