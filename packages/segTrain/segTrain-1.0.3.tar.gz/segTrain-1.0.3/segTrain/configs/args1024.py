import torch


class settings(object):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # loss only for mask2former
    class_weight = 2.0
    mask_weight = 5.0
    dice_weight = 5.0
    train_num_points = 12544
    deep_supervision = True
    no_object_weight = 0.1
    dec_layers = 10
    oversample_ratio = 3.0
    importance_sample_ratio = 0.75

    data_root = r"/scratch/liwanchun/Large_Size_Datasets"
    # data_root = r"weight"
    batch_size = 2
    num_workers = 2
    learn_rate = 0.0001

    def __init__(self,
                 data_type="FBP",
                 downsample=8,
                 backbone="swin_b",
                 segHead="mask2former",
                 isContext=True):
        self.isContext = isContext
        # data
        self.data_type = data_type
        self.downsample = downsample

        # model
        self.backbone = backbone
        self.segHead = segHead
        if data_type == "FBP":
            self.nclass = 25
        elif data_type == "HPD":
            self.nclass = 10
        else:
            self.nclass = 2
        self.ignore_index = -100 if self.nclass == 2 else 0

        self.resume = False
        self.pth_resume = "weight/mask2former/FBP_d1_best.pth"
        self.pth_name = f"{data_type}_d{downsample}_1024"
        # self.pth_name = f"{data_type}_d{downsample}"
        self.pth_path = f"weight/{segHead}"

        # train
        self.max_epochs = 50 * downsample

        if data_type == "FBP":
            self.early_stopping_patience = min(5 * downsample + 3, 13)
            self.lr_patience = min(3 * downsample + 1, 7)
        else:
            self.early_stopping_patience = 5
            self.lr_patience = 3
        print("########################################")
        print(f"max_epochs = {self.max_epochs}")
        print(f"early_stopping_patience = {self.early_stopping_patience}")
        print(f"lr_patience = {self.lr_patience}")
        print(f"isContext = {isContext}")
        print(f"feature encoder = {self.backbone}")
        print(f"segment decoder = {self.segHead}")
        print("########################################")
