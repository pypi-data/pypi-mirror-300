# -*- coding: utf-8 -*-
from __future__ import annotations
import cv2
import numpy as np


def draw_points_shape(img, roi_points, color):
    for v in range(1, len(roi_points)):
        cv2.line(img, roi_points[v], roi_points[v - 1], color, 2)

    cv2.line(img, roi_points[0], roi_points[-1], color, 2)

    return img


def draw_contour(image: np.ndarray, points, fill: bool):
    points = np.array(points, dtype=np.int32)
    points = points.reshape((-1, 1, 2))

    if fill:
        cv2.fillPoly(image, [points], color=(255, 255, 255))
    else:
        cv2.polylines(image, [points], isClosed=True, color=(255, 255, 255), thickness=3)

    return image
