from PIL import Image, ImageDraw


if __name__ == '__main__':
    image = Image.new('RGB', (1000, 1000), color='white')
    for i in range(19968, 40944):
        print(i, chr(i))
    image.show()
