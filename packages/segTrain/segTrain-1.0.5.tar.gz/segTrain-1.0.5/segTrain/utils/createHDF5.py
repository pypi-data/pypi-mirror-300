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


def createHDF5(imagePath, labelPath, output_hdf5, downsample, size=512):
    print(f"==============[{downsample}]==============")
    print(imagePath)
    print(labelPath)
    print(output_hdf5)
    ImageNums = len(os.listdir(imagePath))
    oneImage = os.listdir(imagePath)[0]
    H0, W0, _ = cv2.imread(os.path.join(imagePath, oneImage)).shape
    h = round(H0 / downsample)
    w = round(W0 / downsample)
    nums = math.ceil(h / size) * math.ceil(w / size) * ImageNums
    with h5py.File(output_hdf5, "w") as hf:
        image_dataset = hf.create_dataset("images", shape=(nums, size, size, 3), dtype="uint8")
        label_dataset = hf.create_dataset("labels", shape=(nums, size, size), dtype="uint8")
        idx = 0
        for name in tqdm(os.listdir(imagePath)):
            name = name[:-4]
            image0 = cv2.imread(os.path.join(imagePath, name + ".jpg"))
            label0 = np.array(Image.open(os.path.join(labelPath, name + ".png"))).astype(np.uint8)
            image = cv2.resize(image0, (w, h), interpolation=cv2.INTER_LINEAR)
            label = cv2.resize(label0, (w, h), interpolation=cv2.INTER_NEAREST)
            label[label > 0] = 1  # FBP is not need # TODO
            for i in range(0, h, size):
                i = h - size if i + size > h else i
                for j in range(0, w, size):
                    j = w - size if j + size > w else j
                    img, ann = crop_from_one(image=image, label=label, head=(i, j), size=size)
                    image_dataset[idx] = img
                    label_dataset[idx] = ann

                    idx += 1
        hf.close()


class Single_View_HDF5(Dataset):
    def __init__(self, HDF5path):
        super(Single_View_HDF5, self).__init__()
        if not os.path.exists(HDF5path):
            raise FileNotFoundError(f"HDF5 file not found: {HDF5path}")

        if not h5py.is_hdf5(HDF5path):
            raise ValueError(f"Invalid HDF5 file: {HDF5path}")

        hf = h5py.File(HDF5path)
        self.images = hf["images"]
        self.labels = hf["labels"]

    def __len__(self):
        return self.labels.shape[0]

    # def __del__(self):
    #     self.hf.close()

    def __getitem__(self, idx):
        img = self.images[idx]
        ann = self.labels[idx]
        maskTensor = torch.from_numpy(ann).type(torch.LongTensor)
        out = {
            "img": torch.from_numpy(np.transpose(img / 255, (2, 0, 1))).type(torch.FloatTensor),
            "mask": maskTensor
        }
        return out


if __name__ == "__main__":
    # createHDF5(imagePath=r"F:\data_lwc\water\test\img",
    #            labelPath=r"F:\data_lwc\water\test\label",
    #            output_hdf5="water_d5_test.h5", downsample=5, size=512)
    root = r"/scratch/liwanchun"
    path = {"HPD": "HPD",
            "water": "GLH_water",
            "road": "road_data",
            "building": "building_data",
            "FBP": "FBP_data"}
    #
    for data_type in ("building", "water"):  # ("water", "road", "building"):
        for split in ("train", "val"):
            imagePath = os.path.join(root, path[data_type], split, "img")
            labelPath = os.path.join(root, path[data_type], split, "label")
            assert os.path.exists(imagePath) and os.path.exists(labelPath)
            for d in [1]:  # [1, 2, 3, 4, 6, 8]:
                outPath = os.path.join(root, "Large_Size_Datasets", f"{data_type}_{split}_d{d}.h5")
                createHDF5(imagePath=imagePath,
                           labelPath=labelPath,
                           output_hdf5=outPath,
                           downsample=d,
                           size=512)
    # dataset = Single_View_HDF5("water_d5_test.h5")
    # print(len(dataset))
    # batch_size = 2
    # loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, pin_memory=True)
    # # 使用数据加载器进行训练
    # from torchvision.utils import save_image
    #
    # for batch in loader:
    #     img = batch["img"]
    #     print(img.device)
    #     gt = batch["mask"]
    #     save_image(img[0], 'h5img.tif')
    #     save_image(gt[0].type(torch.FloatTensor), 'h5mask.jpg')
    #     print("1")
    #     break
    # for batch in loader:
    #     gt = batch["mask"]
    #     print("2")
    #     break
