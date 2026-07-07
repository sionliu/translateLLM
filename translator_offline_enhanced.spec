# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files

# 模型文件
model_binaries = [('hy-mt1.5-1.8b-q4_k_m.gguf', '.')]

# 收集 llama_cpp 的动态库
llama_binaries = collect_dynamic_libs('llama_cpp')

# NLTK 数据目录
NLTK_DATA_DIR = r"C:\Users\Administrator\AppData\Roaming\nltk_data"

a = Analysis(
    ['translator_offline_enhanced.py'],
    pathex=[],
    binaries=model_binaries + llama_binaries,
    datas=[
        (NLTK_DATA_DIR, 'nltk_data'),
    ],
    hiddenimports=[
        'pyttsx3.drivers',
        'pyttsx3.drivers.sapi5',
        'offline_dictionary',
        'nltk',
        'nltk.corpus',
        'nltk.corpus.wordnet',
        'nltk.corpus.cmudict',
        'llama_cpp',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter.test',
        'unittest',
        'pdb',
        'test',
    ],
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
    name='小D单词翻译器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
