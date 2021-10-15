import cv2
import numpy as np
#from util_tools import *
import contourutil
import imutils


"""
寻找包裹区域
返回仅包含包裹的图
"""
def find_package(img, rect, vis_result=False):
    # -------------- 包裹区域定位 -------------------

    # 高斯模糊原图，为前景识别减少背景干扰
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    cv2.dilate(img, se, img)
    gaussian_img = cv2.GaussianBlur(img, (5, 5), 0)
    # cv2.imshow('gaussian_img', gaussian_img)

    # 选取roi区域
    img = gaussian_img.copy()
    cv2.rectangle(img, (int(rect[0]), int(rect[1])), (int(rect[0]) + int(rect[2]), int(rect[1]) + int(rect[3])), (255, 0, 0), 2)

    # 原图内容mask
    mask = np.zeros(img.shape[:2], dtype=np.uint8)

    # 在roi内识别前景
    bgdmodel = np.zeros((1, 65), np.float64)  # bg模型的临时数组  13 * iterCount
    fgdmodel = np.zeros((1, 65), np.float64)  # fg模型的临时数组  13 * iterCount
    rect = (int(rect[0]), int(rect[1]), int(rect[2]), int(rect[3]))  # 矩形roi，包括前景的矩形，格式为(x,y,w,h)
    cv2.grabCut(gaussian_img, mask, rect, bgdmodel, fgdmodel, 11, mode=cv2.GC_INIT_WITH_RECT)

    # 提取前景和可能的前景区域
    mask_foreground = np.where((mask == 1) + (mask == 3), 255, 0).astype('uint8')
    if vis_result:
        cv2.imshow('mask_foreground', mask_foreground)

    # 过滤调所有背景的
    filter_src = img.copy()
    for i in range(3):
        filter_src[:, :, i] = filter_src[:, :, i] * (mask_foreground > 0).astype(np.uint8)
    if vis_result:
        cv2.imshow('background', filter_src)
        cv2.waitKey(0)

    return filter_src.copy()


# 寻找包裹区域内的标签
def find_label(img, vis_result=False):

    # 图片缩放 + 手动选取目标区域
    src = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    r = cv2.selectROI('input', src, False)  # 返回 (x_min, y_min, w, h)

    # 高斯模糊原图，为前景识别减少背景干扰
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    cv2.dilate(src, se, img)
    gaussian_img = cv2.GaussianBlur(src, (5, 5), 0)
    # cv2.imshow('gaussian_img', gaussian_img)

    # 选取roi区域
    img = gaussian_img.copy()
    cv2.rectangle(img, (int(r[0]), int(r[1])), (int(r[0]) + int(r[2]), int(r[1]) + int(r[3])), (255, 0, 0), 2)

    # 原图内容mask
    mask = np.zeros(src.shape[:2], dtype=np.uint8)

    # 在roi内识别前景
    bgdmodel = np.zeros((1, 65), np.float64)  # bg模型的临时数组  13 * iterCount
    fgdmodel = np.zeros((1, 65), np.float64)  # fg模型的临时数组  13 * iterCount
    rect = (int(r[0]), int(r[1]), int(r[2]), int(r[3]))  # 矩形roi，包括前景的矩形，格式为(x,y,w,h)
    cv2.grabCut(gaussian_img, mask, rect, bgdmodel, fgdmodel, 11, mode=cv2.GC_INIT_WITH_RECT)

    # 提取前景和可能的前景区域
    mask_foreground = np.where((mask == 1) + (mask == 3), 255, 0).astype('uint8')
    if vis_result:
        cv2.imshow('mask_foreground', mask_foreground)

    # 过滤调所有背景的
    filter_src = src.copy()
    for i in range(3):
        filter_src[:, :, i] = filter_src[:, :, i] * (mask_foreground > 0).astype(np.uint8)
    if vis_result:
        cv2.imshow('background', filter_src)
        cv2.waitKey(0)

    return filter_src.copy()



def find_package_label(img, vis_result=False):
    # 包裹签阈值过滤
    # thresholding the image
    ret, thresh = cv2.threshold(img, 190, 229, cv2.THRESH_TOZERO)
    thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)

    # ADDED BINARY THRESHOLD
    ret, edged = cv2.threshold(thresh, 240, 255, cv2.THRESH_BINARY)
    kernal = np.ones((3, 3))
    imgDial = cv2.dilate(edged, kernal, iterations=3)
    imgThre = cv2.erode(imgDial, kernal, iterations=2)
    if vis_result:
        cv2.imshow('thresh', thresh)
        cv2.imshow('edged', edged)
        cv2.imshow('imgThre', imgThre)
        cv2.waitKey(0)


    # ---------------------------
    # 图片轮廓
    minArea = 100
    filter = 4
    contours, hiearchy = cv2.findContours(imgThre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    finalContours = []
    for i in contours:
        # 计算轮廓的面积
        area = cv2.contourArea(i)
        if area > minArea:
            # 计算轮廓的周长
            peri = cv2.arcLength(i, True)
            # 多边形逼近
            # approxPolyDP主要功能是把一个连续光滑曲线折线化，对图像轮廓点进行多边形拟合
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            # 矩形边框
            # boundingRect主要功能是用一个最小的矩形，把找到的形状包起来。还有一个带旋转的矩形，面积会更小
            bbox = cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) == filter:
                    finalContours.append([len(approx), area, approx, bbox, i])
            else:
                finalContours.append([len(approx), area, approx, bbox, i])


    length = finalContours[0][0]#len(finalContours[0][0])
    points = []
    for i in range(len(finalContours[0][2])):
        img = cv2.circle(img, finalContours[0][2][i][0], 2, (0,255,0), 3)
        img = cv2.putText(img, str(i), finalContours[0][2][i][0], cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 3)
        points.append(finalContours[0][2][i][0])

    # 显示图片
    print(points)
    if vis_result:
        cv2.imshow('line', img)
        cv2.waitKey()

    return points


