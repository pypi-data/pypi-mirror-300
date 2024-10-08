import os
import random
from typing import Sequence
import numpy as np
import mmcv
import torch
from torchvision import transforms
import cv2


def normalize_function(img):  # 更快
    # Mean values used to pre-training the pre-trained backbone models
    mean = [123.675, 116.28, 103.53]
    std = [58.395, 57.12, 57.375]
    mean = np.array(mean, dtype=np.float32)
    std = np.array(std, dtype=np.float32)
    results = mmcv.imnormalize(img, mean, std, to_rgb=True)
    return torch.from_numpy(results.transpose((2, 0, 1))).float()


def photo_metric_distortion(img: np.ndarray,
                            brightness_delta: int = 32,
                            contrast_range: Sequence[float] = (0.5, 1.5),
                            saturation_range: Sequence[float] = (0.5, 1.5),
                            hue_delta: int = 18) -> np.ndarray:
    def convert(img: np.ndarray, alpha: int = 1, beta: int = 0) -> np.ndarray:
        img = img.astype(np.float32) * alpha + beta
        img = np.clip(img, 0, 255)
        return img.astype(np.uint8)

    def brightness(img: np.ndarray) -> np.ndarray:
        if random.randint(0, 1):
            return convert(img, beta=random.uniform(-brightness_delta, brightness_delta))
        return img

    def contrast(img: np.ndarray) -> np.ndarray:
        if random.randint(0, 1):
            return convert(img, alpha=random.uniform(contrast_range[0], contrast_range[1]))
        return img

    def saturation(img: np.ndarray) -> np.ndarray:
        if random.randint(0, 1):
            img_hsv = mmcv.bgr2hsv(img)
            img_hsv[:, :, 1] = convert(img_hsv[:, :, 1], alpha=random.uniform(saturation_range[0], saturation_range[1]))
            img = mmcv.hsv2bgr(img_hsv)
        return img

    def hue(img: np.ndarray) -> np.ndarray:
        if random.randint(0, 1):
            img_hsv = mmcv.bgr2hsv(img)
            img_hsv[:, :, 0] = (img_hsv[:, :, 0].astype(int) + random.randint(-hue_delta, hue_delta)) % 180
            img = mmcv.hsv2bgr(img_hsv)
        return img

    # random brightness
    img = brightness(img)

    # mode == 0 --> do random contrast first
    # mode == 1 --> do random contrast last
    mode = random.randint(0, 1)
    if mode == 1:
        img = contrast(img)

    # random saturation
    img = saturation(img)

    # random hue
    img = hue(img)

    # random contrast
    if mode == 0:
        img = contrast(img)

    return img


def GridMask(image, grid_size=16, cell_size=32,
             mask_ratio=0.25):
    grid_size = image.shape[0] // cell_size
    mask = np.zeros((grid_size, grid_size))
    mask[1::2, 1::2] = 1
    for i in range(grid_size):
        for j in range(grid_size):
            if mask[i, j] == 1:
                image[i * cell_size: (i + 1) * cell_size, j * cell_size: (j + 1) * cell_size, :] = \
                    [123.675, 116.28, 103.53]
    return image


def BlockMask(image, grid_size=16, cell_size=32,
              mask_ratio=0.25):
    grid_size = image.shape[0] // cell_size
    mask = np.zeros((grid_size, grid_size))
    r = random.randint(0, grid_size // 2)
    c = random.randint(0, grid_size // 2)
    mask[r:r + grid_size // 2, c:c + grid_size // 2] = 1
    for i in range(grid_size):
        for j in range(grid_size):
            if mask[i, j] == 1:
                image[i * cell_size: (i + 1) * cell_size, j * cell_size: (j + 1) * cell_size, :] = \
                    [123.675, 116.28, 103.53]
    return image


def RandomMask(image, grid_size=16, cell_size=32,
               mask_ratio=0.25):
    # grid_size = image.shape[0] // cell_size
    mask = np.random.choice([0, 1], size=(grid_size, grid_size), p=[1 - mask_ratio, mask_ratio])
    for i in range(grid_size):
        for j in range(grid_size):
            if mask[i, j] == 1:
                image[i * cell_size: (i + 1) * cell_size, j * cell_size: (j + 1) * cell_size, :] = \
                    [123.675, 116.28, 103.53]
    return image


def checkPath(path):
    if not os.path.exists(path):
        os.makedirs(path)


def checkFile(path):
    return os.path.isfile(path)


# un use

class Normalize(object):
    # rgb
    # imagenet_mean = [0.485, 0.456, 0.406]
    # imagenet_std = [0.229, 0.224, 0.225]
    def __init__(self, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)):
        self.mean = mean
        self.std = std

    def __call__(self, img):
        # img:opencv:bgr
        # cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        img = np.array(img[:, :, ::-1]).astype(np.float32)
        img /= 255.0
        img -= self.mean
        img /= self.std

        return img


class ToTensor(object):
    def __call__(self, img):
        # swap color axis because
        # numpy image: H x W x C
        # torch image: C X H X W
        img = np.array(img).astype(np.float32).transpose((2, 0, 1))
        img = torch.from_numpy(img).float()

        return img


# 将 Normalize 和 ToTensor 组合成一个函数
def transform_function(img):
    composed_transforms = transforms.Compose([
        Normalize(),
        ToTensor(),
    ])

    return composed_transforms(img)


def color_distortion(image):
    # 随机改变图像的亮度、对比度和饱和度
    alpha = 1.0 + np.random.uniform(-0.5, 0.5)  # 亮度
    beta = 0.5 + np.random.uniform(-0.5, 0.5)  # 对比度
    saturation_scale = 0.5 + np.random.uniform(0, 1)  # 饱和度

    image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 调整饱和度
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation_scale, 0, 255)

    distorted_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return distorted_image


def gaussian_noise(image):
    row, col, ch = image.shape
    mean = 0
    var = 0.1
    sigma = var ** 0.5
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    noisy = np.clip(image + gauss * 255, 0, 255).astype(np.uint8)
    return noisy
