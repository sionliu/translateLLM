# translateLLM

English Introduction:

This is an offline LLM translation tool (Windows version) based on local CPU, primarily designed to solve the problem of children looking up English words without an internet connection. It can be downloaded and used directly, or the source code can be downloaded and compiled for use. Parents with similar needs are welcome to download and use it.

If you need to compile the source files yourself, you can first install and configure your Python environment locally, download the Tencent HunYuan model hy-mt1.5-1.8b-q4_k_m.gguf, and run `python build_package.py` in the console. This will generate an executable file—translateLLM.exe—in the dist directory. The executable file does not require installation; simply place the model file in the same directory to run it directly.

The Tencent HunYuan model is quite large; please download it yourself from: https://huggingface.co/Tencent-HunYuan/HY-MT1.5-1.8B-GGUF/resolve/main/hy-mt1.5-1.8b-q4_k_m.gguf

中文说明：

这是一个基于本地CPU的离线LLM翻译工具（Windows版本），主要设计用于解决儿童在没有网络连接的情况下查找英语单词的问题。您可以直接下载使用，也可以下载源代码并编译后使用。欢迎有类似需求的家长下载使用。

如果需要自行编译源文件，可以先在本地安装配置好python环境，下载腾讯混元模型 hy-mt1.5-1.8b-q4_k_m.gguf，并在控制台运行 python build_package.py，会在dist目录下生成可执行文件——translateLLM.exe。可执行文件无需安装，只需要将模型文件放在相同目录即可直接运行。

腾讯混元模型较大，请自行下载，地址为：https://huggingface.co/Tencent-HunYuan/HY-MT1.5-1.8B-GGUF/resolve/main/hy-mt1.5-1.8b-q4_k_m.gguf
