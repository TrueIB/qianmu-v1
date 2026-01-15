from PIL import Image, ImageDraw, ImageFont
import random
import os


if __name__ == '__main__':
    # WIDTH, HEIGHT = 10000, 10000
    WIDTH, HEIGHT = 10000, 10000
    font = ImageFont.truetype('c:\windows\fonts\simsun.ttc', size=80)
    characters = []
    IMAGE_WIDTH = 100
    for i in range(19968, 40870):
    # for i in range(19968, 20000):
        characters.append(chr(i))
        print('\r', i, '汉字：', chr(i), '  已添加成功', end='')
    print('\n')
    if not os.path.exists('dataset'):
        os.makedirs('dataset')
    if not os.path.exists('dataset\\0'):
        os.makedirs('dataset\\0')
    if not os.path.exists('dataset\\0\\group1'):
        os.makedirs('dataset\\0\\group1')
    for epoch in range(10):
        # 生成图像
        print(f'正在生成第 {epoch + 1} / 10 张完整图像...')
        image = Image.new('L', (WIDTH, HEIGHT), color=255)
        draw = ImageDraw.Draw(image)
        for i in range(0, HEIGHT, 100):
            for j in range(0, WIDTH, 100):
                draw.text((i, j), random.choice(characters), font=font, fill='black')
        # 随机框选一些文字
        print('保存数据集...')
        for imagesCount in range(2000):
            pos = random.randint(0, WIDTH - IMAGE_WIDTH), random.randint(0, HEIGHT - IMAGE_WIDTH)
            tile = image.crop((*pos, pos[0] + IMAGE_WIDTH, pos[1] + IMAGE_WIDTH))
            tile_load = tile.load()
            for i in range(IMAGE_WIDTH):
                for j in range(IMAGE_WIDTH):
                    tile_load[i, j] = 0 if tile_load[i, j] < 150 else 255
            tile.save(f'dataset\\0\\group1\\{epoch * 2000 + imagesCount + 1}.png')
            print(f'\r处理并保存：{imagesCount + 1} / 2000', end='')
        print(f'第 {epoch} 张完整图像处理完成。')
    print(f'完成。')
    os.system('pause')
