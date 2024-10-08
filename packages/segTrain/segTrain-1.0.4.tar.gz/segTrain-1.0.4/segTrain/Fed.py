import torch
import torch.nn as nn
import torch.nn.functional as F
from scipy.optimize import linear_sum_assignment
from torch.cuda.amp import autocast


def calIoU(mask1, mask2, eps=10 ** -9):
    mask1 = mask1 > 0.5
    mask2 = mask2 > 0.5

    intersection = torch.logical_and(mask1.unsqueeze(1), mask2.unsqueeze(0)).sum(dim=(2, 3))
    union = torch.logical_or(mask1.unsqueeze(1), mask2.unsqueeze(0)).sum(dim=(2, 3))

    iou = intersection.float() / (union.float() + eps)

    return iou


def batch_kl_loss(inputs: torch.Tensor, targets: torch.Tensor):
    """
    Compute the KL divergence matrix between two sets of distributions.
    """
    # Apply softmax to convert logits to probabilities
    inputs = F.softmax(inputs.flatten(1), dim=-1)  # [q,c]
    targets = F.softmax(targets.flatten(1), dim=-1)  # [q,c]

    kl_matrix = torch.einsum("qxc,qmc->qm", targets[:, None, :],
                             torch.log(targets[:, None, :] + 1e-10) - torch.log(inputs + 1e-10))
    
    return kl_matrix


@torch.no_grad()
def memory_efficient_forward(outmasks1, outmasks2):
    """More memory-friendly matching"""
    bs, num_queries = outmasks1.shape[:2]

    indices = []

    # Iterate through batch size
    for b in range(bs):
        out_mask1 = outmasks1[b]
        out_mask2 = outmasks2[b]

        with autocast(enabled=False):
            # Compute the cost between masks
            cost_mask = batch_kl_loss(out_mask1, out_mask2)
            # cost_mask = calIoU(out_mask1, out_mask2)
        # print(cost_mask.shape, "\n", cost_mask)
        # Final cost matrix
        C = cost_mask
        C = C.reshape(num_queries, -1).cpu()  # [num_queries, num_total_targets]

        indices.append(linear_sum_assignment(C))

    return [
        (torch.as_tensor(i, dtype=torch.int64), torch.as_tensor(j, dtype=torch.int64))
        for i, j in indices
    ]


def crop(input, shape):
    h0, w0 = shape
    h, w = input.shape[-2:]
    dh = (h - h0) // 2
    dw = (w - w0) // 2
    return input[..., dh:dh + h0, dw:dw + h0]


class FedTrain(object):
    def __init__(self, device="cpu", deviceC="cpu", downsample_tuple=(1, 2, 4)):
        self.device = device
        self.deviceC = deviceC
        assert len(downsample_tuple) == 3
        d1, d2, d3 = downsample_tuple
        assert d1 == 1
        self.d1 = d1
        self.d2 = d2
        self.w2 = 1 / d2
        self.d3 = d3
        self.w3 = 1 / d3
        self.kl_loss = nn.KLDivLoss(reduction="batchmean")

    def CalKL(self, input, target):
        KLloss = self.kl_loss(F.log_softmax(input, dim=1), F.softmax(target, dim=1))
        return KLloss

    def Align(self, InputList):
        feat1, feat2, feat3 = InputList
        h, w = feat1.shape[-2:]
        feat2 = F.interpolate(feat2, scale_factor=self.d2, mode="bilinear", align_corners=False)
        feat3 = F.interpolate(feat2, scale_factor=self.d3, mode="bilinear", align_corners=False)
        return feat1, crop(feat2, (h, w)), crop(feat3, (h, w))

    def _get_permutation_idx1(self, indices):
        # permute idx1 following indices
        batch_idx = torch.cat([torch.full_like(src, i) for i, (src, _) in enumerate(indices)])
        src_idx = torch.cat([src for (src, _) in indices])
        return batch_idx, src_idx

    def _get_permutation_idx2(self, indices):
        # permute targets following indices
        batch_idx = torch.cat([torch.full_like(tgt, i) for i, (_, tgt) in enumerate(indices)])
        tgt_idx = torch.cat([tgt for (_, tgt) in indices])
        return batch_idx, tgt_idx

    def calLoss(self, indices, resA, resB):
        idxA = self._get_permutation_idx1(indices)
        # print(idxA)
        resALabel = resA["pred_logits"][idxA]
        # resAMask = resA["pred_masks"][idxA]

        idxB = self._get_permutation_idx2(indices)
        resBLabel = resB["pred_logits"][idxB]
        # resBMask = resB["pred_masks"][idxB]
        # print(resALabel.shape, resBLabel.shape, resAMask.shape, resBMask.shape)

        return self.CalKL(resALabel.to(self.device), resBLabel.to(self.device))

    def trainer(self, out1, out2, out3):
        # "pred_logits" [bs,q,nclass]
        # "pred_masks" [bs,q,h,w]

        # Align
        _, _, h, w = out1["pred_masks"].shape
        out2["pred_masks"] = crop(
            F.interpolate(out2["pred_masks"], scale_factor=self.d2, mode="bilinear", align_corners=False),
            (h, w)).to(self.deviceC)
        out3["pred_masks"] = crop(
            F.interpolate(out3["pred_masks"], scale_factor=self.d3, mode="bilinear", align_corners=False),
            (h, w)).to(self.deviceC)
        match12 = memory_efficient_forward(out1["pred_masks"].to(self.deviceC), out2["pred_masks"])
        match13 = memory_efficient_forward(out1["pred_masks"].to(self.deviceC), out3["pred_masks"])

        loss12 = self.calLoss(match12, out1, out2)
        loss13 = self.calLoss(match13, out1, out3)
        return loss12 * self.w2 + loss13 * self.w3


if __name__ == "__main__":
    a, b = torch.ones((1, 4, 4)), torch.zeros((1, 4, 4))
    a[0, 1, 1] = 0
    b[0, 0, 0] = 1
    print(a, "\n", b)
    print(calIoU(torch.cat((a, b), dim=0), torch.cat((b, a), dim=0)))
    print(memory_efficient_forward(torch.cat((a, b, a), dim=0).unsqueeze(0),
                                   torch.cat((b, a, a), dim=0).unsqueeze(0)))

    output = F.kl_div(F.log_softmax(a.flatten(1), dim=-1), F.softmax(b.flatten(1), dim=-1), reduction='batchmean')
    print(1, output)

    output = F.kl_div(F.log_softmax(b.flatten(1), dim=-1), F.softmax(a.flatten(1), dim=-1), reduction='batchmean')
    print(2, output)
    print(aa)
    s = 128
    nclass = 26
    bs = 2
    featsList, predList = [], []
    out1 = {"pred_logits": torch.randn((bs, 100, nclass), requires_grad=True),
            "pred_masks": torch.randn((bs, 100, s, s), requires_grad=True)}
    out2 = {"pred_logits": torch.randn((bs, 100, nclass)),
            "pred_masks": torch.randn(bs, 100, s, s)}
    out3 = {"pred_logits": torch.randn((bs, 100, nclass)),
            "pred_masks": torch.randn(bs, 100, s, s)}
    f = FedTrain()
    l = f.trainer(out1, out2, out3)
    print(l)


    def batch_dice_loss(inputs: torch.Tensor, targets: torch.Tensor):
        """
        Compute the DICE loss, similar to generalized IOU for masks
        Args:
            inputs: A float tensor of arbitrary shape.
                    The predictions for each example.
            targets: A float tensor with the same shape as inputs. Stores the binary
                     classification label for each element in inputs
                    (0 for the negative class and 1 for the positive class).
        """
        inputs = inputs.sigmoid()
        inputs = inputs.flatten(1)
        numerator = 2 * torch.einsum("nc,mc->nm", inputs, targets)
        denominator = inputs.sum(-1)[:, None] + targets.sum(-1)[None, :]
        loss = 1 - (numerator + 1) / (denominator + 1)
        return loss


    y = batch_dice_loss(inputs=torch.randn(100, 200), targets=torch.ones(8, 200))
    print(y.shape)

    print(torch.randn(3, 6, 8).flatten(1).shape)
