"""
PyInstaller hook for llama_cpp
确保动态库被正确收集
"""
from PyInstaller.utils.hooks import collect_dynamic_libs

# 收集 llama_cpp 目录下的所有 DLL
binaries = collect_dynamic_libs('llama_cpp')
