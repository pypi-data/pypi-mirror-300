import os
import cv2
import h5py
import random
import numpy as np
from tqdm import tqdm

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data.dataset import Dataset
from torch.utils.data import DataLoader
from torch.cuda.amp import autocast, GradScaler

from utils.metrics import Evaluator
from utils.net_utils import loadWeight, EarlyStopping, checkFile, seed_torch, count_trainable_params
from build import *
from Fed import FedTrain
from utils.path import checkPath, photo_metric_distortion, normalize_function
# TODO
from configs.args1024 import settings

# 设置随机种子
seed_torch()
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:4"

# 定义加载网络模型的函数
def loadNet(args: settings):
    net = build_model(args)
    pth_best = os.path.join(args.pth_path, f"{args.pth_name}_best.pth")
    assert os.path.isfile(pth_best)
    loadWeight(path=pth_best, net=net)
    net.eval()
    return net

# 自定义数据集类，用于处理HDF5格式的数据
class Views_HDF5(Dataset):
    def __init__(self, HDF5path, training=False):
        super(Views_HDF5, self).__init__()
        if not os.path.exists(HDF5path):
            raise FileNotFoundError(f"HDF5 file not found: {HDF5path}")

        if not h5py.is_hdf5(HDF5path):
            raise ValueError(f"Invalid HDF5 file: {HDF5path}")

        hf = h5py.File(HDF5path)
        self.images = hf["images"]
        self.labels = hf["labels"]
        self.training = training

    def __len__(self):
        return self.labels.shape[0]

    def __getitem__(self, idx):
        img = self.images[idx]
        ann = self.labels[idx]
        if self.training:
            img, ann = self.aug(img, ann)  # 数据增强
        maskTensor = torch.from_numpy(ann).type(torch.LongTensor)
        out = {
            "img": normalize_function(img),
            "mask": maskTensor
        }
        return out

    @staticmethod
    def aug(img, ann):
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

        def random_cover(image):
            row, col, ch = image.shape
            r = random.randint(8, row // 8)
            c = random.randint(8, col // 8)
            m = np.zeros((r, c, ch))
            sr = random.randint(0, row - r - 1)
            sc = random.randint(0, col - c - 1)
            image[sr:sr + r, sc:sc + c, :] = m
            return image

        if random.random() < 0.5:
            flip_type = random.choice([0, 1])
            img = cv2.flip(img, flip_type)
            ann = cv2.flip(ann, flip_type)
        
        return img, ann

# 训练函数
def train(data):
    size = 512

    # 设置GPU
    print(torch.cuda.device_count())
    assert torch.cuda.device_count() > 0
    device = torch.device("cuda:0")

    d1 = 1
    print(f"==============[{data}]==============")

    # 保存路径？ 参数设置
    if data == "FBP":
        pth_root = rf"./weight/FBP_normal_sswinl_upernet{size}_{d1}"
        args = settings(segHead="upernet", downsample=d1, backbone="sswin_l", isContext=False)
    elif data == "water":
        pth_root = rf"./weight/water_normal_sswinl_upernet_{size}_{d1}"
        args = settings(segHead="upernet", data_type="water", downsample=d1, backbone="sswin_l", isContext=False)
    elif data == "building":
        pth_root = rf"./weight/building_normal_sswinl_upernet_{size}_{d1}"
        args = settings(segHead="upernet", data_type="building", downsample=d1, backbone="sswin_l", isContext=False)
    else:
        raise ValueError

    # 加载训练集和验证集
    checkPath(path=pth_root)
    train_data = Views_HDF5(HDF5path=os.path.join("/scratch/liwanchun/Large_Size_Datasets",
                                                  f"{data}_train_d{d1}.h5"),
                            training=True)
    train_loader = DataLoader(train_data,
                              batch_size=8 if size == 512 else 1,
                              num_workers=2,
                              shuffle=True,
                              drop_last=True)
    val_data = Views_HDF5(HDF5path=os.path.join("/scratch/liwanchun/Large_Size_Datasets",
                                                f"{data}_val_d{d1}.h5"))
    val_loader = DataLoader(val_data,
                            batch_size=1,
                            shuffle=True,
                            drop_last=True)

    # 模型加载
    net1 = build_model(args=args)
    path = os.path.join(pth_root, "best.pth")
    if os.path.isfile(path):
        print(f"Loading net from : {path}")
        check = torch.load(path)
        net1.load_state_dict(check)
    net1.to(device)

    # 优化器
    optimizer, scheduler = build_optimizer(net=net1, args=args)
    evaluator, earlystopping = build_evaluator(args)
    earlystopping.criterion = 0

    # 创建损失函数
    criterion = build_loss(args)

    # 训练过程
    max_epochs = 80
    print(f"max epochs:{max_epochs}")
    torch.save(net1.state_dict(), os.path.join(pth_root, f"0.pth"))

    for epoch in range(1, max_epochs + 1):
        print(f"##########################[{epoch}]##########################")
        print(f"Training [{epoch}]:")
        # training
        net1.train()
        print("learn rate = {:.9f}".format(optimizer.param_groups[0]['lr']))
        print("learn rate = {:.9f}".format(optimizer.param_groups[-1]['lr']))
        bar_train = tqdm(train_loader, desc=f'Train::', position=0, leave=True, mininterval=60)

        # 获取图像和标签，进行训练
        for idx, batch in enumerate(bar_train):
            torch.cuda.empty_cache()
            img1 = batch["img"].to(device)
            mask = batch["mask"].to(device)
            torch.cuda.empty_cache()

            out = net1(img1)
            loss = criterion(out, mask)
            net1.zero_grad()
            (loss["loss_tot"]).backward()
            optimizer.step()

            #每2两个batch 更新进度条和统计信息
            if idx % 2 == 0:
                postfix_args = {k: "{:.5f}".format(v.item()) for k, v in loss.items() \
                                if k in ("loss_tot", "loss_ce", "loss_mask", "loss_dice")}
                bar_train.set_postfix(**postfix_args)
                bar_train.update()

        #保存当前的权重
        torch.save(net1.state_dict(), os.path.join(pth_root, f"{epoch}.pth"))
        print(f"{epoch}.pth was saved to {pth_root}")
        if checkFile(path=os.path.join(pth_root, f"{epoch - 1}.pth")):
            os.remove(os.path.join(pth_root, f"{epoch - 1}.pth"))

        # 验证阶段
        net1.eval()
        print(f"Validation [{epoch}]:")

        torch.cuda.empty_cache()
        bar_val = tqdm(val_loader, desc=f'Val::', position=0, leave=True, mininterval=60)
        evaluator.reset()
        with torch.no_grad():
            for idx, batch in enumerate(bar_val):
                img1 = batch["img"].to(device)
                outputs = net1(img1)
                gt = batch["mask"].to(device)
                # pred = outputs[:, 1:, :, :]  # TODO FBP
                pred = outputs
                pre = np.argmax(pred.cpu().numpy(), axis=1)[0]
                gt = gt.squeeze(0).cpu().numpy()

                evaluator.add_batch(gt, pre)
                if idx % 2 == 0:
                    postfix_args1 = {"id": f"{idx}"}
                    bar_val.set_postfix(**postfix_args1)
                    bar_val.update()

        MIoU = evaluator.Mean_Intersection_over_Union()
        print(f"MIoU = {MIoU}")
        if earlystopping.CheckStopping(new_criterion=MIoU):
            torch.save(net1.state_dict(), os.path.join(pth_root, "best.pth"))
            print("BETTER MODEL SAVED")
        scheduler.step(earlystopping.criterion)

        print(f"best_MIoU = {earlystopping.criterion}")

        if earlystopping.EarlyStopping:
            print("EarlyStooping")
            return

def select_data(data_type, batch_size):

    train_data_path = "/data"
    val_data_path = "/data"
    size = 512
    d1 = 1
    # 根据数据类型加载训练集和验证集
    if data_type == "FBP":
        train_dataset_path = os.path.join(train_data_path, f"FBP_train_d{d1}.h5")
        val_dataset_path = os.path.join(val_data_path, f"FBP_val_d{d1}.h5")
        pth_root = rf"/data/weight/FBP_normal_sswinl_upernet{size}_{d1}"
        args = settings(downsample=d1, isContext=False)
    elif data_type == "water":
        train_dataset_path = os.path.join(train_data_path, f"water_train_d{d1}.h5")
        val_dataset_path = os.path.join(val_data_path, f"water_val_d{d1}.h5")
        pth_root = rf"/data/weight/water_normal_sswinl_upernet_{size}_{d1}"
        args = settings(data_type="water", downsample=d1, isContext=False)
    elif data_type == "building":
        train_dataset_path = os.path.join(train_data_path, f"building_train_d{d1}.h5")
        val_dataset_path = os.path.join(val_data_path, f"building_val_d{d1}.h5")
        pth_root = rf"/data/weight/building_normal_sswinl_upernet_{size}_{d1}"
        args = settings(data_type="building", downsample=d1, isContext=False)
    else:
        raise ValueError("Invalid data type specified")

    train_data = Views_HDF5(HDF5path=train_dataset_path, training=True)
    val_data = Views_HDF5(HDF5path=val_dataset_path)

    #train_loader = DataLoader(train_data, batch_size=8 if size == 512 else 1, num_workers=2, shuffle=True, drop_last=True)
    train_loader = DataLoader(train_data, batch_size=batch_size, num_workers=2, shuffle=True, drop_last=True)
    val_loader = DataLoader(val_data, batch_size=1, shuffle=True, drop_last=True)


    return train_loader, val_loader, args, pth_root

def design_model(decoder, encoder, args, pth_root):

    print(torch.cuda.device_count())
    assert torch.cuda.device_count() > 0
    device = torch.device("cuda:0")
    # 根据给定参数创建模型
    #args = settings(segHead=decoder, backbone=encoder)
    args.segHead = decoder
    args.backbone = encoder
    model = build_model(args=args)
    path = os.path.join(pth_root, "best.pth")
    if os.path.isfile(path):
        print(f"Loading net from : {path}")
        check = torch.load(path)
        model.load_state_dict(check)
    model.to(device)
    return model,args,device

def design_optimizer(model, args):
    optimizer, scheduler = build_optimizer(net=model, args=args)
    evaluator, earlystopping = build_evaluator(args)
    earlystopping.criterion = 0
    return optimizer,scheduler,evaluator,earlystopping

def design_loss(args):
    criterion = build_loss(args)
    return criterion

def train_model(epoch, model, pth_root, train_loader, val_loader, device,optimizer, scheduler, evaluator, earlystopping, criterion):
    # 训练过程
    max_epochs = epoch
    net1 = model

    print(f"max epochs:{max_epochs}")
    torch.save(net1.state_dict(), os.path.join(pth_root, f"0.pth"))

    for epoch in range(1, max_epochs + 1):
        print(f"##########################[{epoch}]##########################")
        print(f"Training [{epoch}]:")
        # training
        net1.train()
        print("learn rate = {:.9f}".format(optimizer.param_groups[0]['lr']))
        print("learn rate = {:.9f}".format(optimizer.param_groups[-1]['lr']))
        bar_train = tqdm(train_loader, desc=f'Train::', position=0, leave=True, mininterval=60)

        # 获取图像和标签，进行训练
        for idx, batch in enumerate(bar_train):
            torch.cuda.empty_cache()
            img1 = batch["img"].to(device)
            mask = batch["mask"].to(device)
            torch.cuda.empty_cache()

            out = net1(img1)
            loss = criterion(out, mask)
            net1.zero_grad()
            (loss["loss_tot"]).backward()
            optimizer.step()

            # 每2两个batch 更新进度条和统计信息
            if idx % 2 == 0:
                postfix_args = {k: "{:.5f}".format(v.item()) for k, v in loss.items() \
                                if k in ("loss_tot", "loss_ce", "loss_mask", "loss_dice")}
                bar_train.set_postfix(**postfix_args)
                bar_train.update()

        # 保存当前的权重
        torch.save(net1.state_dict(), os.path.join(pth_root, f"{epoch}.pth"))
        print(f"{epoch}.pth was saved to {pth_root}")
        if checkFile(path=os.path.join(pth_root, f"{epoch - 1}.pth")):
            os.remove(os.path.join(pth_root, f"{epoch - 1}.pth"))

        # 验证阶段
        net1.eval()
        print(f"Validation [{epoch}]:")

        torch.cuda.empty_cache()
        bar_val = tqdm(val_loader, desc=f'Val::', position=0, leave=True, mininterval=60)
        evaluator.reset()
        with torch.no_grad():
            for idx, batch in enumerate(bar_val):
                img1 = batch["img"].to(device)
                outputs = net1(img1)
                gt = batch["mask"].to(device)
                # pred = outputs[:, 1:, :, :]  # TODO FBP
                pred = outputs
                pre = np.argmax(pred.cpu().numpy(), axis=1)[0]
                gt = gt.squeeze(0).cpu().numpy()

                evaluator.add_batch(gt, pre)
                if idx % 2 == 0:
                    postfix_args1 = {"id": f"{idx}"}
                    bar_val.set_postfix(**postfix_args1)
                    bar_val.update()

        MIoU = evaluator.Mean_Intersection_over_Union()
        print(f"MIoU = {MIoU}")
        if earlystopping.CheckStopping(new_criterion=MIoU):
            torch.save(net1.state_dict(), os.path.join(pth_root, "best.pth"))
            print("BETTER MODEL SAVED")
        scheduler.step(earlystopping.criterion)

        print(f"best_MIoU = {earlystopping.criterion}")

        if earlystopping.EarlyStopping:
            print("EarlyStooping")
            return

# if __name__ == "__main__":
#     # import argparse
#     #
#     # parser = argparse.ArgumentParser('Set PFNetPlus Train', add_help=False)
#     # parser.add_argument('--data', type=str, default="water")
#     #
#     # args = parser.parse_args()
#     # print(f"==============[{args.data}]==============")
#     # train(data=args.data)
#
#     #数据选择
#     train_loader, val_loader, args, pth_root = select_data("FBP", 8)
#
#     #模型设计
#     model, args, device = design_model("upernet", "sswin-l", args, pth_root)
#
#     #优化器设计
#     optimizer, scheduler, evaluator, earlystopping = design_optimizer(model, args)
#
#     #损失函数设计
#     criterion = design_loss(args)
#
#     #模型训练
#     train_model(80, model, pth_root, train_loader,val_loader, device, optimizer, scheduler, evaluator, earlystopping, criterion)
