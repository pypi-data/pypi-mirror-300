import os
import torch
import torch.optim as optim
import torch.nn as nn
from typing import Any, Dict, List, Set
import copy
import itertools
from .model.semseg.deeplabv3plus import DeepLabV3Plus
from .model.semseg.mask2former import Mask2Former
from .model.semseg.upernet import UPerNet
from .model.semseg.unetformer import UNetFormer

# from dataset import build_dataloader
from .configs.args import settings
from .utils.net_utils import loadWeight, seed_torch, EarlyStopping
from .utils.metrics import Evaluator
from .losses.criterion import SetCriterion
from .losses.matcher import HungarianMatcher
from .losses.celoss import SegmentationLosses

# 构建模型函数
def build_model(args: settings):
    seed_torch()
    print(f"feature encoder : {args.backbone}")
    print(f"segment decoder : {args.segHead}")
    if args.segHead == "deeplabv3":
        model = DeepLabV3Plus(backbone=args.backbone, nclass=args.nclass, isContext=args.isContext)
    elif args.segHead == "mask2former":
        model = Mask2Former(backbone=args.backbone, nclass=args.nclass, isContext=args.isContext)
    elif args.segHead == "upernet":
        model = UPerNet(backbone=args.backbone, nclass=args.nclass, isContext=args.isContext)
    elif args.segHead == "unetformer":
        model = UNetFormer(backbone=args.backbone, nclass=args.nclass, isContext=args.isContext)
    else:
        raise ValueError(f"Invalid seg head: {args.segHead}")
    if args.resume:
        loadWeight(path=args.pth_resume, net=model)
    # model.to(args.device)
    return model

# 构建数据加载器函数
def build_data(args: settings):
    print(f"data type : {args.data_type}")
    print(f"downsample : {args.downsample}")
    trainDataLoader = build_dataloader(
        data_path=os.path.join(args.data_root, f"{args.data_type}_train_d{args.downsample}_1024.h5"),
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        isSingleClass=args.data_type == "FBP")
    valDataLoader = build_dataloader(
        data_path=os.path.join(args.data_root, f"{args.data_type}_val_d{args.downsample}_1024.h5"),
        batch_size=1,  # val batch size = 1
        isSingleClass=args.data_type == "FBP")

    return trainDataLoader, valDataLoader

# 构建Mask2Former优化器
def build_optimizer_mask2former(model, lr):
    weight_decay_norm = 0.0  # cfg.SOLVER.WEIGHT_DECAY_NORM
    weight_decay_embed = 0.0  # cfg.SOLVER.WEIGHT_DECAY_EMBED

    defaults = {}
    BASE_LR = lr
    defaults["lr"] = BASE_LR  # cfg.SOLVER.BASE_LR
    defaults["weight_decay"] = 0.05  # cfg.SOLVER.WEIGHT_DECAY

    norm_module_types = (
        torch.nn.BatchNorm1d,
        torch.nn.BatchNorm2d,
        torch.nn.BatchNorm3d,
        torch.nn.SyncBatchNorm,
        # NaiveSyncBatchNorm inherits from BatchNorm2d
        torch.nn.GroupNorm,
        torch.nn.InstanceNorm1d,
        torch.nn.InstanceNorm2d,
        torch.nn.InstanceNorm3d,
        torch.nn.LayerNorm,
        torch.nn.LocalResponseNorm,
    )

    params: List[Dict[str, Any]] = []
    memo: Set[torch.nn.parameter.Parameter] = set()
    for module_name, module in model.named_modules():
        for module_param_name, value in module.named_parameters(recurse=False):
            if not value.requires_grad:
                continue
            # Avoid duplicating parameters
            if value in memo:
                continue
            memo.add(value)

            hyperparams = copy.copy(defaults)
            if "backbone" in module_name:
                hyperparams["lr"] = hyperparams["lr"] * 0.1  # cfg.SOLVER.BACKBONE_MULTIPLIER
            if (
                    "relative_position_bias_table" in module_param_name
                    or "absolute_pos_embed" in module_param_name
            ):
                print(module_param_name)
                hyperparams["weight_decay"] = 0.0
            if isinstance(module, norm_module_types):
                hyperparams["weight_decay"] = weight_decay_norm
            if isinstance(module, torch.nn.Embedding):
                hyperparams["weight_decay"] = weight_decay_embed
            params.append({"params": [value], **hyperparams})

    def maybe_add_full_model_gradient_clipping(optim):
        # detectron2 doesn't have full model gradient clipping now
        clip_norm_val = 0.1  # cfg.SOLVER.CLIP_GRADIENTS.CLIP_VALUE
        enable = (
            # cfg.SOLVER.CLIP_GRADIENTS.ENABLED
            # and cfg.SOLVER.CLIP_GRADIENTS.CLIP_TYPE == "full_model"
                True
                and clip_norm_val > 0.0
        )

        class FullModelGradientClippingOptimizer(optim):
            def step(self, closure=None):
                all_params = itertools.chain(*[x["params"] for x in self.param_groups])
                torch.nn.utils.clip_grad_norm_(all_params, clip_norm_val)
                super().step(closure=closure)

        return FullModelGradientClippingOptimizer if enable else optim

    optimizer_type = "ADAMW"  # cfg.SOLVER.OPTIMIZER
    if optimizer_type == "SGD":
        optimizer = maybe_add_full_model_gradient_clipping(torch.optim.SGD)(
            params, BASE_LR, momentum=cfg.SOLVER.MOMENTUM
        )
    elif optimizer_type == "ADAMW":
        optimizer = maybe_add_full_model_gradient_clipping(torch.optim.AdamW)(
            params, BASE_LR
        )
    else:
        raise NotImplementedError(f"no optimizer type {optimizer_type}")
    # if not cfg.SOLVER.CLIP_GRADIENTS.CLIP_TYPE == "full_model":
    #     optimizer = maybe_add_gradient_clipping(cfg, optimizer)
    return optimizer

# 构建优化器和学习率调度器
def build_optimizer(net, args: settings):
    # optimizer
    # if args.segHead == "mask2former":
    #     optimizer = build_optimizer_mask2former(net, lr=args.learn_rate)
    # else:
    #     # optimizer = optim.SGD(net.parameters(), lr=args.learn_rate, momentum=0.9, weight_decay=0.0005)
    #     optimizer = optim.AdamW(net.parameters(), lr=args.learn_rate, betas=(0.9, 0.999),
    #                             eps=1e-08, weight_decay=0.05, amsgrad=False)
    optimizer = build_optimizer_mask2former(net, lr=args.learn_rate)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'max', patience=args.lr_patience, verbose=True)
    return optimizer, scheduler

# 构建评估器和早停机制
def build_evaluator(args: settings, now_criterion: float = 0):
    evaluator = Evaluator(args.nclass, args.ignore_index)
    earlystopping = EarlyStopping(criterion=now_criterion, patience=args.early_stopping_patience)
    return evaluator, earlystopping

# 构建损失函数
def build_loss(args: settings):
    if args.segHead != "mask2former":
        if args.nclass > 2:
            weight = torch.ones(args.nclass).to(args.device)
            weight[0] = 0
        else:
            weight = None
        criterion = SegmentationLosses(weight=weight, ignore_index=args.ignore_index,
                                       device=args.device).build_loss(mode="ce")
        return criterion
    # 损失参数
    deep_supervision = args.deep_supervision
    no_object_weight = args.no_object_weight

    # 损失权重
    class_weight = args.class_weight
    dice_weight = args.dice_weight
    mask_weight = args.mask_weight

    # 构建标准
    matcher = HungarianMatcher(
        cost_class=class_weight,
        cost_mask=mask_weight,
        cost_dice=dice_weight,
        num_points=args.train_num_points,
    )

    weight_dict = {"loss_ce": class_weight, "loss_mask": mask_weight, "loss_dice": dice_weight}
    if deep_supervision:
        dec_layers = args.dec_layers
        aux_weight_dict = {}
        for i in range(dec_layers - 1):
            aux_weight_dict.update({k + f"_{i}": v for k, v in weight_dict.items()})
        weight_dict.update(aux_weight_dict)

    losses = ["labels", "masks"]
    criterion = SetCriterion(
        args.nclass,
        matcher=matcher,
        weight_dict=weight_dict,
        eos_coef=no_object_weight,
        losses=losses,
        num_points=args.train_num_points,
        oversample_ratio=args.oversample_ratio,
        importance_sample_ratio=args.importance_sample_ratio,
        device=args.device
    )
    return criterion
