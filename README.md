<h1 align="center">Qianmu-V1</h1>

<p align="center">
  <b>English</b> | <a href="README_zh.md">简体中文</a>
</p>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-1.9+-red.svg)](https://pytorch.org/)

</div>

## 📌 Introduction

**Qianmu-V1** is a lightweight binary classification convolutional neural network implemented with PyTorch, designed to determine whether an image contains handwritten content. The project provides a complete pipeline for dataset generation, model training, testing, and inference, suitable for scenarios such as handwriting removal.

**Specific implementation for handwriting removal:** The image is segmented into many 32×32 patches, and the model judges each patch to decide whether to remove it.

---

## 📅 Basic Information

- **Development Period**: 2026.01.03 – 2026.03.07  
- **Programming Language**: Python 3.8+  
- **Project Type**: Image Classification (Binary: with handwriting / without handwriting)  
- **Developer**: [TrueIB](https://gitee.com/TrueIB) (Personal Project)

---

## 📁 Project Structure

```text
qianmu-v1/
├── dataset/               # Dataset directory
│   ├── 0/                 # Raw dataset class 0: images without handwriting
│   │   ├── 1.jpg
│   │   ├── 2.jpg
│   │   └── ...
│   └── 1/                 # Raw dataset class 1: images with handwriting
│       ├── 1.jpg
│       ├── 2.jpg
│       └── ...
├── README.md              # Project documentation (this file)
├── README_zh.md              # Project Chinese documentation
├── icon.png               # Project icon (PNG)
├── icon.ico               # Project icon (ICO)
├── losses.png             # Training loss curve
├── qianmu-v1.pth          # Pre-trained model weights
├── dataset_generation.py  # Dataset generation script
├── main.py                # Main program (inference/demo)
├── model.py               # Model definition
├── train_test.py          # Training and testing script
├── LICENSE.txt            # MIT License
└── requirements.txt       # Project dependencies
```

---

## 💾 Dataset Information

### Source
Images were captured from real-world scenes (examination papers, books, exercise books, etc.) using a mobile phone, then randomly cropped to a uniform size (32×32 grayscale). The dataset is organized into `dataset/0/` (without handwriting) and `dataset/1/` (with handwriting) and randomly split into training and test sets with a ratio of 7:3.

### Statistics

| Metric                      | Training Set | Test Set    |
|-----------------------------|--------------|-------------|
| Total images                | 173,510      | 44,909      |
| Total pixels                | 177,674,240  | 45,986,816  |
| Storage space (MB)          | 550          | 235         |
| Pixel mean (before scaling) | 0.3626       | 0.3628      |
| Pixel std (before scaling)  | 0.1598       | 0.1601      |

> **Note**: Pixel values have been scaled to the [0,1] range; mean and standard deviation are computed over all image pixels.

---

## 🧠 Model

### 4.1 Model Architecture

- **Framework**: PyTorch
- **Input Size**: 1×32×32 (grayscale)
- **Output**: 2-dimensional vector (logits for each class)
- **Network Structure**:

```python
import torch.nn as nn


class model(nn.Module):
    def __init__(self):
        super(model, self).__init__()
        self.featureExtract = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2)
        )
        
        self.makeDecisions = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.5),
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(256, 2)
        )

    def forward(self, x):
        x = self.featureExtract(x)
        x = self.makeDecisions(x)
        return x

```

### 4.2 Training Configuration

- **Optimizer**: Adam (default parameters)
- **Loss Function**: Cross-entropy loss
- **Batch Size**: 64
- **Epochs**: 2
- **Hardware**: NVIDIA GeForce RTX 3060 (12GB)

#### Training Loss Curve
![Training Loss Curve](losses.png)  
*Figure: Loss values over training iterations*

### 4.3 Test Results

- **Test Set Size**: 44,909 images
- **Average Loss**: 0.0985
- **Classification Accuracy**: 43,118 / 44,909 ≈ **96.01%**

---

## 📦 Dependency Installation

All dependencies are listed in [requirements.txt](requirements.txt). It is recommended to install them in a Python virtual environment:

```bash
pip install -r requirements.txt
```

Main dependencies:
- torch >= 1.9.0
- torchvision
- numpy
- pillow
- matplotlib (for plotting loss curves)

---

## 🚀 Quick Start

### 1. Dataset Preparation
- Place images into `dataset/0/` (without handwriting) and `dataset/1/` (with handwriting) according to their classes.
- Run `dataset_generation.py` for preprocessing and splitting.

### 2. Train the Model
```bash
python train_test.py --mode train_model
```

### 3. Test the Model
```bash
python train_test.py --mode test_model
```

### 4. Single Image Inference
```python
from model import model
from PIL import Image
import torchvision.transforms as transforms

QModel = model()
QModel.load_state_dict(torch.load('qianmu-v1.pth'))
QModel.eval()

img = Image.open('example.jpg').convert('L').resize((32, 32))
tensor = transforms.ToTensor()(img).unsqueeze(0)
with torch.no_grad():
    output = QModel(tensor)
    pred = output.argmax(dim=1).item()
print("With handwriting" if pred == 1 else "Without handwriting")
```

---

## 🔗 Related Links

- **Project License**: [MIT License](LICENSE.txt)
- **GitHub Repository**: [https://github.com/TrueIB/qianmu-v1/](https://github.com/TrueIB/qianmu-v1/)
- **Gitee Repository**: [https://gitee.com/TrueIB/qianmu-v1/](https://gitee.com/TrueIB/qianmu-v1/)
- **GitCode Repository**: [https://gitcode.com/TrueIB/qianmu-v1/](https://gitcode.com/TrueIB/qianmu-v1/)

---

## ❌ Known Issues

The current model performs poorly in handwriting removal tasks. This will be improved in **Qianmu-V2** using a U-Net architecture.

## 📬 Feedback & Contributions

Issues and Pull Requests are welcome. If you encounter any problems, please provide detailed logs and your runtime environment.

---

**Revision Notes**  
- Corrected the test set size in dataset statistics to be consistent with the accuracy denominator (now unified as 44,909).  
- Clarified dataset class meanings (0 = without handwriting, 1 = with handwriting).  
- Fixed the dependency installation command to `pip install -r requirements.txt`.  
- Added a "Quick Start" section with inference example code.  
- Added badges and improved formatting for better readability.
