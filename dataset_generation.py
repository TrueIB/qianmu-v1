from PIL import Image, ImageDraw, ImageFont
import random
import numpy
import os


if __name__ == '__main__':
    WIDTH, HEIGHT = 10000, 10000
    image = Image.new('L', (WIDTH, HEIGHT), color=255)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('c:\windows\fonts\simsun.ttc', size=60)
    characters = []
    IMAGE_WIDTH = 100
    for i in range(19968, 40870): 
        characters.append(chr(i))
        print('\r', i, '汉字：', chr(i), '已添加成功', end='')
    for i in range(0, HEIGHT, 100):
        for j in range(0, WIDTH, 100):
            draw.text((i, j), random.choice(characters), font=font, fill='black')
    load = image.load()
    for i in range(HEIGHT):
        for j in range(WIDTH):
            load[i, j] = 0 if load[i, j] < 50 else 255
    #os.system('pause')
    image.save('dataset_example.png')
    image.show()
