# main.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['C:\\Users\\Swarajh Mehta\\Desktop\\Projects\\gitincis\\Incis'],
    binaries=[('C:\\Users\\Swarajh Mehta\\Desktop\\Projects\\gitincis\\Incis\\venv\\Lib\\site-packages\\pywin32_system32\\pywintypes310.dll', '.')],
    datas=[('last.jpg', '.'), ('C:\\Program Files\\Tesseract-OCR\\tesseract.exe', '.')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False to remove the console window
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
