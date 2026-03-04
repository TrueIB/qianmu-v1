import torch
from torchvision import transforms
from PIL import Image, ImageTk, ImageOps
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
import tkinter.filedialog as fdl
import model
import os


class main:
    def __init__(self, QModel, transform):
        self.QModel = QModel
        self.transform = transform
        self.TILE_WIDTH = 32

        self.window = tk.Tk()
        self.window.withdraw()
        self.window.title('千目-V1')
        self.window.iconbitmap('icon.ico')

        self.icon = tk.PhotoImage(file='icon.png')
        self.image = Image.new('RGB', (400, 200), (0, 0, 0))
        self.imageTk = ImageTk.PhotoImage(self.image)

        self.style = ttk.Style()
        self.style.configure(
            'TButton',
            font=('kaiti', 20),
            justify='center'
        )

        self.mainFrame = tk.Frame(self.window)

        self.startFrame = tk.Frame(self.mainFrame)
        tk.Label(
            self.startFrame,
            image=self.icon
        ).pack(pady=(30, 10))
        tk.Label(
            self.startFrame,
            text='千目-V1',
            font=('kaiti', 30)
        ).pack(pady=(0, 20))
        tk.Label(
            self.startFrame,
            text='一个用于去除图像中的手写文字的神经网络模型',
            font=('kaiti', 12)
        ).pack(padx=120)
        ttk.Button(
            self.startFrame,
            text='上传图片文件',
            width=15,
            command=self.upload_file
        ).pack(pady=(100, 30))
        self.startFrame.grid(
            row=0,
            column=0,
            sticky='nsew'
        )

        self.usedFrame = tk.Frame(self.mainFrame)
        self.imageLabel = tk.Label(
            self.usedFrame,
            image=self.imageTk
        )
        self.imageLabel.image = self.imageTk
        self.imageLabel.pack(pady=(50, 10))

        self.buttonsFrame = tk.Frame(self.usedFrame)
        ttk.Button(
            self.buttonsFrame,
            text='重新上传',
            width=15,
            command=self.openFile
        ).pack(pady=5)
        ttk.Button(
            self.buttonsFrame,
            text='去除手写',
            width=15,
            command=lambda: self.window.after(
                1,
                self.predict
            )
        ).pack(pady=5)
        ttk.Button(
            self.buttonsFrame,
            text='取消',
            width=15,
            command=lambda: self.moveFrame(
                self.mainFrame,
                False,
                self.usedFrame.winfo_width()
            )
        ).pack(pady=(5, 20))
        self.buttonsFrame.pack()

        self.progressFrame = tk.Frame(self.usedFrame)
        tk.Label(
            self.progressFrame,
            text='开始生成图像...',
            font=('kaiti', 20)
        ).pack()
        self.progressLabel = tk.Label(
            self.progressFrame,
            text='',
            font=('kaiti', 20)
        )
        self.progressLabel.pack()

        self.doneFrame = tk.Frame(self.usedFrame)
        tk.Label(
            self.doneFrame,
            text='✅ 完成！',
            font=('kaiti', 20)
        ).pack(pady=5)
        ttk.Button(
            self.doneFrame,
            text='保存图片',
            width=15,
            command=self.saveProcessedImage
        ).pack(pady=5)
        ttk.Button(
            self.doneFrame,
            text='返回',
            width=15,
            command=self.returnToMainPage
        ).pack(pady=(5, 20))

        self.usedFrame.grid(
            row=0,
            column=1,
            sticky='nsew'
        )
        self.mainFrame.place(x=0, y=0)

        self.window.update()

        self.SCREEN_SIZE = (
            max(
                self.startFrame.winfo_width(),
                self.usedFrame.winfo_width()
            ),
            max(
                self.startFrame.winfo_height(),
                self.usedFrame.winfo_height()
            )
        )

        geometry = (
            self.SCREEN_SIZE[0],
            self.SCREEN_SIZE[1],
            (self.window.winfo_screenwidth()
             - self.SCREEN_SIZE[0]) // 2,
            (self.window.winfo_screenheight()
             - self.SCREEN_SIZE[1]) // 2
        )
        self.window.geometry(
            f'{geometry[0]}x{geometry[1]}+'
            f'{geometry[2]}+{geometry[3]}'
        )
        self.window.resizable(False, False)

        self.mainFrame.place(
            x=0,
            y=0,
            width=self.SCREEN_SIZE[0] * 2,
            height=self.SCREEN_SIZE[1]
        )

        self.mainFrame.rowconfigure(0, weight=1)
        if (
            self.startFrame.winfo_width() >
            self.usedFrame.winfo_width()
        ):
            self.mainFrame.columnconfigure(
                1,
                weight=1
            )
        else:
            self.mainFrame.columnconfigure(
                0,
                weight=1
            )

        self.window.deiconify()
        self.window.mainloop()

    def returnToMainPage(self):
        self.doneFrame.pack_forget()
        self.buttonsFrame.pack()
        self.moveFrame(
            self.mainFrame,
            False,
            self.startFrame.winfo_width()
        )

    def saveProcessedImage(self):
        path = fdl.asksaveasfilename(
            filetypes=[
                ('JPG 文件', ('*.jpg', '*.jpeg')),
                ('PNG 文件', '*.png'),
                ('GIF 文件', '*.gif'),
                ('所有文件', '*.*')
            ],
            initialfile='未命名.jpg',
            defaultextension=".jpg",
            title='保存图片文件'
        )

        if path:
            try:
                self.image.save(path)
                msg.showinfo('保存成功', f'已保存至：{path}')
            except Exception:
                msg.showerror('错误', f'无法保存文件至：{path}')

    def predict(self):
        self.buttonsFrame.pack_forget()
        self.progressFrame.pack()
        if self.image.size[0] > 2000:
            self.image = self.image.resize((
                2000,
                (
                    self.image.size[1] * 2000 //
                    self.image.size[0]
                )
            ))
        if self.image.size[1] > 2000:
            self.image = self.image.resize((
                (
                    self.image.size[0] * 2000 //
                    self.image.size[1]
                ),
                2000
            ))
        self.image = self.image.resize((
            (
                self.image.size[0] + self.TILE_WIDTH -
                self.image.size[0] % self.TILE_WIDTH
            ),
            (
                self.image.size[1] + self.TILE_WIDTH -
                self.image.size[1] % self.TILE_WIDTH
            )
        ))

        count = 0
        self.image = ImageOps.invert(self.image)
        for i in range(
            0,
            self.image.size[0],
            self.TILE_WIDTH
        ):
            for j in range(
                0,
                self.image.size[1],
                self.TILE_WIDTH
            ):
                box = (
                    i,
                    j,
                    i + self.TILE_WIDTH,
                    j + self.TILE_WIDTH
                )
                tile = self.transform(
                    self.image.crop(box).convert('L')
                ).unsqueeze(0)

                if torch.argmax(
                    self.QModel(tile),
                    dim=1
                ).item():
                    self.imageProcessing(self.image, box)

                count += 1
                progress = round((
                    self.TILE_WIDTH ** 2 * 100 * count /
                    self.image.size[0] / self.image.size[1]
                ))
                self.progressLabel.configure(
                    text=f'当前进度：{progress}%'
                )
                self.window.update()
        self.image = ImageOps.invert(self.image)
        image_resize = self.image
        if self.image.size[0] > 400:
            image_resize = self.image.resize((
                400,
                (
                    self.image.size[1] *
                    400 // self.image.size[0]
                )
            ))

        if self.image.size[1] > 200:
            image_resize = self.image.resize((
                (
                    self.image.size[0] *
                    200 // self.image.size[1]
                ),
                200
            ))

        self.imageTk = ImageTk.PhotoImage(image_resize)
        self.imageLabel.configure(image=self.imageTk)
        self.imageLabel.image = self.imageTk
        self.progressFrame.pack_forget()
        self.doneFrame.pack()

    def get_mean(self, load):
        backgroundColor = 0
        count = 0

        for i in range(self.TILE_WIDTH):
            for j in range(self.TILE_WIDTH):
                if load[i, j] <= 145:
                    backgroundColor += load[i, j]
                    count += 1
        try:
            return int(backgroundColor / count)
        except Exception:
            return 0

    def imageProcessing(self, image, box):
        tile = image.crop(box).convert('L')
        load = tile.load()
        mean = self.get_mean(load)

        if mean != 0:
            tile = Image.new(
                'L',
                (self.TILE_WIDTH, self.TILE_WIDTH),
                mean
            )
        else:
            tile = Image.new(
                'L',
                (self.TILE_WIDTH, self.TILE_WIDTH),
                155
            )

        image.paste(tile, box)

    def upload_file(self):
        if self.openFile():
            self.moveFrame(
                self.mainFrame,
                True,
                self.startFrame.winfo_width()
            )

    def openFile(self):
        path = fdl.askopenfilename(
            filetypes=[
                ('JPG 文件', ('*.jpg', '*.jpeg')),
                ('PNG 文件', '*.png'),
                ('GIF 文件', '*.gif'),
                ('所有文件', '*.*')
            ],
            title='打开文件'
        )

        if not self.loadImage(path):
            if not path:
                return False
            msg.showerror('错误', f'无法打开文件：{path}')
            return False

        return True

    def loadImage(self, path):
        if not os.path.exists(path):
            return False

        try:
            self.image = Image.open(path).convert('L')
        except Exception:
            return False

        image_resize = self.image
        if self.image.size[0] > 400:
            image_resize = self.image.resize((
                400,
                (
                    self.image.size[1] *
                    400 // self.image.size[0]
                )
            ))

        if self.image.size[1] > 200:
            image_resize = self.image.resize((
                (
                    self.image.size[0] *
                    200 // self.image.size[1]
                ),
                200
            ))

        self.imageTk = ImageTk.PhotoImage(image_resize)
        self.imageLabel.configure(image=self.imageTk)
        self.imageLabel.image = self.imageTk
        return True

    def moveFrame(self, frame, direction, width):
        positions = []
        if direction:
            for i in range(1, width + 1, 15):
                positions.append(frame.winfo_x() - i)
            if width % 15 != 0:
                positions.append(frame.winfo_x() - width)
        else:
            for i in range(1, width + 1, 15):
                positions.append(frame.winfo_x() + i)
            if width % 15 != 0:
                positions.append(frame.winfo_x() + width)
        for position in positions:
            frame.place(x=position, y=frame.winfo_y())
            self.window.update()


if __name__ == '__main__':
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.5],
            std=[0.5]
        )
    ])

    QModel = model.model()
    QModel.load_state_dict(
        torch.load('qianmu-v1.pth', weights_only=True)
    )
    QModel.eval()
    main(QModel, transform)
