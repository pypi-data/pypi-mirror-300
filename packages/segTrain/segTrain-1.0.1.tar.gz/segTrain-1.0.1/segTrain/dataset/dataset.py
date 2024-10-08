import os
import cv2
import random
from PIL import Image
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data.dataset import Dataset
import random
import h5py


def flip_image(image, label):
    index = random.choice([0, 1, -1])
    return cv2.flip(image, index), cv2.flip(label, index)


class Single_View(Dataset):
    def __init__(self, root_path, isSingleClass=False):
        super(Single_View, self).__init__()

        self.image_path = os.path.join(root_path, "img")
        self.label_path = os.path.join(root_path, "label")
        self.data_list = []
        self.isSingleClass = isSingleClass

        for image_name in os.listdir(self.image_path):
            self.data_list.append(image_name[:-4])

    def __len__(self):
        return len(self.data_list)

    def __getitem__(self, idx):
        name = self.data_list[idx]
        img = cv2.imread(os.path.join(self.image_path, name + '.jpg')).astype("uint8")
        ann = np.array(Image.open(os.path.join(self.label_path, name + '.png'))).astype("uint8")
        if self.isSingleClass:
            ann[ann < 100] = 0
            ann[ann >= 100] = 1
        maskTensor = torch.from_numpy(ann).type(torch.LongTensor)
        out = {
            "img": torch.from_numpy(np.transpose(img / 255, (2, 0, 1))).type(torch.FloatTensor),
            "mask": maskTensor
        }
        return out


class Single_View_HDF5_ERROR(Dataset):  # too large to load
    def __init__(self, HDF5path):
        super(Single_View_HDF5, self).__init__()
        with h5py.File(HDF5path, "r") as hf:
            self.images = hf["images"][:]
            self.labels = hf["labels"][:]
        hf.close()

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        img = self.images[idx]
        ann = self.labels[idx]
        maskTensor = torch.from_numpy(ann).type(torch.LongTensor)
        out = {
            "img": torch.from_numpy(np.transpose(img / 255, (2, 0, 1))).type(torch.FloatTensor),
            "mask": maskTensor
        }
        return out


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
