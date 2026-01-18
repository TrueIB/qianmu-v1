from PIL import Image
import random
import os


if __name__ == '__main__':
    IMAGE_WIDTH = 100
    if not os.path.exists('..\\dataset\\train\\0\\group2'):
        os.makedirs('..\\dataset\\train\\0\\group2')
    for imagesCount in range(1, 22):
        print(f'\n开始处理第 {imagesCount} 张图像...')
        image = Image.open(f'.\\dataset\\train\\0\\group2_new\\{imagesCount}.jpg').convert('L')
        load = image.load()
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                load[i, j] = 0 if load[i, j] < 150 else 255
        for epoch in range(1200):
            pos = random.randint(0, image.size[0] - IMAGE_WIDTH), random.randint(0, image.size[1] - IMAGE_WIDTH)
            tile = image.crop((*pos, pos[0] + IMAGE_WIDTH, pos[1] + IMAGE_WIDTH))
            tile.save(f'..\\dataset\\train\\0\\group2\\{epoch + imagesCount * 1200}.png')
            print(f'\r{epoch + 1} / 1200', end='')
