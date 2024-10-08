from .backbone import resnet, swin_transformer, checkpoint
from .semseg.deeplabv3plus import DeepLabV3Plus


def build_model(backbone, nclass, segHead="deeplabV3P"):
    if segHead == "deeplabV3P":
        net = DeepLabV3Plus(backbone=backbone, nclass=nclass)
    else:
        raise EnvironmentError
    return net
