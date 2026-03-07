import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from torch import optim
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import model
import time
import os


class ImageDataset(Dataset):
    def __init__(self, img_dir, transform=None):
        super().__init__()
        self.img_dir = img_dir
        self.transform = transform
        self.img_paths = [
            os.path.join(img_dir, f) for f in os.listdir(
                img_dir
            ) if f.endswith(('.png', '.jpg', '.jpeg'))
        ]

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, index):
        img_path = self.img_paths[index]
        try:
            image = Image.open(img_path).convert('L')
        except Exception as e:
            print(e)
            print(img_path)
            return (
                self.transform(
                    Image.new('L', (48, 48), 45)
                ),
                0
            )
        path_parts = []
        temp_path = img_path
        while temp_path and temp_path != os.path.sep:
            head, tail = os.path.split(temp_path)
            if tail:
                path_parts.insert(0, tail)
            temp_path = head
        label = 0 if path_parts[-1].startswith('0_') else 1
        if self.transform:
            image = self.transform(image)
        else:
            image = transforms.ToTensor()(image)
        return image, label


def calculate_gray_stats(
    dataset_path,
    batch_size=32,
    num_workers=4
):
    print('-' * 50)
    print('准备统计均值与标准差...')
    transform = transforms.Compose([
        transforms.ToTensor()
    ])

    dataset = ImageDataset(
        img_dir=dataset_path,
        transform=transform
    )

    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        shuffle=False
    )

    mean = 0.0
    std = 0.0
    total_pixels = 0
    n_batches = 0

    print('开始统计...')
    for batch_idx, (images, _) in enumerate(dataloader):
        batch_size_current = images.size(0)
        height, width = (
            images.size(2),
            images.size(3)
        )

        batch_pixels = (
            batch_size_current *
            height * width
        )

        batch_mean = images.mean().item()
        mean = ((
            (
                total_pixels * mean +
                batch_pixels * batch_mean
            ) / (
                total_pixels +
                batch_pixels
            )
        ))

        batch_std_squared = (
            (images - batch_mean) ** 2
        ).mean().item()
        std = ((
            (
                total_pixels * std + batch_pixels
                * batch_std_squared
            ) / (
                total_pixels +
                batch_pixels
            )
        ))

        total_pixels += batch_pixels
        n_batches += 1

        if (batch_idx + 1) % 10 == 0:
            print(
                f'\r已处理',
                f'{min((batch_idx + 1) * batch_size, len(dataset))}',
                f'/ {len(dataset)} 张图像',
                end=''
            )

    std = np.sqrt(std)
    print()
    print('-' * 50)
    print(f'数据集统计结果：')
    print(f' 总图像数：{len(dataset)}')
    print(f' 总像素数：{total_pixels}')
    print(f' 均值：{mean:.6f}')
    print(f' 标准差：{std:.6f}')
    print('-' * 50)
    os.system('pause')

    return float(f'{mean:.6f}'), float(f'{std:.6f}')


def train_model(
    model,
    train_loader,
    criterion,
    optimizer,
    epochs=20
):
    model.train()
    train_losses = []

    for epoch in range(epochs):
        running_loss = 0.0
        time_ = time.time()

        for batch_idx, (data, target) in enumerate(
            train_loader
        ):
            output = model(data)

            loss = criterion(output, target)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            print(f'\r{batch_idx % 100} / 100', end='')

            if batch_idx % 100 == 0:
                print(
                    f'\rEpoch: {epoch + 1} / {epochs} | '
                    f'Batch: {batch_idx + 1} / {len(train_loader)} | '
                    f'Loss: {loss.item():.4f} | '
                    f'Time: {time.time() - time_:.4f}'
                )
                train_losses.append(loss.item())
                if loss.item() < 0.005:
                    print('模型训练中止。')
                    return train_losses
                time_ = time.time()

        avg_loss = running_loss / len(train_loader)
        print(f'\rEpoch {epoch + 1} 平均损失: {avg_loss:.4f}')
    return train_losses


def test_model(
    model,
    test_loader,
    criterion
):
    model.eval()
    test_loss = 0
    correct = 0

    with torch.no_grad():
        for data, target in test_loader:
            output = model(data)
            test_loss += criterion(output, target).item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(
                target.view_as(pred)
            ).sum().item()

    test_loss /= len(test_loader)
    accuracy = 100. * correct / len(test_loader.dataset)

    print(f'\n测试结果:')
    print(f'平均损失: {test_loss:.4f}')
    print(
        f'准确率: {correct}/{len(test_loader.dataset)} '
        f'（{accuracy:.2f}%）'
    )

    return accuracy


if __name__ == '__main__':
    '''
    calculate_gray_stats('dataset/train')
    --------------------------------------------------
    数据集统计结果：
     总图像数：173510
     总像素数：177674240
     均值：0.362622  
     标准差：0.159764
    --------------------------------------------------

    calculate_gray_stats('dataset/test')
    --------------------------------------------------
    数据集统计结果：
     总图像数：74350
     总像素数：76134400
     均值：0.362762
     标准差：0.160077
    --------------------------------------------------
    '''

    train_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.5],
            std=[0.5]
        )
    ])

    test_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.5],
            std=[0.5]
        )
    ])

    train_dataset = ImageDataset(
        img_dir='dataset/train',
        transform=train_transform
    )

    test_dataset = ImageDataset(
        img_dir='dataset/test',
        transform=test_transform
    )

    QModel = model.model()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(QModel.parameters(), lr=0.00008)

    train_loader = DataLoader(
        train_dataset,
        batch_size=64,
        shuffle=True,
        num_workers=2
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=64,
        shuffle=False,
        num_workers=2
    )

    time_ = time.time()
    train_losses = train_model(
        model=QModel,
        train_loader=train_loader,
        criterion=criterion,
        optimizer=optimizer,
        epochs=2
    )
    time_ = time.time() - time_
    print(f'Time: {time_}')

    plt.plot(range(1, len(train_losses) + 1), train_losses)
    plt.title('Result')
    plt.xlabel('Time')
    plt.ylabel('Losses')
    plt.savefig('losses.png')
    plt.show()

    test_model(QModel, test_loader, criterion)
    torch.save(QModel.state_dict(), 'qianmu-v1.pth')
    print("✅ The model has been saved.")
    os.system('pause')
