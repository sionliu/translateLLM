import tkinter as tk
from tkinter import messagebox
import re
import sys
import threading
import pyttsx3
from llama_cpp import Llama
from offline_dictionary import lookup_dict



# ---------- 模型加载 ----------
MODEL_PATH = "./hy-mt1.5-1.8b-q4_k_m.gguf"   # 改成你实际的 gguf 文件名
try:
    llm = Llama(model_path=MODEL_PATH, n_ctx=2048, verbose=False)
except Exception as e:
    messagebox.showerror("致命错误", f"模型加载失败: {e}")
    sys.exit(1)

# ---------- 语音类（线程安全）----------
class SpeechEngine:
    def speak(self, text, lang="en"):
        def _run():
            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', 150)
                voices = engine.getProperty('voices')
                target = None
                for v in voices:
                    if lang == "zh" and "chinese" in v.name.lower():
                        target = v; break
                    elif lang == "en" and "english" in v.name.lower():
                        target = v; break
                if target:
                    engine.setProperty('voice', target.id)
                engine.say(text)
                engine.runAndWait()
                engine.stop()
            except Exception:
                pass
        t = threading.Thread(target=_run, daemon=True)
        t.start()

speaker = SpeechEngine()

# ---------- 语言检测 ----------
def detect_language(text):
    return "zh" if re.search(r'[\u4e00-\u9fff]+', text) else "en"

# ---------- 翻译（模型只做纯翻译，词性/音标/例句由离线词典提供）----------

def translate_with_example(text, direction="zh"):
    if not text:
        return "", "", "", "", ""

    # 纯翻译提示词（简洁直接，适合翻译模型）
    if direction == "zh":
        prompt = f"English: {text}\nChinese:"
    else:
        prompt = f"Chinese: {text}\nEnglish:"

    try:
        output = llm(prompt, max_tokens=256, stop=["\n\n"], echo=False)
        raw = output['choices'][0]['text'].strip()
    except Exception as e:
        messagebox.showerror("翻译错误", f"模型调用失败: {e}")
        return "", "", "", "", ""

    translation = raw

    # 如果是英译中且输入是单个单词，查离线词典获取词性/音标/例句
    phonetic = ""
    pos = ""
    example_en = ""
    example_zh = ""
    if direction == "zh" and len(text.split()) <= 2:
        phonetic, pos, example_en, _ = lookup_dict(text)
        # 如果有英文例句，用模型翻译成中文
        if example_en:
            try:
                # 更明确的翻译指令，强制输出中文
                ex_prompt = f"Translate the following English sentence into Chinese (only output Chinese, no English):\n{example_en}\nChinese:"
                ex_output = llm(ex_prompt, max_tokens=128, stop=["\n\n"], echo=False)
                example_zh = ex_output['choices'][0]['text'].strip()
                # 如果输出仍然是英文（不含中文字符），尝试用更简洁的提示词重试一次
                if example_zh and not re.search(r'[\u4e00-\u9fff]+', example_zh):
                    ex_prompt2 = f"English: {example_en}\nChinese:"
                    ex_output2 = llm(ex_prompt2, max_tokens=128, stop=["\n\n"], echo=False)
                    example_zh = ex_output2['choices'][0]['text'].strip()
            except Exception:
                example_zh = ""


    return translation, phonetic, pos, example_en, example_zh











# ---------- GUI 回调 ----------
def do_translate():
    text = input_box.get("1.0", tk.END).strip()
    if not text:
        return
    lang = detect_language(text)
    direction = "zh" if lang == "en" else "en"
    trans, phonetic, pos, ex_en, ex_zh = translate_with_example(text, direction)

    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    # 翻译
    output_box.insert(tk.END, f"翻译：{trans}\n", "trans")
    # 音标（仅英译中时）
    if phonetic:
        output_box.insert(tk.END, f"音标：{phonetic}\n", "phonetic")
    # 词性
    if pos:
        output_box.insert(tk.END, f"词性：{pos}\n", "pos")
    # 例句
    if ex_en:
        output_box.insert(tk.END, f"\n例句：{ex_en}\n", "ex_en")
    if ex_zh:
        output_box.insert(tk.END, f"例句翻译：{ex_zh}", "ex_zh")
    output_box.config(state=tk.DISABLED)


def do_speak():
    text = input_box.get("1.0", tk.END).strip()
    if not text:
        return
    lang = detect_language(text)
    speaker.speak(text, lang)

# ---------- 界面搭建（修正布局）----------
root = tk.Tk()
root.title("小D单词翻译器 (离线·增强版)")
root.geometry("700x500")
root.minsize(600, 400)

# 主容器，不设置 expand，用 grid 控制比例
root.grid_rowconfigure(0, weight=1)   # 上方区域可拉伸
root.grid_rowconfigure(1, weight=0)   # 按钮行固定高度
root.grid_columnconfigure(0, weight=1)

top_frame = tk.Frame(root)
top_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10,5))

btn_frame = tk.Frame(root)
btn_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,10))

# 上部分为左右两个 LabelFrame
top_frame.grid_columnconfigure(0, weight=1)
top_frame.grid_columnconfigure(1, weight=1)
top_frame.grid_rowconfigure(0, weight=1)

input_frame = tk.LabelFrame(top_frame, text="输入单词/句子", font=("微软雅黑", 11))
input_frame.grid(row=0, column=0, sticky="nsew", padx=(0,5))
input_box = tk.Text(input_frame, wrap=tk.WORD, font=("微软雅黑", 12), relief=tk.FLAT)
input_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

output_frame = tk.LabelFrame(top_frame, text="翻译结果", font=("微软雅黑", 11))
output_frame.grid(row=0, column=1, sticky="nsew", padx=(5,0))
output_box = tk.Text(output_frame, wrap=tk.WORD, font=("微软雅黑", 12), state=tk.DISABLED)
output_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# 样式标签
output_box.tag_config("trans", font=("微软雅黑", 12, "bold"), foreground="#1a1a1a")
output_box.tag_config("phonetic", font=("微软雅黑", 11), foreground="#8B4513")
output_box.tag_config("pos", font=("微软雅黑", 11, "italic"), foreground="#2d6a4f")
output_box.tag_config("ex_en", font=("微软雅黑", 11, "italic"), foreground="#555555")
output_box.tag_config("ex_zh", font=("微软雅黑", 11), foreground="#2d6a4f")


# 底部按钮
speak_btn = tk.Button(btn_frame, text="🔊 朗读", command=do_speak,
                      font=("微软雅黑", 11), width=10)
speak_btn.pack(side=tk.LEFT, padx=5)

translate_btn = tk.Button(btn_frame, text="翻译", command=do_translate,
                          font=("微软雅黑", 12, "bold"), bg="#4CAF50", fg="white", width=10)
translate_btn.pack(side=tk.LEFT, padx=5)

root.mainloop()