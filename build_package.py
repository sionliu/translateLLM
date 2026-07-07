"""
打包脚本 - 将翻译器打包分享给家人
运行方式: python build_package.py

打包后会在 dist/ 目录生成 "translateLLM" 文件夹，
里面包含 exe 和模型文件，复制整个文件夹即可分享。
"""
import os
import sys
import subprocess

# NLTK 数据目录
NLTK_DATA_DIR = r"C:\Users\Administrator\AppData\Roaming\nltk_data"

if not os.path.exists(NLTK_DATA_DIR):
    print(f"❌ 找不到 NLTK 数据目录: {NLTK_DATA_DIR}")
    print("请先运行: python -c \"import nltk; nltk.download('wordnet'); nltk.download('cmudict')\"")
    sys.exit(1)

print(f"NLTK 数据目录: {NLTK_DATA_DIR}")

# 构建 PyInstaller 命令
cmd = [
    "pyinstaller",
    "--noconfirm",
    "--onedir",
    "--windowed",
    "--name", "translateLLM",
    # 收集 llama_cpp 所有文件（包括 lib 目录下的 DLL）
    "--collect-all", "llama_cpp",
    # 添加模型文件
    f"--add-data", f"hy-mt1.5-1.8b-q4_k_m.gguf;.",
    # 添加 NLTK 数据
    f"--add-data", f"{NLTK_DATA_DIR};nltk_data",
    # 隐藏导入
    "--hidden-import", "pyttsx3.drivers",
    "--hidden-import", "pyttsx3.drivers.sapi5",
    "--hidden-import", "offline_dictionary",
    "--hidden-import", "nltk",
    "--hidden-import", "nltk.corpus",

    # 排除不需要的
    "--exclude-module", "tkinter.test",
    "--exclude-module", "unittest",
    "--exclude-module", "pdb",
    "--exclude-module", "test",
    # 主程序
    "translator_offline_enhanced.py"
]

print("开始打包...")
result = subprocess.run(cmd, shell=True)

if result.returncode == 0:
    dist_dir = os.path.join("dist", "translateLLM")
    model_file = "hy-mt1.5-1.8b-q4_k_m.gguf"
    
    # 复制模型文件到输出目录
    import shutil
    if os.path.exists(model_file):
        shutil.copy2(model_file, os.path.join(dist_dir, model_file))
        print(f"✅ 模型文件已复制: {model_file}")
    
    # 检查 llama_cpp 的 lib 目录是否在打包结果中
    internal_dir = os.path.join(dist_dir, "_internal")
    llama_lib_dir = os.path.join(internal_dir, "llama_cpp", "lib")
    if os.path.exists(llama_lib_dir):
        print(f"✅ llama_cpp 库文件已包含: {llama_lib_dir}")
        for f in os.listdir(llama_lib_dir):
            print(f"   - {f}")
    else:
        print(f"⚠️  llama_cpp/lib 目录未找到，尝试查找...")
        # 搜索 DLL 文件
        for root, dirs, files in os.walk(internal_dir):
            for f in files:
                if f.endswith('.dll'):
                    print(f"   找到 DLL: {os.path.join(root, f)}")
    
    # 计算总大小
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(dist_dir):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    
    print(f"\n{'='*50}")
    print(f"✅ 打包成功！")
    print(f"📂 输出文件夹: {os.path.abspath(dist_dir)}")
    print(f"📏 总大小: {total_size / 1024 / 1024:.1f} MB")
    print(f"\n📋 分享方法：")
    print(f"   1. 将整个文件夹复制到U盘或压缩成zip")
    print(f"   2. 家人收到后，双击运行 'translateLLM.exe' 即可")
    print(f"   3. 无需安装 Python 或任何依赖")
    print(f"{'='*50}")
else:
    print(f"\n❌ 打包失败，错误码: {result.returncode}")
