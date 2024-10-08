from collections import OrderedDict
from pprint import pprint

import numpy as np
from prettytable import PrettyTable


def intersect_and_union(pred_label: np.array, label: np.array,
                        num_classes: int, ignore_index: int):
    # Calculate Intersection and Union.

    mask = (label != ignore_index)
    pred_label = pred_label[mask] - 1
    label = label[mask] - 1

    intersect = pred_label[pred_label == label]
    area_intersect, _ = np.histogram(intersect, bins=num_classes, range=(0, num_classes - 1))
    area_pred_label, _ = np.histogram(pred_label, bins=num_classes, range=(0, num_classes - 1))
    area_label, _ = np.histogram(label, bins=num_classes, range=(0, num_classes - 1))

    area_intersect, _ = np.histogram(intersect, bins=num_classes - 1, range=(0, num_classes - 1 - 1))
    area_pred_label, _ = np.histogram(pred_label, bins=num_classes - 1, range=(0, num_classes - 1 - 1))
    area_label, _ = np.histogram(label, bins=num_classes - 1, range=(0, num_classes - 1 - 1))

    area_union = area_pred_label + area_label - area_intersect
    # return area_intersect[1:], area_union[1:], area_pred_label[1:], area_label[1:]
    return area_intersect, area_union, area_pred_label, area_label


def intersect_and_union1(pred_label: np.array, label: np.array,
                         num_classes: int, ignore_index: int):
    # Calculate Intersection and Union.

    mask = (label != ignore_index)
    pred_label = pred_label[mask]
    label = label[mask]

    intersect = pred_label[pred_label == label]
    area_intersect = np.bincount(intersect, minlength=num_classes)
    area_pred_label = np.bincount(pred_label, minlength=num_classes)
    area_label = np.bincount(label, minlength=num_classes)

    area_union = area_pred_label + area_label - area_intersect
    return area_intersect, area_union, area_pred_label, area_label


def total_area_to_metrics(total_area_intersect: np.ndarray,
                          total_area_union: np.ndarray,
                          total_area_pred_label: np.ndarray,
                          total_area_label: np.ndarray,
                          metrics=['mIoU', 'mDice', 'mFscore'],
                          nan_to_num=None,
                          beta: int = 1):
    # Calculate evaluation metrics

    def f_score(precision, recall, beta=1):
        # calculate the f-score value.

        score = (1 + beta ** 2) * (precision * recall) / (
                (beta ** 2 * precision) + recall)
        return score

    if isinstance(metrics, str):
        metrics = [metrics]
    allowed_metrics = ['mIoU', 'mDice', 'mFscore']
    if not set(metrics).issubset(set(allowed_metrics)):
        raise KeyError(f'metrics {metrics} is not supported')

    all_acc = total_area_intersect.sum() / total_area_label.sum()
    ret_metrics = OrderedDict({'aAcc': all_acc})
    for metric in metrics:
        if metric == 'mIoU':
            iou = total_area_intersect / total_area_union
            acc = total_area_intersect / total_area_label
            ret_metrics['IoU'] = iou
            ret_metrics['Acc'] = acc
        elif metric == 'mDice':
            dice = 2 * total_area_intersect / (
                    total_area_pred_label + total_area_label)
            acc = total_area_intersect / total_area_label
            ret_metrics['Dice'] = dice
            ret_metrics['Acc'] = acc
        elif metric == 'mFscore':
            precision = total_area_intersect / total_area_pred_label
            recall = total_area_intersect / total_area_label
            f_value = np.array([
                f_score(x[0], x[1], beta) for x in zip(precision, recall)
            ])
            ret_metrics['Fscore'] = f_value
            ret_metrics['Precision'] = precision
            ret_metrics['Recall'] = recall

    ret_metrics = {
        metric: value
        for metric, value in ret_metrics.items()
    }
    if nan_to_num is not None:
        ret_metrics = OrderedDict({
            metric: np.nan_to_num(metric_value, nan=nan_to_num)
            for metric, metric_value in ret_metrics.items()
        })
    return ret_metrics


def compute_metrics(results: list):
    # Compute the metrics from processed results.

    # convert list of tuples to tuple of lists, e.g.
    # [(A_1, B_1, C_1, D_1), ...,  (A_n, B_n, C_n, D_n)] to
    # ([A_1, ..., A_n], ..., [D_1, ..., D_n])
    results = tuple(zip(*results))
    assert len(results) == 4

    total_area_intersect = sum(results[0])
    total_area_union = sum(results[1])
    total_area_pred_label = sum(results[2])
    total_area_label = sum(results[3])
    ret_metrics = total_area_to_metrics(
        total_area_intersect, total_area_union, total_area_pred_label, total_area_label,
        metrics=['mIoU', 'mDice', 'mFscore'],
        nan_to_num=None,
        beta=1)

    class_names = [str(i) for i in range(24)]
    # summary table
    ret_metrics_summary = OrderedDict({
        ret_metric: np.round(np.nanmean(ret_metric_value) * 100, 5)
        for ret_metric, ret_metric_value in ret_metrics.items()
    })
    metrics = dict()
    for key, val in ret_metrics_summary.items():
        if key == 'aAcc':
            metrics[key] = val
        else:
            metrics['m' + key] = val

    # each class table
    ret_metrics.pop('aAcc', None)
    ret_metrics_class = OrderedDict({
        ret_metric: np.round(ret_metric_value * 100, 2)
        for ret_metric, ret_metric_value in ret_metrics.items()
    })
    ret_metrics_class.update({'Class': class_names})
    ret_metrics_class.move_to_end('Class', last=False)
    class_table_data = PrettyTable()
    for key, val in ret_metrics_class.items():
        class_table_data.add_column(key, val)

    print('per class results:')
    print(class_table_data.get_string())

    return metrics


class Evaluator(object):
    def __init__(self, num_class, ignore_index=-1):
        self.num_class = num_class
        self.ignore_index = ignore_index
        self.batch_results = []

    def reset(self):
        self.batch_results.clear()

    def add_batch(self, gt_image, pre_image):
        # gt [0:n-1] <==> pre [0:n-1]
        assert gt_image.shape == pre_image.shape, f"{gt_image.shape}!={pre_image.shape}"
        self.batch_results.append(intersect_and_union(pred_label=pre_image, label=gt_image,
                                                      num_classes=25, ignore_index=0))


if __name__ == '__main__':
    import os, cv2

    name = "GF2_PMS2__L1A0001119060-MSS2.png"
    name = "GF2_PMS2__L1A0000718813-MSS2.png"
    gt = cv2.imread(os.path.join(r"F:\data_lwc\FBP\test\label", name), 0)
    pr = cv2.imread(os.path.join(r"F:\data_lwc\FBP\test\mask2former\FBP_1024\d2", name), 0)
    arr = []
    for name in os.listdir(r"F:\data_lwc\FBP\test\label"):
        # if name == "GF2_PMS2__L1A0001119060-MSS2.png": continue
        # name = "GF2_PMS2__L1A0001119060-MSS2.png"
        print(name)
        gt = cv2.imread(os.path.join(r"F:\data_lwc\FBP\test\label", name), 0)[54:6800 + 54, 60:7200 + 60]
        pr = cv2.imread(os.path.join(r"D:\git\wbuilding\PFNet_IPNet\result\mask2former\FBP\testcw", name), 0)
        arr.append(intersect_and_union(pred_label=pr, label=gt,
                                       num_classes=25, ignore_index=0))
        # break
    print(len(arr))
    m = compute_metrics(arr)
    pprint(m)
