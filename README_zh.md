<h1 align="center">千目-V1</h1>

---

<p align="center"><a href="README.md">English</a> | 简体中文</p>

## 📃 1. 基本信息
- 开源许可：MIT
- 建立时间：2026年1月3日
- 编程语言：Python
- 项目描述：一个被用于去掉图片中手写内容的神经网络模型
- 使用到的第三方模块（按字母排序）：
  |  模块名称   | 用途                         | 文件                             |
  | :---------: | :--------------------------- | :------------------------------- |
  | matplotlib  | 绘制训练损失折线图           | train_test.py                    |
  |    numpy    | 数据集统计                   | train_test.py                    |
  |   pillow    | 处理图像                     | dataset_generation.py、main.py   |
  | pyinstaller | 将代码打包为exe              | /                                |
  |    torch    | 模型定义、模型训练、模型调用 | main.py、model.py、train_test.py |
  | torchvision | 数据集处理                   | main.py、train_test.py           |
- 开发人员：[TrueIB](https://gitee.com/TrueIB)（个人开发）

## 📄 2. 项目结构
```text
qianmu-v1/
├── .venv/                # Python 虚拟环境目录
├── .vscode/              # VS Code 编辑器生成的虚拟环境目录
├── __pycache__/
├── dataset/              # 数据集存放目录
│   ├── 0/                # 原数据集存放目录0
│   │   ├── 1.jpg
│   │   ├── 2.jpg
│   │   ├── 3.jpg
│   │   └── ...
│   ├── 1/                # 原数据集存放目录1
│   │   ├── 1.jpg
│   │   ├── 2.jpg
│   │   ├── 3.jpg
│   │   └── ...
│   ├── test/             # 测试数据集存放目录
│   │   ├── 0_1.png
│   │   ├── 0_2.png
│   │   ├── 0_3.png
│   │   └── ...
│   └── train/            # 训练数据集存放目录
│   │   ├── 0_1.png
│   │   ├── 0_2.png
│   │   ├── 0_3.png
│   │   └── ...
├── README.md             # 项目介绍文档（当前文件）
├── icon.png              # 项目图标 PNG 文件
├── losses.png            # 模型训练损失图文件
├── qianmu-v1.pth         # 模型文件
├── dataset_generation.py # 数据集生成程序文件
├── main.py               # 主程序文件
├── model.py              # 模型结构定义文件
├── train_test.py         # 模型训练、测试程序文件
├── icon.ico              # 图标文件
└── LICENCE               # 项目开源许可
```

# 💻 3. 数据集信息
- 来源：来自拍摄的图片随机裁剪得到
- 统计信息：
  |       统计信息       |  训练数据集 |  测试数据集 |
  | :------------------: | ----------: | ----------: |
  | 总图像数（单位：张） |     207,001 |     88,712 |
  | 总像素数（单位：个） | 211,969,024 | 90,841,088 |
  |   大小（单位：MB）   |      220.76 |       94.44 |
  |         均值         |    0.361402 |    0.361635 |
  |        标准差        |    0.152333 |    0.152518 |

## 🔑 4. 模型信息
- 实现模块：torch
- 模型定义：
```python
import torch.nn as nn
import torch.nn.functional as F


class model(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv1 = nn.Conv2d(1, 16, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(16)

        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(32)

        self.conv3 = nn.Conv2d(32, 64, 3, padding=1)
        self.bn3 = nn.BatchNorm2d(64)

        self.pool = nn.MaxPool2d(2, 2)

        self.fc1 = nn.Linear(4 * 4 * 64, 256)
        self.dropout1 = nn.Dropout(0.3)

        self.fc2 = nn.Linear(256, 128)
        self.dropout2 = nn.Dropout(0.2)

        self.fc3 = nn.Linear(128, 64)
        self.dropout3 = nn.Dropout(0.1)

        self.fc4 = nn.Linear(64, 2)

    def forward(self, x):
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        x = self.pool(F.relu(self.bn3(self.conv3(x))))

        x = x.view(-1, 4 * 4 * 64)

        x = F.relu(self.fc1(x))
        x = self.dropout1(x)

        x = F.relu(self.fc2(x))
        x = self.dropout2(x)

        x = F.relu(self.fc3(x))
        x = self.dropout3(x)

        x = self.fc4(x)
        return x

```

# 模型训练与测试
## 模型训练
- 训练轮数：12轮
- 模型损失图像：

  ![❌该图片无法显示](losses.png)
- 训练时长：3.92 h
## 模型测试
  - 平均损失：0.0985
  - 准确率：43118/44909（96.01%）

# 🔗 相关链接
这是一些对您可能有帮助的链接：
- 项目许可：[*MIT License*](LICENSE.txt)
- GitHub 项目地址：[*https://github.com/TrueIB/qianmu-v1/*](https://github.com/TrueIB/qianmu-v1/)
- Gitee 项目地址：[*https://gitee.com/TrueIB/qianmu-v1/*](https://gitee.com/TrueIB/qianmu-v1/)
- GitCode 项目地址：[*https://gitcode.com/TrueIB/qianmu-v1/*](https://gitcode.com/TrueIB/qianmu-v1/)
