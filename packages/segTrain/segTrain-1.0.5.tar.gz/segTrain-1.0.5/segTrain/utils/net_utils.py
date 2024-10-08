import random
import torch
import torch.backends.cudnn as cudnn
import numpy as np

cudnn.enabled = False
cudnn.benchmark = True

from .path import *


def count_trainable_params(model):
    count = 0
    for param in model.parameters():
        if param.requires_grad:
            count += param.numel()
    return count


def seed_torch(seed=3407):
    # random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)  #
    # np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    # torch.cuda.manual_seed_all(seed)  # if you are using multi-GPU.
    # torch.backends.cudnn.benchmark = False
    # torch.backends.cudnn.deterministic = True


def loadWeight(path, net):
    print(f"count_trainable_params = {count_trainable_params(model=net)}")

    if checkFile(path):
        print(f"Loading net from : {path}")
        check = torch.load(path)
        net.load_state_dict(check)
    else:
        print("There is no weight to be loaded!!")


class EarlyStopping(object):
    def __init__(self, criterion: float = 0.0, patience: int = 7):
        """
        连续 patience 轮 criterion 指标不增加
        """
        self.EarlyStopping = False
        self.patience = patience
        self.count = 0
        self.criterion = criterion

    def CheckStopping(self, new_criterion):
        flag = False
        if new_criterion < self.criterion:
            self.count += 1
            print(f"EarlyStopping counter: {self.count} out of {self.patience}")
        else:
            print(f"EarlyStopping criterion : {self.criterion} => {new_criterion}")
            self.criterion = new_criterion
            self.count = 0
            flag = True
        if self.count >= self.patience:
            self.EarlyStopping = True
        return flag
