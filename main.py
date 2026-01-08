import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
import tkinter.filedialog as fdl
# import torch
# import model
import time


class main:
    def __init__(self):
        self.window = tk.Tk()
        self.icon = tk.PhotoImage(file='icon.png')
        self.image = tk.PhotoImage(file='example.png')
        self.style = ttk.Style()
        self.style.configure('TButton', font=('kaiti', 20), justify='center')
        self.window.title('千目-V1')
        self.window.iconbitmap('icon.ico')
        self.window.withdraw()
        self.mainFrame = tk.Frame(self.window)
        self.startFrame = tk.Frame(self.mainFrame)
        tk.Label(self.startFrame, image=self.icon).pack(pady=(30, 10))
        tk.Label(self.startFrame, text='千目-V1', font=('kaiti', 30)).pack(pady=(0, 20))
        tk.Label(self.startFrame, text='一个用于去除图像中的手写文字的神经网络模型', font=('kaiti', 12)).pack(padx=120)
        ttk.Button(self.startFrame, text='上传图片文件', width=15, command=self.openFile).pack(pady=(100, 30))
        self.startFrame.grid(row=0, column=0)
        self.usedFrame = tk.Frame(self.mainFrame)
        self.imageLabel = tk.Label(self.usedFrame, image=self.image)
        self.imageLabel.pack(anchor='n')
        self.usedFrame.grid(row=0, column=1)
        self.mainFrame.place(x=0, y=0)
        self.window.update()
        self.SCREEN_SIZE = max(self.startFrame.winfo_width(), self.usedFrame.winfo_width()), max(self.startFrame.winfo_height(), self.usedFrame.winfo_height())
        self.window.geometry(f'{self.SCREEN_SIZE[0]}x{self.SCREEN_SIZE[1]}+{(self.window.winfo_screenwidth() - self.SCREEN_SIZE[0]) // 2}+{(self.window.winfo_screenheight() - self.SCREEN_SIZE[1]) // 2}')
        self.window.resizable(False, False)
        self.startFrame.configure(width=self.SCREEN_SIZE[0], height=self.SCREEN_SIZE[1])
        self.usedFrame.configure(width=self.SCREEN_SIZE[0], height=self.SCREEN_SIZE[1])
        self.usedFrame.grid(row=0, column=1)
        self.window.deiconify()
        self.window.mainloop()

    def openFile(self):
        path = fdl.askopenfilename(filetypes = [('打开文件', '*.png')])
        if not self.loadImage(path):
            msg.showerror('错误', '找不到指定路径')
            return
        self.moveFrame(self.mainFrame, True, self.startFrame.winfo_width())

    def loadImage(self, path):
        return True

    def moveFrame(self, frame, direction, width):
        positions = []
        if direction:
            for i in range(1, width + 1, 4):
                positions.append((frame.winfo_x() - i, frame.winfo_y()))
            if width // 4 != 0:
                positions.append((frame.winfo_x() - width, frame.winfo_y()))
        else:
            for i in range(1, width + 1, 4):
                positions.append((frame.winfo_x() + i, frame.winfo_y()))
            if width // 4 != 0:
                positions.append((frame.winfo_x() + width, frame.winfo_y()))
        for position in positions:
            frame.place(x=position[0], y=position[1])
            self.window.update()
        print(self.SCREEN_SIZE)
        print(self.usedFrame.winfo_width())


if __name__ == '__main__':
    main()
