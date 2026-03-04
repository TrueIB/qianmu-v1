from PIL import Image, ImageOps
import random
import os


def dataset_generation(
    inputDir,
    outputDir,
    imageWidth=32,
    multiple=10,
    prefix=''
):
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    imagesWalk = os.walk(inputDir)
    for _, _, imagePaths in imagesWalk:
        break
    count = 0
    for imagesCount, imagePath in enumerate(imagePaths):
        print(
            f'\n开始处理{imagePath}',
            f'（{imagesCount + 1} / {len(imagePaths)}）...',
            sep=''
        )
        image = Image.open(
            f'{inputDir}/{imagePath}'
        ).convert('L')
        width, height = image.size

        widthList = [
            width,
            width,
            width
        ]
        heightList = [
            height,
            height,
            height
        ]

        total = int(
            (width * height * multiple /
             imageWidth / imageWidth)
        )
        for idx in range(len(widthList)):
            if (widthList[idx] < imageWidth or
                heightList[idx] < imageWidth):
                continue
            image = image.resize((
                widthList[idx],
                heightList[idx]
            ))
            for epoch in range(total):
                pos = (
                    random.randint(
                        0,
                        image.size[0] - imageWidth
                    ),
                    random.randint(
                        0,
                        image.size[1] - imageWidth
                    )
                )
                tile = image.crop((
                    *pos,
                    pos[0] + imageWidth,
                    pos[1] + imageWidth
                ))
                count += 1
                if prefix.startswith('1'):
                    white = 0
                    tile_load = tile.load()
                    for i in range(tile.size[0]):
                        for j in range(tile.size[1]):
                            if tile_load[i, j] < 170:
                                white += 1
                    if (
                        white >=
                        tile.size[0] * tile.size[1] - 5
                    ):
                        continue
                if tile.size[0] != imageWidth:
                    print('\n', imageWidth)
                    raise ValueError('图片宽度错误。')
                tile = ImageOps.invert(tile)
                tile.save(f'{outputDir}/{prefix}{count}.png')
                print(
                    f'\r{idx + 1} / {len(widthList)}',
                    f'{epoch + 1} / {total}         ',
                    end=''
                )


def checkDimensions(
    imgDir,
    imgWidth
):
    walk = os.walk(imgDir)
    for *_, paths in walk:
        break

    for i in range(len(paths)):
        img = Image.open(f'{imgDir}/{paths[i]}')
        if img.size != (imgWidth, imgWidth):
            print(f'\n{paths[i]}')
            return
        print(f'\r{i + 1} / {len(paths)}', end='')


if __name__ == '__main__':
    IMAGE_WIDTH = 32

    # 训练数据集生成
    print('开始生成训练数据集0...')
    print('-' * 50, end='')
    dataset_generation(
        inputDir='dataset/0',
        outputDir='dataset/train',
        imageWidth=IMAGE_WIDTH,
        multiple=1.4,
        prefix='0_'
    )

    print('\n\n开始生成训练数据集1...')
    print('-' * 50, end='')
    dataset_generation(
        inputDir='dataset/1',
        outputDir='dataset/train/',
        imageWidth=IMAGE_WIDTH,
        multiple=1.4,
        prefix='1_'
    )

    # 测试数据集生成
    print('\n\n开始生成测试数据集0...')
    print('-' * 50, end='')
    dataset_generation(
        inputDir='dataset/0',
        outputDir='dataset/test',
        imageWidth=IMAGE_WIDTH,
        multiple=0.6,
        prefix='0_'
    )

    print('\n\n开始生成测试数据集1...')
    print('-' * 50, end='')
    dataset_generation(
        inputDir='dataset/1',
        outputDir='dataset/test',
        imageWidth=IMAGE_WIDTH,
        multiple=0.6,
        prefix='1_'
    )
