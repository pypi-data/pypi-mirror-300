from ..semseg.base import BaseNet
import torch
from torch import nn
import torch.nn.functional as F
from addict import Dict

from .utils_mask2former.pixel_decoder.msdeformattn import MSDeformAttnPixelDecoder
from .utils_mask2former.transformer_decoder.mask2former_transformer_decoder import MultiScaleMaskedTransformerDecoder


class Mask2Former(BaseNet):
    def __init__(self, backbone, nclass: int = 25):
        super(Mask2Former, self).__init__(backbone)
        self.backbone_feature_shape = dict()
        self.cal_shape()
        self.sem_seg_head = MaskFormerHead(input_shape=self.backbone_feature_shape,
                                           nclass=nclass)

    def cal_shape(self):
        out = self.backbone.base_forward(torch.randn((2, 3, 512, 512)))
        for i, x in enumerate(out):
            self.backbone_feature_shape[f'res{i + 2}'] = Dict({'channel': x.shape[1], 'stride': 512 // x.shape[2]})
        print("mask2former get features shapes:")
        print(self.backbone_feature_shape)

    def base_forward(self, x):
        h, w = x.shape[-2:]
        f = self.backbone.base_forward(x)
        features = dict()
        for i, x in enumerate(f):
            features[f'res{i + 2}'] = x
        outputs = self.sem_seg_head(features)
        if self.training:
            return outputs
        else:
            # delete last ==================#
            mask_cls = outputs["pred_logits"][..., 1:-1]
            mask_pred = outputs["pred_masks"]
            # delete last ==================#
            # delete first ==================#
            # last one ==>> first one
            # mask_cls = outputs["pred_logits"][..., 1:]
            # mask_cls = torch.cat((mask_cls[..., -1:], mask_cls[..., :-1]), dim=-1)
            # mask_pred = outputs["pred_masks"]
            # delete first ==================#
            mask_pred = F.interpolate(
                mask_pred,
                size=(h, w),
                mode="bilinear",
                align_corners=False,
            )
            mask_cls = F.softmax(mask_cls, dim=-1)
            mask_pred = mask_pred.sigmoid()
            pred_mask = torch.einsum("bqc,bqhw->bchw", mask_cls, mask_pred)
            return pred_mask
            # return F.interpolate(pred_mask, size=(h, w), mode="bilinear", align_corners=True)

            """
                mask_cls_results = outputs["pred_logits"]
                mask_pred_results = outputs["pred_masks"]
    
                mask_pred_results = F.interpolate(
                    mask_pred_results,
                    size=(inpurt_tensor.shape[-2], inpurt_tensor.shape[-1]),
                    mode="bilinear",
                    align_corners=False,
                )
                pred_masks = self.semantic_inference(mask_cls_results, mask_pred_results)
                    def semantic_inference(self, mask_cls, mask_pred):
                        mask_cls = F.softmax(mask_cls, dim=-1)[..., 1:]
                        mask_pred = mask_pred.sigmoid()
                        semseg = torch.einsum("bqc,bqhw->bchw", mask_cls, mask_pred)
                        return semseg.cpu().numpy()
                
                mask_img = np.argmax(pred_masks, axis=1)[0]
            """


class MaskFormerHead(nn.Module):
    def __init__(self, input_shape, nclass: int = 2):
        super().__init__()
        self.pixel_decoder = self.pixel_decoder_init(input_shape)
        self.predictor = self.predictor_init(nclass)

    def pixel_decoder_init(self, input_shape):
        common_stride = 4
        transformer_dropout = 0
        transformer_nheads = 8
        transformer_dim_feedforward = 1024
        transformer_enc_layers = 4
        conv_dim = 256
        mask_dim = 256
        transformer_in_features = ["res3", "res4", "res5"]

        pixel_decoder = MSDeformAttnPixelDecoder(input_shape,
                                                 transformer_dropout,
                                                 transformer_nheads,
                                                 transformer_dim_feedforward,
                                                 transformer_enc_layers,
                                                 conv_dim,
                                                 mask_dim,
                                                 transformer_in_features,
                                                 common_stride)
        return pixel_decoder

    def predictor_init(self, nclass):
        in_channels = 256
        num_classes = nclass
        hidden_dim = 256
        num_queries = 100
        nheads = 8
        dim_feedforward = 2048
        dec_layers = 10 - 1
        pre_norm = False
        mask_dim = 256
        enforce_input_project = False
        mask_classification = True
        predictor = MultiScaleMaskedTransformerDecoder(in_channels,
                                                       num_classes,
                                                       mask_classification,
                                                       hidden_dim,
                                                       num_queries,
                                                       nheads,
                                                       dim_feedforward,
                                                       dec_layers,
                                                       pre_norm,
                                                       mask_dim,
                                                       enforce_input_project)
        return predictor

    def forward(self, features, mask=None):
        mask_features, transformer_encoder_features, multi_scale_features = \
            self.pixel_decoder.forward_features(features)
        predictions = self.predictor(multi_scale_features, mask_features, mask)
        return predictions
