# Copyright (c) Facebook, Inc. and its affiliates.
# Modified by Bowen Cheng from https://github.com/facebookresearch/detr/blob/master/models/detr.py
"""
MaskFormer criterion.
"""
from typing import List, Optional
import torch
from torch import Tensor
import numpy as np
import torch.nn.functional as F
import torch.distributed as dist
from torch import nn
import sys
import os
import torchvision

sys.path.append(os.path.dirname(__file__) + os.sep + '../')

# 计算二维列表每个列的最大值
def _max_by_axis(the_list):
    # type: (List[List[int]]) -> List[int]
    maxes = the_list[0]
    for sublist in the_list[1:]:
        for index, item in enumerate(sublist):
            maxes[index] = max(maxes[index], item)
    return maxes

# 获取分布式训练的进程数量
def get_world_size() -> int:
    if not dist.is_available():
        return 1
    if not dist.is_initialized():
        return 1
    return dist.get_world_size()


def reduce_dict(input_dict, average=True):
    """
    归约分布式训练中的字典，将所有进程的字典数据汇总
    """
    world_size = get_world_size()
    if world_size < 2:
        return input_dict
    with torch.no_grad():
        names = []
        values = []
        # 按键排序，确保跨进程一致
        for k in sorted(input_dict.keys()):
            names.append(k)
            values.append(input_dict[k])
        values = torch.stack(values, dim=0)
        dist.all_reduce(values)
        if average:
            values /= world_size
        reduced_dict = {k: v for k, v in zip(names, values)}
    return reduced_dict


class NestedTensor(object):
    def __init__(self, tensors, mask: Optional[Tensor]):
        self.tensors = tensors
        self.mask = mask

    def to(self, device):
        # type: (Device) -> NestedTensor # noqa
        cast_tensor = self.tensors.to(device)
        mask = self.mask
        if mask is not None:
            assert mask is not None
            cast_mask = mask.to(device)
        else:
            cast_mask = None
        return NestedTensor(cast_tensor, cast_mask)

    def decompose(self):
        return self.tensors, self.mask

    def __repr__(self):
        return str(self.tensors)

# 将tensor列表转换为NestedTensor
def nested_tensor_from_tensor_list(tensor_list: List[Tensor]):
    # TODO make this more general
    if tensor_list[0].ndim == 3:
        if torchvision._is_tracing():
            # nested_tensor_from_tensor_list() does not export well to ONNX
            # call _onnx_nested_tensor_from_tensor_list() instead
            return _onnx_nested_tensor_from_tensor_list(tensor_list)

        # TODO make it support different-sized images
        max_size = _max_by_axis([list(img.shape) for img in tensor_list])
        # min_size = tuple(min(s) for s in zip(*[img.shape for img in tensor_list]))
        batch_shape = [len(tensor_list)] + max_size
        b, c, h, w = batch_shape
        dtype = tensor_list[0].dtype
        device = tensor_list[0].device
        tensor = torch.zeros(batch_shape, dtype=dtype, device=device)
        mask = torch.ones((b, h, w), dtype=torch.bool, device=device)
        for img, pad_img, m in zip(tensor_list, tensor, mask):
            pad_img[: img.shape[0], : img.shape[1], : img.shape[2]].copy_(img)
            m[: img.shape[1], : img.shape[2]] = False
    else:
        raise ValueError("not supported")
    return NestedTensor(tensor, mask)


# 处理ONNX tracing中不支持的操作
@torch.jit.unused
def _onnx_nested_tensor_from_tensor_list(tensor_list: List[Tensor]) -> NestedTensor:
    max_size = []
    for i in range(tensor_list[0].dim()):
        max_size_i = torch.max(
            torch.stack([img.shape[i] for img in tensor_list]).to(torch.float32)
        ).to(torch.int64)
        max_size.append(max_size_i)
    max_size = tuple(max_size)

    # work around for
    # pad_img[: img.shape[0], : img.shape[1], : img.shape[2]].copy_(img)
    # m[: img.shape[1], :img.shape[2]] = False
    # which is not yet supported in onnx
    padded_imgs = []
    padded_masks = []
    for img in tensor_list:
        padding = [(s1 - s2) for s1, s2 in zip(max_size, tuple(img.shape))]
        padded_img = torch.nn.functional.pad(img, (0, padding[2], 0, padding[1], 0, padding[0]))
        padded_imgs.append(padded_img)

        m = torch.zeros_like(img[0], dtype=torch.int, device=img.device)
        padded_mask = torch.nn.functional.pad(m, (0, padding[2], 0, padding[1]), "constant", 1)
        padded_masks.append(padded_mask.to(torch.bool))

    tensor = torch.stack(padded_imgs)
    mask = torch.stack(padded_masks)

    return NestedTensor(tensor, mask=mask)


def is_dist_avail_and_initialized():
    if not dist.is_available():
        return False
    if not dist.is_initialized():
        return False
    return True


def dice_loss(
        inputs: torch.Tensor,
        targets: torch.Tensor,
        num_masks: float,
):
    """
    计算DICE损失，类似于用于掩码的广义IOU
    Args:
        inputs: A float tensor of arbitrary shape.
                The predictions for each example.
        targets: A float tensor with the same shape as inputs. Stores the binary
                 classification label for each element in inputs
                (0 for the negative class and 1 for the positive class).
    """
    inputs = inputs.sigmoid()
    inputs = inputs.flatten(1)
    numerator = 2 * (inputs * targets).sum(-1)
    denominator = inputs.sum(-1) + targets.sum(-1)
    loss = 1 - (numerator + 1) / (denominator + 1)
    return loss.sum() / num_masks


def sigmoid_ce_loss(
        inputs: torch.Tensor,
        targets: torch.Tensor,
        num_masks: float,
):
    """
    计算二值交叉熵损失
    Args:
        inputs: A float tensor of arbitrary shape.
                The predictions for each example.
        targets: A float tensor with the same shape as inputs. Stores the binary
                 classification label for each element in inputs
                (0 for the negative class and 1 for the positive class).
    Returns:
        Loss tensor
    """
    loss = F.binary_cross_entropy_with_logits(inputs, targets, reduction="none")
    return loss.mean(1).sum() / num_masks


def sigmoid_focal_loss(inputs, targets, num_masks, alpha: float = 0.25, gamma: float = 2):
    """
    RetinaNet中用于密集检测的损失函数: https://arxiv.org/abs/1708.02002.
    Args:
        inputs: A float tensor of arbitrary shape.
                The predictions for each example.
        targets: A float tensor with the same shape as inputs. Stores the binary
                 classification label for each element in inputs
                (0 for the negative class and 1 for the positive class).
        alpha: (optional) Weighting factor in range (0,1) to balance
                positive vs negative examples. Default = -1 (no weighting).
        gamma: Exponent of the modulating factor (1 - p_t) to
               balance easy vs hard examples.
    Returns:
        Loss tensor
    """
    prob = inputs.sigmoid()
    ce_loss = F.binary_cross_entropy_with_logits(inputs, targets, reduction="none")
    p_t = prob * targets + (1 - prob) * (1 - targets)
    loss = ce_loss * ((1 - p_t) ** gamma)

    if alpha >= 0:
        alpha_t = alpha * targets + (1 - alpha) * (1 - targets)
        loss = alpha_t * loss

    return loss.mean(1).sum() / num_masks


def calculate_uncertainty(logits):
    """
    我们通过计算 'logits' 中前景类的预测与 0.0 的 L1 距离来估计不确定性。
    参数:
        logits (Tensor): 形状为 (R, 1, ...) 的张量，代表特定类别或类别无关的预测结果，其中 R 是所有图片中预测的掩码总数，C 是前景类别的数量。值为 logits。
    返回:
        scores (Tensor): 形状为 (R, 1, ...) 的张量，包含不确定性分数，最不确定的位置具有最高的不确定性分数。
    """
    assert logits.shape[1] == 1
    gt_class_logits = logits.clone()
    return -(torch.abs(gt_class_logits))


class SetCriterion(nn.Module):
    """
    这个类用于计算 DETR 的损失。
    过程分为两个步骤：
        1) 计算真实框与模型输出之间的匈牙利匹配。
        2) 对每对匹配的真实值/预测值进行监督（监督类别和框）。
    """

    def __init__(self, num_classes, matcher, weight_dict, eos_coef, losses,
                 num_points, oversample_ratio, importance_sample_ratio, device):
        """
        创建损失计算标准。
        参数:
            num_classes: 对象类别数量，不包括特殊的无对象类别。
            matcher: 能够计算目标和提议之间匹配的模块。
            weight_dict: 包含损失名称为键，及其相对权重为值的字典。
            eos_coef: 应用于无对象类别的相对分类权重。
            losses: 所有将应用的损失的列表。请参阅 get_loss 以获取可用损失的列表。
        """
        super().__init__()
        self.num_classes = num_classes
        self.matcher = matcher
        self.weight_dict = weight_dict
        self.eos_coef = eos_coef
        self.losses = losses
        self.device = device
        empty_weight = torch.ones(self.num_classes + 1).to(device)
        empty_weight[0] = 0  # TODO for FBP
        empty_weight[-1] = self.eos_coef
        self.empty_weight = empty_weight

        # pointwise mask loss parameters
        self.num_points = num_points
        self.oversample_ratio = oversample_ratio
        self.importance_sample_ratio = importance_sample_ratio

    def loss_labels(self, outputs, targets, indices, num_masks):
        """
        分类损失 (NLL)
        目标字典必须包含键 "labels"，其包含维度为 [nb_target_boxes] 的张量。
        """
        assert "pred_logits" in outputs
        src_logits = outputs["pred_logits"].float()

        idx = self._get_src_permutation_idx(indices)
        target_classes_o = torch.cat([t["labels"][J] for t, (_, J) in zip(targets, indices)]).to(self.device)
        target_classes = torch.full(src_logits.shape[:2], 0, dtype=torch.int64, device=src_logits.device)
        target_classes[idx] = target_classes_o

        loss_ce = F.cross_entropy(src_logits.transpose(1, 2), target_classes, self.empty_weight)
        losses = {"loss_ce": loss_ce}
        return losses

    def loss_masks(self, outputs, targets, indices, num_masks):
        """
        计算与掩码相关的损失：焦点损失和 dice 损失。
        目标字典必须包含键 "masks"，其包含维度为 [nb_target_boxes, h, w] 的张量。
        """
        assert "pred_masks" in outputs

        src_idx = self._get_src_permutation_idx(indices)
        tgt_idx = self._get_tgt_permutation_idx(indices)
        src_masks = outputs["pred_masks"]  #
        src_masks = src_masks[src_idx]
        masks = [t["masks"] for t in targets]
        # TODO use valid to mask invalid areas due to padding in loss
        target_masks, valid = nested_tensor_from_tensor_list(masks).decompose()
        # print([x.shape for x in masks])
        # target_masks = torch.cat(masks, dim=0)
        target_masks = target_masks.to(src_masks)
        target_masks = target_masks[tgt_idx]

        # ===================================================================================
        # seg task no need to sample #
        # No need to upsample predictions as we are using normalized coordinates :)
        # N x 1 x H x W

        # src_masks = src_masks[:, None]
        # target_masks = target_masks[:, None]

        # with torch.no_grad():
        #     # sample point_coords
        #     point_coords = get_uncertain_point_coords_with_randomness(
        #         src_masks,
        #         lambda logits: calculate_uncertainty(logits),
        #         self.num_points,
        #         self.oversample_ratio,
        #         self.importance_sample_ratio,
        #     )
        #     # get gt labels
        #     point_labels = point_sample(
        #         target_masks,
        #         point_coords,
        #         align_corners=False,
        #     ).squeeze(1)

        # point_logits = point_sample(
        #     src_masks,
        #     point_coords,
        #     align_corners=False,
        # ).squeeze(1)
        # ===================================================================================
        point_logits = src_masks.flatten(1)
        point_labels = target_masks.flatten(1)

        losses = {
            "loss_mask": sigmoid_ce_loss(point_logits, point_labels, num_masks),
            # sigmoid_focal_loss(point_logits, point_labels, num_masks), #
            "loss_dice": dice_loss(point_logits, point_labels, num_masks)
        }

        del src_masks
        del target_masks
        return losses

    def _get_src_permutation_idx(self, indices):
        # 根据索引排列预测值
        batch_idx = torch.cat([torch.full_like(src, i) for i, (src, _) in enumerate(indices)])
        src_idx = torch.cat([src for (src, _) in indices])
        return batch_idx, src_idx

    def _get_tgt_permutation_idx(self, indices):
        # 根据索引排列目标值
        batch_idx = torch.cat([torch.full_like(tgt, i) for i, (_, tgt) in enumerate(indices)])
        tgt_idx = torch.cat([tgt for (_, tgt) in indices])
        return batch_idx, tgt_idx

    def get_loss(self, loss, outputs, targets, indices, num_masks):
        loss_map = {
            'labels': self.loss_labels,
            'masks': self.loss_masks,
        }
        assert loss in loss_map, f"do you really want to compute {loss} loss?"
        return loss_map[loss](outputs, targets, indices, num_masks)

    @staticmethod
    def postOutput(outputs):
        for k, v in outputs.items():
            if k == "aux_outputs":
                for i in range(len(v)):
                    outputs[k][i]["pred_masks"] = F.interpolate(
                        outputs[k][i]["pred_masks"].float(),
                        scale_factor=4,
                        mode="bilinear",
                        align_corners=False,
                    )
            elif k == "pred_masks":
                outputs[k] = F.interpolate(
                    outputs[k].float(),
                    scale_factor=4,
                    mode="bilinear",
                    align_corners=False,
                )
        return outputs

    def forward(self, outputs, gt_masks):
        """
        执行损失计算。
        参数:
             outputs: 张量的字典，参见模型的输出规范以获取格式。
             gt_masks: [bs, h_net_output, w_net_output]
        """
        # H, W = outputs["pred_masks"].shape[2:]
        # gt_masks = F.interpolate(gt_masks.float().unsqueeze(1), size=(H, W), mode='nearest').squeeze(1).long()
        outputs = self.postOutput(outputs)
        outputs_without_aux = {k: v for k, v in outputs.items() if k != "aux_outputs"}
        targets = self._get_targets(gt_masks)
        # 获取最后一层输出与目标之间的匹配
        indices = self.matcher(outputs_without_aux, targets)

        # 计算所有节点中目标框的平均数量，用于归一化目的
        num_masks = sum(len(t["labels"]) for t in targets)
        num_masks = torch.as_tensor([num_masks], dtype=torch.float, device=next(iter(outputs.values())).device)
        if is_dist_avail_and_initialized():
            torch.distributed.all_reduce(num_masks)
        num_masks = torch.clamp(num_masks / get_world_size(), min=1).item()

        # 计算所有损失
        losses = {}
        for loss in self.losses:
            losses.update(self.get_loss(loss, outputs, targets, indices, num_masks))

        # 如果有辅助损失，则对每个中间层的输出重复此过程。
        if "aux_outputs" in outputs:
            for i, aux_outputs in enumerate(outputs["aux_outputs"]):
                indices = self.matcher(aux_outputs, targets)
                for loss in self.losses:
                    l_dict = self.get_loss(loss, aux_outputs, targets, indices, num_masks)
                    l_dict = {k + f"_{i}": v for k, v in l_dict.items()}
                    losses.update(l_dict)
        loss_ce = 0.0
        loss_dice = 0.0
        loss_mask = 0.0
        for k in list(losses.keys()):
            if k in self.weight_dict:
                losses[k] *= self.weight_dict[k]
                if '_ce' in k:
                    loss_ce += losses[k]
                elif '_dice' in k:
                    loss_dice += losses[k]
                elif '_mask' in k:
                    loss_mask += losses[k]
            else:
                # 如果在 `weight_dict` 中未指定，则删除此损失
                losses.pop(k)
        loss = loss_ce + loss_dice + loss_mask
        losses["loss_tot"] = loss
        return losses

    def _get_binary_mask(self, target):
        y, x = target.size()
        target_onehot = torch.zeros(self.num_classes + 1, y, x).to(target.device)
        target_onehot = target_onehot.scatter(dim=0, index=target.unsqueeze(0), value=1)
        return target_onehot

    def _get_targets(self, gt_masks):
        targets = []
        for mask in gt_masks:
            binary_masks = self._get_binary_mask(mask)
            cls_label = torch.unique(mask)
            labels = cls_label[:] if cls_label[0] != 0 else cls_label[1:]  # TODO for FBP
            binary_masks = binary_masks[labels]
            targets.append({'masks': binary_masks, 'labels': labels})
        return targets

    def __repr__(self):
        head = "Criterion " + self.__class__.__name__
        body = [
            "matcher: {}".format(self.matcher.__repr__(_repr_indent=8)),
            "losses: {}".format(self.losses),
            "weight_dict: {}".format(self.weight_dict),
            "num_classes: {}".format(self.num_classes),
            "eos_coef: {}".format(self.eos_coef),
            "num_points: {}".format(self.num_points),
            "oversample_ratio: {}".format(self.oversample_ratio),
            "importance_sample_ratio: {}".format(self.importance_sample_ratio),
        ]
        _repr_indent = 4
        lines = [head] + [" " * _repr_indent + line for line in body]
        return "\n".join(lines)


class Criterion(object):
    def __init__(self, num_classes, alpha=0.5, gamma=2, weight=None, ignore_index=0):
        self.num_classes = num_classes
        self.alpha = alpha
        self.gamma = gamma
        self.weight = weight
        self.ignore_index = ignore_index
        self.smooth = 1e-5
        self.ce_fn = nn.CrossEntropyLoss(weight=self.weight, ignore_index=self.ignore_index, reduction='none')

    def get_loss(self, outputs, gt_masks):
        """执行损失计算。
        参数:
             outputs: 张量的字典，查看模型的输出规范以了解格式
             gt_masks: [bs, h_net_output, w_net_output]
        """
        loss_labels = 0.0
        loss_masks = 0.0
        loss_dices = 0.0
        num = gt_masks.shape[0]
        pred_logits = [outputs["pred_logits"].float()]  # [bs, num_query, num_classes + 1]
        pred_masks = [outputs['pred_masks'].float()]  # [bs, num_query, h, w]
        targets = self._get_targets(gt_masks, pred_logits[0].shape[1], pred_logits[0].device)
        for aux_output in outputs['aux_outputs']:
            pred_logits.append(aux_output["pred_logits"].float())
            pred_masks.append(aux_output["pred_masks"].float())

        gt_label = targets['labels']  # [bs, num_query]
        gt_mask_list = targets['masks']
        for mask_cls, pred_mask in zip(pred_logits, pred_masks):
            loss_labels += F.cross_entropy(mask_cls.transpose(1, 2), gt_label)
            # loss_masks += self.focal_loss(pred_result, gt_masks.to(pred_result.device))
            loss_dices += self.dice_loss(pred_mask, gt_mask_list)

        return loss_labels / num, loss_dices / num

    def binary_dice_loss(self, inputs, targets):
        inputs = inputs.sigmoid()
        inputs = inputs.flatten(1)
        targets = targets.flatten(1)
        numerator = 2 * torch.einsum("nc,mc->nm", inputs, targets)
        denominator = inputs.sum(-1)[:, None] + targets.sum(-1)[None, :]
        loss = 1 - (numerator + 1) / (denominator + 1)
        return loss.mean()

    def dice_loss(self, predict, targets):
        bs = predict.shape[0]
        total_loss = 0
        for i in range(bs):
            pred_mask = predict[i]
            tgt_mask = targets[i].to(predict.device)
            dice_loss_value = self.binary_dice_loss(pred_mask, tgt_mask)
            total_loss += dice_loss_value
        return total_loss / bs

    def focal_loss(self, preds, labels):
        """
        preds: [bs, num_class + 1, h, w]
        labels: [bs, h, w]
        """
        logpt = -self.ce_fn(preds, labels)
        pt = torch.exp(logpt)
        loss = -((1 - pt) ** self.gamma) * self.alpha * logpt
        return loss.mean()

    def _get_binary_mask(self, target):
        y, x = target.size()
        target_onehot = torch.zeros(self.num_classes + 1, y, x)
        target_onehot = target_onehot.scatter(dim=0, index=target.unsqueeze(0), value=1)
        return target_onehot

    def _get_targets(self, gt_masks, num_query, device):
        binary_masks = []
        gt_labels = []
        for mask in gt_masks:
            mask_onehot = self._get_binary_mask(mask)
            cls_label = torch.unique(mask)
            labels = torch.full((num_query,), 0, dtype=torch.int64, device=gt_masks.device)
            labels[:len(cls_label)] = cls_label
            binary_masks.append(mask_onehot[cls_label])
            gt_labels.append(labels)
        return {"labels": torch.stack(gt_labels).to(device), "masks": binary_masks}
