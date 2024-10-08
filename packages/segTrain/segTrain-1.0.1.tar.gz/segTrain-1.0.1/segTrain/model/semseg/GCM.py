import torch
from torch import nn
import torch.nn.functional as F


# pytorch 1.7.0
class Global_Context_Module(nn.Module):
    def __init__(self, channels, nHeads: int = 2, nLayers: int = 3):
        super(Global_Context_Module, self).__init__()
        assert len(channels) == 4  # 四组特征的通道数
        assert nLayers == 3
        c1, c2, c3, c4 = channels

        self.attention12 = nn.ModuleList()
        self.attention13 = nn.ModuleList()
        self.Squeue = nn.ModuleList()
        for c in (c2, c3, c4):
            self.attention12.append(nn.MultiheadAttention(embed_dim=c, num_heads=nHeads))
            self.attention13.append(nn.MultiheadAttention(embed_dim=c, num_heads=nHeads))
            self.Squeue.append(nn.Conv2d(c * nLayers, c, kernel_size=1, stride=1, padding=0))

    @staticmethod
    def att(q, kv, attention, saveName=None):
        # q,kv [bs,c,h,w]
        # attention nn.MultiheadAttention
        # (L,N,E)
        # where L is the target sequence length, N is the batch size, E is the embedding dimension.
        # return q
        # 将图像特征展平为序列长度
        bs, c, h, w = q.shape
        q = q.flatten(2).permute(2, 0, 1)  # h*w,bs,c
        kv = kv.flatten(2).permute(2, 0, 1)

        output, _ = attention(q, kv, kv)
        output = output.permute(1, 2, 0)  # (batch_size, embed_dim, seq_len)
        output = output.view(bs, c, h, w)  # (batch_size, embed_dim, height, width)

        return output

    def forward(self, f1, f2, f3):
        """
        :param f1: 来自小视场图像的特征，有四组 已经有梯度
        :param f2: 来自中视场图像的特征，有四组
        :param f3: 来自大视场图像的特征，有四组
        :return: 融合之后的特征，四组
        """
        outFeats = []

        for i, x in enumerate(zip(f1, f2, f3)):
            fx1, fx2, fx3 = x
            if i == 0:
                outFeats.append(fx1)
                continue
            fx2.requires_grad = True
            fx3.requires_grad = True
            Fx = torch.cat((fx1,
                            self.att(q=fx1, kv=fx2, attention=self.attention12[i - 1]),
                            self.att(q=fx1, kv=fx3, attention=self.attention13[i - 1])),
                           dim=1)
            outFeats.append(self.Squeue[i - 1](Fx))
        return outFeats
