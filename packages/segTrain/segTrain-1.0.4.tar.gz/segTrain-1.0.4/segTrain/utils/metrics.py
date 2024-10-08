import os, cv2
import numpy as np
from tqdm import tqdm
from PIL import Image
import warnings

warnings.filterwarnings("ignore")
Image.MAX_IMAGE_PIXELS = None


class Evaluator(object):
    def __init__(self, num_class, ignore_index=-1):
        # assert ignore_index in (-1, 0)
        self.num_class = num_class - 1 if ignore_index >= 0 else num_class
        self.ignore_index = ignore_index
        self.confusion_matrix = np.zeros((self.num_class,) * 2)

    def Pixel_Accuracy(self):
        Acc = np.diag(self.confusion_matrix).sum() / self.confusion_matrix.sum()
        return Acc

    def Pixel_Accuracy_Class(self):
        Acc = np.diag(self.confusion_matrix) / self.confusion_matrix.sum(axis=1)
        Acc = np.nanmean(Acc)
        return Acc

    def Mean_Intersection_over_Union(self):
        IoU = np.diag(self.confusion_matrix) / (
                np.sum(self.confusion_matrix, axis=1) + np.sum(self.confusion_matrix, axis=0) -
                np.diag(self.confusion_matrix))
        MIoU = np.nanmean(IoU)
        return MIoU

    def Frequency_Weighted_Intersection_over_Union(self):
        freq = np.sum(self.confusion_matrix, axis=1) / np.sum(self.confusion_matrix)
        iu = np.diag(self.confusion_matrix) / (
                np.sum(self.confusion_matrix, axis=1) + np.sum(self.confusion_matrix, axis=0) -
                np.diag(self.confusion_matrix))
        FWIoU = (freq[freq > 0] * iu[freq > 0]).sum()
        return FWIoU

    def F1_Score(self, idx=-1):
        """
        :param idx: if -1, all classes will be compute, else only idx
        :return: f1_score
        """
        precision = np.diag(self.confusion_matrix) / np.sum(self.confusion_matrix, axis=0)
        recall = np.diag(self.confusion_matrix) / np.sum(self.confusion_matrix, axis=1)
        f1_score = 2 * precision * recall / (precision + recall)
        if idx < 0:
            return np.nanmean(f1_score)
        else:
            return f1_score[idx]

    def generate_matrix(self, gt_image, pre_image):
        mask = gt_image != self.ignore_index
        label = self.num_class * (gt_image[mask] - 1).astype('int') + (pre_image[mask]).astype('int')
        count = np.bincount(label, minlength=self.num_class ** 2)
        confusion_matrix = count.reshape(self.num_class, self.num_class)
        return confusion_matrix

    def generate_matrix1(self, gt_image, pre_image):
        label = self.num_class * gt_image.astype('int') + pre_image.astype('int')
        count = np.bincount(np.ravel(label), minlength=self.num_class ** 2)
        confusion_matrix = count.reshape(self.num_class, self.num_class)
        return confusion_matrix

    def add_batch(self, gt_image, pre_image):
        assert gt_image.shape == pre_image.shape, f"{gt_image.shape}!={pre_image.shape}"
        if self.ignore_index >= 0:
            self.confusion_matrix += self.generate_matrix(gt_image, pre_image)
        else:
            self.confusion_matrix += self.generate_matrix1(gt_image, pre_image)

    def reset(self):
        self.confusion_matrix = np.zeros((self.num_class,) * 2)

    def cal_metrics0(self):
        precision = np.diag(self.confusion_matrix) / np.sum(self.confusion_matrix, axis=0)
        recall = np.diag(self.confusion_matrix) / np.sum(self.confusion_matrix, axis=1)
        f1_score = 2 * precision * recall / (precision + recall)
        iou = np.diag(self.confusion_matrix) / (
                np.sum(self.confusion_matrix, axis=0) + np.sum(self.confusion_matrix, axis=1) -
                np.diag(self.confusion_matrix))
        # miou = np.nanmean(iou)
        oa = np.diag(self.confusion_matrix).sum() / self.confusion_matrix.sum()

        print("Precision:\n", precision[self.ignore_index + 1:])
        print("Recall:\n", recall[self.ignore_index + 1:])
        print("F1 Score:\n", f1_score[self.ignore_index + 1:])
        print("IoU:\n", iou[self.ignore_index + 1:])

        print("mPrecision:\n", np.nanmean(precision[self.ignore_index + 1:]))
        print("mRecall:\n", np.nanmean(recall[self.ignore_index + 1:]))
        print("mF1:\n", np.nanmean(f1_score[self.ignore_index + 1:]))
        print("mIoU:\n", np.nanmean(iou[self.ignore_index + 1:]))
        print("FWIoU:\n", self.Frequency_Weighted_Intersection_over_Union())

        print("Overall Accuracy (OA):\n", oa)

    def cal_metrics(self):
        precision = np.diag(self.confusion_matrix) / np.sum(self.confusion_matrix, axis=0)
        recall = np.diag(self.confusion_matrix) / np.sum(self.confusion_matrix, axis=1)
        f1_score = 2 * precision * recall / (precision + recall)
        iou = np.diag(self.confusion_matrix) / (
                np.sum(self.confusion_matrix, axis=0) + np.sum(self.confusion_matrix, axis=1) -
                np.diag(self.confusion_matrix))
        # miou = np.nanmean(iou)
        oa = np.diag(self.confusion_matrix).sum() / self.confusion_matrix.sum()

        print("Precision:\n", precision)
        print("Recall:\n", recall)
        print("F1 Score:\n", f1_score)
        print("IoU:\n", iou)

        print("mPrecision:\n", np.nanmean(precision))
        print("mRecall:\n", np.nanmean(recall))
        print("mF1:\n", np.nanmean(f1_score))
        print("mIoU:\n", np.nanmean(iou))
        print("FWIoU:\n", self.Frequency_Weighted_Intersection_over_Union())

        print("Overall Accuracy (OA):\n", oa)


def cal_metrics(pre_path, ann_path, nclass, ignore_index):
    print("====================evaluating====================")
    print(f"pre_path = {pre_path}")
    print(f"ann_path = {ann_path}")
    print(f"ncalss = {nclass}")
    print(f"ignore_index = {ignore_index}")
    evaluator = Evaluator(nclass, ignore_index=ignore_index)
    evaluator.reset()
    for name in tqdm(os.listdir(pre_path)):
        ann = np.array(Image.open(os.path.join(ann_path, name))).astype(np.uint8)
        pre = np.array(Image.open(os.path.join(pre_path, name))).astype(np.uint8)
        if nclass == 2:
            ann[ann > 0] = 1
            pre[pre > 0] = 1
        evaluator.add_batch(ann, pre)
    evaluator.cal_metrics()
    print("==================================================")


# General util function to get the boundary of a binary mask.
def mask_to_boundary(mask, dilation_ratio=0.2):
    """
    Convert binary mask to boundary mask.
    :param mask (numpy array, uint8): binary mask
    :param dilation_ratio (float): ratio to calculate dilation = dilation_ratio * image_diagonal
    :return: boundary mask (numpy array)
    """
    h, w = mask.shape
    img_diag = np.sqrt(h ** 2 + w ** 2)
    dilation = int(round(dilation_ratio * img_diag))
    if dilation < 1:
        dilation = 1
    # Pad image so mask truncated by the image border is also considered as boundary.
    new_mask = cv2.copyMakeBorder(mask, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
    kernel = np.ones((3, 3), dtype=np.uint8)
    new_mask_erode = cv2.erode(new_mask, kernel, iterations=dilation)
    mask_erode = new_mask_erode[1: h + 1, 1: w + 1]
    # G_d intersects G in the paper.
    return mask - mask_erode


def boundary_iou(gt, dt, dilation_ratio=0.2):
    """
    Compute boundary iou between two binary masks.
    :param gt (numpy array, uint8): binary mask
    :param dt (numpy array, uint8): binary mask
    :param dilation_ratio (float): ratio to calculate dilation = dilation_ratio * image_diagonal
    :return: boundary iou (float)
    """
    gt_boundary = mask_to_boundary(gt, dilation_ratio)
    dt_boundary = mask_to_boundary(dt, dilation_ratio)
    intersection = ((gt_boundary * dt_boundary) > 0).sum()
    union = ((gt_boundary + dt_boundary) > 0).sum()
    # boundary_iou = intersection / union
    return intersection, union  # , boundary_iou


def cal_boundaryIoU(pre_path, ann_path, dilation_ratio=0.2):
    print("====================boundaryIoU====================")
    print(f"pre_path = {pre_path}")
    print(f"ann_path = {ann_path}")
    print(f"dilation_ratio={dilation_ratio}")
    boundary_intersection = 0
    boundary_union = 0
    for name in tqdm(os.listdir(labels)):
        pre = np.array(Image.open(os.path.join(pres, name))).astype("uint8")
        ann = np.array(Image.open(os.path.join(labels, name))).astype("uint8")
        pre[pre < 128] = 0
        pre[pre >= 128] = 1
        ann[ann < 100] = 0
        ann[ann > 100] = 1
        i, u = boundary_iou(gt=ann, dt=pre, dilation_ratio=dilation_ratio)
        boundary_union += u
        boundary_intersection += i
    print('boundary_iou: %.8f%%' % (boundary_intersection / boundary_union * 100))
    print("===================================================")


if __name__ == '__main__':
    # cal_metrics(pre_path=r"D:\git\wbuilding\PFNet_IPNet\result\512\upernet\context_upernet512_1_5_10",
    #             ann_path=r"F:\data_lwc\FBP\test\label",
    #             nclass=25,
    #             ignore_index=0)
    labels = rf"F:\data_lwc\FBP\test\label"
    out_path_m = rf"F:\data_lwc\FBP\test\ipnet"
    cal_metrics(pre_path=out_path_m, ann_path=labels, nclass=25, ignore_index=0)
    print(xxx)
    cal_metrics(pre_path=r"F:\data_lwc\HPD\result\HPD_normal_swinl_upernet_512_1",
                ann_path=r"F:\data_lwc\HPD\test\label",
                nclass=10,
                ignore_index=0)
    cal_metrics(pre_path=r"F:\data_lwc\HPD\result\HPD_context_swinl_upernet_512_1_5_10",
                ann_path=r"F:\data_lwc\HPD\test\label",
                nclass=10,
                ignore_index=0)

