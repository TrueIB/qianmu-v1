import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import os


class ImageDataset(Dataset):
    def __init__(self, img_dir, transform=None):
        super().__init__()
        self.img_dir = img_dir
        self.transform = transform
        self.img_paths = [os.path.join(img_dir, f) for f in os.listdir(
            img_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, index):
        img_path = self.img_paths[index]
        image = Image.open(img_path).convert('L')
        path_parts = []
        temp_path = img_path
        while temp_path and temp_path != os.path.sep:
            head, tail = os.path.split(temp_path)
            if tail:
                path_parts.insert(0, tail)
            temp_path = head
        label = 0 if '0' in temp_path else 1
        if self.transform:
            image = self.transform(image)
        return image, label




if __name__ == '__main__':
    pass
