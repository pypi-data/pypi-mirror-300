from ..semseg.base import BaseNet

import torch
from torch import nn
import torch.nn.functional as F

from ..semseg.GCM import Global_Context_Module

class DeepLabV3Plus(BaseNet):
    def __init__(self, backbone, nclass, isContext: bool = False):
        super(DeepLabV3Plus, self).__init__(backbone)
        self.isContext = isContext
        print(f"isContext = {self.isContext}")
        if self.isContext:
            self.GCM = Global_Context_Module(channels=self.backbone.channels)
        low_level_channels = self.backbone.channels[0]
        high_level_channels = self.backbone.channels[-1]

        self.head = ASPPModule(high_level_channels, (12, 24, 36))

        self.reduce = nn.Sequential(nn.Conv2d(low_level_channels, 48, 1, bias=False),
                                    nn.BatchNorm2d(48),
                                    nn.ReLU(True))

        self.fuse = nn.Sequential(nn.Conv2d(high_level_channels // 8 + 48, 256, 3, padding=1, bias=False),
                                  nn.BatchNorm2d(256),
                                  nn.ReLU(True),

                                  nn.Conv2d(256, 256, 3, padding=1, bias=False),
                                  nn.BatchNorm2d(256),
                                  nn.ReLU(True),
                                  nn.Dropout(0.1, False))

        self.classifier = nn.Conv2d(256, nclass, 1, bias=True)

    def base_forward0(self, x):
        h, w = x.shape[-2:]

        c1, _, _, c4 = self.backbone.base_forward(x)

        c4 = self.head(c4)
        c4 = F.interpolate(c4, size=c1.shape[-2:], mode="bilinear", align_corners=True)

        c1 = self.reduce(c1)

        out = torch.cat([c1, c4], dim=1)
        out_feat = self.fuse(out)
        # feature = F.interpolate(out_feat, size=(h, w), mode="bilinear", align_corners=True)
        out = self.classifier(out_feat)
        out = F.interpolate(out, size=(h, w), mode="bilinear", align_corners=True)
        return out

    def base_forward_context(self, xs):
        x1, x2, x3 = xs
        with torch.no_grad():
            f2 = self.backbone.base_forward(x2)
            f3 = self.backbone.base_forward(x3)
        f1 = self.backbone.base_forward(x1)
        h, w = x1.shape[-2:]

        c1, _, _, c4 = self.GCM(f1, f2, f3)

        c4 = self.head(c4)
        c4 = F.interpolate(c4, size=c1.shape[-2:], mode="bilinear", align_corners=True)

        c1 = self.reduce(c1)

        out = torch.cat([c1, c4], dim=1)
        out_feat = self.fuse(out)
        # feature = F.interpolate(out_feat, size=(h, w), mode="bilinear", align_corners=True)
        out = self.classifier(out_feat)
        out = F.interpolate(out, size=(h, w), mode="bilinear", align_corners=True)
        return out

    def base_forward(self, x):
        if self.isContext:
            return self.base_forward_context(x)
        else:
            return self.base_forward0(x)


def ASPPConv(in_channels, out_channels, atrous_rate):
    block = nn.Sequential(nn.Conv2d(in_channels, out_channels, 3, padding=atrous_rate,
                                    dilation=atrous_rate, bias=False),
                          nn.BatchNorm2d(out_channels),
                          nn.ReLU(True))
    return block


class ASPPPooling(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(ASPPPooling, self).__init__()
        self.gap = nn.Sequential(nn.AdaptiveAvgPool2d(1),
                                 nn.Conv2d(in_channels, out_channels, 1, bias=False),
                                 nn.BatchNorm2d(out_channels),
                                 nn.ReLU(True))

    def forward(self, x):
        h, w = x.shape[-2:]
        pool = self.gap(x)
        return F.interpolate(pool, (h, w), mode="bilinear", align_corners=True)


class ASPPModule(nn.Module):
    def __init__(self, in_channels, atrous_rates):
        super(ASPPModule, self).__init__()
        out_channels = in_channels // 8
        rate1, rate2, rate3 = atrous_rates

        self.b0 = nn.Sequential(nn.Conv2d(in_channels, out_channels, 1, bias=False),
                                nn.BatchNorm2d(out_channels),
                                nn.ReLU(True))
        self.b1 = ASPPConv(in_channels, out_channels, rate1)
        self.b2 = ASPPConv(in_channels, out_channels, rate2)
        self.b3 = ASPPConv(in_channels, out_channels, rate3)
        self.b4 = ASPPPooling(in_channels, out_channels)

        self.project = nn.Sequential(nn.Conv2d(5 * out_channels, out_channels, 1, bias=False),
                                     nn.BatchNorm2d(out_channels),
                                     nn.ReLU(True),
                                     nn.Dropout2d(0.5, False))

    def forward(self, x):
        feat0 = self.b0(x)
        feat1 = self.b1(x)
        feat2 = self.b2(x)
        feat3 = self.b3(x)
        feat4 = self.b4(x)
        y = torch.cat((feat0, feat1, feat2, feat3, feat4), 1)
        return self.project(y)
