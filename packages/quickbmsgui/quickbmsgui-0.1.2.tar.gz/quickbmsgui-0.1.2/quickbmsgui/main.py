import importlib.resources
import subprocess
import threading
import tkinter as tk
from threading import Thread
from tkinter import filedialog, scrolledtext


def select_file():
    # 打开文件选择对话框
    path = filedialog.askopenfilename()
    return path
def on_button1_click():
    p = select_file()
    if p:
        bms_script_path.delete(0,tk.END)
        bms_script_path.insert(0,p)
def on_button2_click():
    p = select_file()
    if p:
        file_path.delete(0, tk.END)
        file_path.insert(0, p)
def on_button22_click():
    p = filedialog.askdirectory()
    if p:
        file_path.delete(0, tk.END)
        file_path.insert(0, p)
def on_button3_click():
    p = filedialog.askdirectory()
    if p:
        out_path.delete(0, tk.END)
        out_path.insert(0, p)

def run_long_process(command):
    # 启动进程
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        errors='ignore'  # 忽略解码错误
    )

    # 实时读取输出
    try:
        while True:
            output = process.stdout.readline()
            if output:
                # 在 Tkinter 界面上显示输出
                text_area.insert(tk.END, output.strip() + '\n')
                text_area.see(tk.END)  # 滚动到最后一行

            # 检查进程是否结束
            if process.poll() is not None:
                break

        # 获取任何剩余的输出
        remaining_output, remaining_error = process.communicate()
        if remaining_output:
            text_area.insert(tk.END, remaining_output.strip() + '\n')
        if remaining_error:
            text_area.insert(tk.END, remaining_error.strip() + '\n')

    except Exception as e:
        text_area.insert(tk.END, f"错误: {str(e)}\n")

def view_list():
    path = importlib.resources.files("quickbmsgui.tools").joinpath("quickbms_4gb_files.exe")
    cmd = [path, "-l",bms_script_path.get(),file_path.get()
           ,out_path.get()]
    threading.Thread(target=run_long_process,args=(cmd,), daemon=True).start()
def unpack_d():
    path = importlib.resources.files("quickbmsgui.tools").joinpath("quickbms_4gb_files.exe")
    cmd = [path, bms_script_path.get(), file_path.get()
        , out_path.get()]
    threading.Thread(target=run_long_process, args=(cmd,), daemon=True).start()
# 创建主窗口
root = tk.Tk()
root.title("quickbms简单gui")
#root.geometry("800x500")  # 设置窗口大小

#选择脚本
frame1 = tk.Frame(root)
bms_script_path = tk.Entry(frame1,width=50)
button1 = tk.Button(frame1,text="选择脚本",command=on_button1_click)
bms_script_path.pack(side=tk.LEFT)
button1.pack(side=tk.LEFT)
frame1.pack()

frame2 = tk.Frame(root)
file_path = tk.Entry(frame2,width=50)
button2 = tk.Button(frame2,text="文件",command=on_button2_click)
button22 = tk.Button(frame2,text="选择文件夹",command=on_button22_click)
file_path.pack(side = tk.LEFT)
button2.pack(side=tk.LEFT)
button22.pack(side=tk.LEFT)
frame2.pack()

frame3 = tk.Frame(root)
out_path = tk.Entry(frame3,width=50)
button3 = tk.Button(frame3,text="输出",command=on_button3_click)
out_path.pack(side=tk.LEFT)
button3.pack(side=tk.LEFT)
frame3.pack()

#
frame4 = tk.Frame(root)
button_unpack = tk.Button(frame4,text="解压",command=unpack_d)
button_unpack.pack(side=tk.LEFT)
button_list = tk.Button(frame4,text="查看列表",command=view_list)
button_list.pack(side=tk.LEFT)
frame4.pack()

frame5 = tk.Frame(root)
text_area = scrolledtext.ScrolledText(frame5, wrap=tk.WORD, width=100, height=20)
text_area.pack(padx=10, pady=10)
frame5.pack()


# 启动事件循环
root.mainloop()