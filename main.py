import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
import tkinter.filedialog as fdl
# import torch
# import model


class main:
    def __init__(self):
        self.window = tk.Tk()
        self.icon = tk.PhotoImage(file='icon.png')
        self.image = None
        self.style = ttk.Style()
        self.style.configure('TButton', font=('kaiti', 20), justify='center')
        self.window.title('千目-V1')
        self.mainFrame = tk.Frame(self.window)
        self.startFrame = tk.Frame(self.mainFrame)
        tk.Label(self.startFrame, image=self.icon).pack(pady=(30, 10))
        tk.Label(self.startFrame, text='千目-V1', font=('kaiti', 30)).pack(pady=(0, 20))
        tk.Label(self.startFrame, text='一个用于去除图像中的手写文字的神经网络模型', font=('kaiti', 12)).pack(padx=120)
        ttk.Button(self.startFrame, text='上传图片文件', width=15, command=self.openFile).pack(pady=(100, 30))
        self.startFrame.grid(row=0, column=0)
        # self.mainFrame.place(x=0, y=0)
        self.usedFrame = tk.Frame(self.mainFrame)
        self.usedFrame.grid(row=0, column=1)
        self.mainFrame.pack()
        self.window.resizable(False, False)
        self.window.mainloop()

    def openFile(self):
        path = fdl.askopenfilename(filetypes = [('打开文件', '*.png')])


if __name__ == '__main__':
    main()
