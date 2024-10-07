from typing import List, Tuple

import cv2
import numpy as np


def numpy_mask_to_yolo(mask: np.ndarray) -> List[float]:
    _, binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    height = mask.shape[0]
    width = mask.shape[1]
    contour_points = []
    for contour in contours:
        for point in contour:
            contour_points.extend((point[0][0] / height, point[0][1] / width))

    return contour_points


def yolo_mask_to_numpy(mask: np.ndarray | List[float], size: Tuple[int, int]) -> np.ndarray:
    img = np.zeros(size, dtype=np.uint8)
    coords = np.array(mask, dtype=np.float32).reshape(-1, 2)
    coords[:, 0] *= size[1]
    coords[:, 1] *= size[0]
    coords = coords.astype(int)
    cv2.fillPoly(img, [coords], 255)
    return img


def to_numpy(masks: List[List], size: Tuple[int, int]) -> List[List]:
    npy_masks = []
    for label, obj in masks:
        npy_mask = yolo_mask_to_numpy(obj, size)
        npy_masks.append([label, npy_mask])
    return npy_masks


def to_yolo(masks: List[List]) -> List[List]:
    yolo_masks = []
    for label, mask in masks:
        mask = numpy_mask_to_yolo(masks)
        yolo_masks.append([label, mask])
    return yolo_masks
