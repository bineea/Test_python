#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cv2
import numpy as np



# ---------------- 画图专用 ----------------#
def draw_point(img, points):
    # 绘制点
    for position in points:
        cv2.circle(img, position, 5, (255, 0, 255), -1)


def draw_line(img, lines):
    # 绘制直线
    for line_points in lines:
        cv2.line(img, (line_points[0][0], line_points[0][1]), (line_points[0][2], line_points[0][3]),
                 (0, 255, 0), 2, 8, 0)


def img_show(window_name, img, need_close_window=True):
    # 展示图片(展示后关闭)
    cv2.imshow(window_name, img)
    if need_close_window:
        cv2.waitKey(0)
        cv2.destroyAllWindows()


