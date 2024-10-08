import os
import numpy as np
from PIL import Image
import cv2
import math
import h5py
import torch
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm

Image.MAX_IMAGE_PIXELS = None


def crop_from_one(image, label, head=(0, 0), size=512):
    x, y = head
    return image[x:x + size, y:y + size, :], label[x:x + size, y:y + size]


def createHDF5(imagePath, labelPath, output_hdf5, downsample_tuple, size=1024):
    print(f"==============[{downsample_tuple}]==============")
    assert len(downsample_tuple) == 3
    d1, d2, d3 = downsample_tuple
    print(imagePath)
    print(labelPath)
    print(output_hdf5)
    ImageNums = len(os.listdir(imagePath))
    oneImage = os.listdir(imagePath)[0]
    H0, W0, _ = cv2.imread(os.path.join(imagePath, oneImage)).shape
    s1 = d1 * size
    s2 = d2 * size
    s3 = d3 * size
    pad_size = (s3 - s1) // 2
    delt23 = (s3 - s2) // 2
    nums = math.ceil(H0 / s1) * math.ceil(W0 / s1) * ImageNums
    with h5py.File(output_hdf5, "w") as hf:
        image1_dataset = hf.create_dataset("image1", shape=(nums, size, size, 3), dtype="uint8")
        image2_dataset = hf.create_dataset("image2", shape=(nums, size, size, 3), dtype="uint8")
        image3_dataset = hf.create_dataset("image3", shape=(nums, size, size, 3), dtype="uint8")

        label_dataset = hf.create_dataset("labels", shape=(nums, size, size), dtype="uint8")
        idx = 0
        for name in tqdm(os.listdir(imagePath)):
            name = name[:-4]
            image0 = cv2.imread(os.path.join(imagePath, name + ".jpg"))
            label0 = np.array(Image.open(os.path.join(labelPath, name + ".png"))).astype(np.uint8)
            image_padded = np.pad(image0,
                                  pad_width=((pad_size, pad_size), (pad_size, pad_size), (0, 0)),
                                  mode='constant')
            # label[label > 0] = 1  # FBP is not need # TODO
            if np.max(label0) > 200:
                label0[label0 > 0] = 1

            for i in range(0, H0, s1):
                i = H0 - s1 if i + s1 > H0 else i
                for j in range(0, W0, s1):
                    j = W0 - s1 if j + s1 > W0 else j
                    img, ann = crop_from_one(image=image0, label=label0, head=(i, j), size=size)
                    image1_dataset[idx] = img
                    image2_dataset[idx] = cv2.resize(
                        image_padded[i + delt23:i + delt23 + s2, j + delt23:j + delt23 + s2, :],
                        (size, size),
                        interpolation=cv2.INTER_LINEAR)
                    image3_dataset[idx] = cv2.resize(image_padded[i:i + s3, j:j + s3, :],
                                                     (size, size),
                                                     interpolation=cv2.INTER_LINEAR)
                    label_dataset[idx] = ann
                    idx += 1
        hf.close()


def TRY():
    os.chdir("try")
    # createHDF5(imagePath=r"F:\data_lwc\FBP\test\img",
    #            labelPath=r"F:\data_lwc\FBP\test\label",
    #            output_hdf5="FBP_d_1_2_4_test.h5",
    #            downsample_tuple=(1, 2, 4),
    #            size=1024)
    hf = h5py.File("FBP_d_1_2_4_test.h5")
    ii = 199
    image1 = hf["image1"][ii]
    image2 = hf["image2"][ii]
    image3 = hf["image3"][ii]

    label = hf["labels"][ii]
    cv2.imwrite("1.jpg", image1)
    cv2.imwrite("2.jpg", image2)
    cv2.imwrite("3.jpg", image3)
    cv2.imwrite("0.png", label)


if __name__ == "__main__":
    # TRY()

    root = r"/scratch/liwanchun"
    path = {"HPD": "HPD",
            "water": "GLH_water",
            "road": "road_data",
            "building": "building_data",
            "FBP": "FBP_data"}
    #
    size = 512  # 1024
    for data_type in ("building", "A", "FBP", "water"):  # ("water", "road", "building"):
        for split in ("train", "val"):
            imagePath = os.path.join(root, path[data_type], split, "img")
            labelPath = os.path.join(root, path[data_type], split, "label")
            assert os.path.exists(imagePath) and os.path.exists(labelPath)
            for d in [(1, 3, 6)]:  # [1, 2, 3, 4, 6, 8]:
                d1, d2, d3 = d
                outPath = os.path.join(root, "Large_Size_Datasets", f"{data_type}_{split}_d_{d1}_{d2}_{d3}_{size}.h5")
                createHDF5(imagePath=imagePath,
                           labelPath=labelPath,
                           output_hdf5=outPath,
                           downsample_tuple=d,
                           size=size)
