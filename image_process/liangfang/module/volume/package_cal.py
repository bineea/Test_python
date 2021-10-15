"""
根据包裹边缘点与标签边缘点计算长度

"""
import cv2
import math
import numpy as np
from module.volume import contourutil


def length_cal(orig_img, points_label, points_package, vis_result=True):
    # 获取图像变换后所需的最大画布（边长）
    l1_1, l1_2 = points_package[0] - points_package[2]
    l2_1, l2_2 = points_package[1] - points_package[3]
    max_l = math.sqrt(max(l1_1 * l1_1 + l1_2 * l1_2, l2_1 * l2_1 + l2_2 * l2_2))

    points_label_ordered = order_point(points_label)               # 对包裹4顶点重新排序
    points_label_dst = target_vertax_point(points_label_ordered)   # 计算包裹目标边缘点，无偏移，用于计算

    print('包裹签透视变换前坐标：', points_label_ordered)
    print('包裹签透视变换后坐标：', points_label_dst)

    # -------- 包裹签所在平面透视变换 ----------
    # 计算变换矩阵
    matrix = cv2.getPerspectiveTransform(
        points_label_ordered.astype(np.float32), points_label_dst.astype(np.float32))
    print('包裹签透视变换矩阵：', matrix)

    # 计算包裹边缘目标顶点
    points_package_dst = cv2.perspectiveTransform(np.array([points_package]).astype(np.float32), matrix)[0]

    # ---------- 计算尺寸变换关系 ------------
    # 由于计算包裹签目标点时，按照与实际像素尺寸1：1进行变换，
    # 因此变换后无需再进行尺寸比例缩放，直接取像素尺寸求平均即可
    length_01_23 = (contourutil.findDis(points_package_dst[0], points_package_dst[1]) +
                    contourutil.findDis(points_package_dst[2], points_package_dst[3])) / 2.0
    length_03_12 = (contourutil.findDis(points_package_dst[0], points_package_dst[3]) +
                    contourutil.findDis(points_package_dst[1], points_package_dst[2])) / 2.0
    print('length 01/23: ', length_01_23)
    print('length 03/12: ', length_03_12)

    # if vis_result:
    #     points_package_dst[:, 0] += max_l
    #     points_package_dst[:, 1] += max_l
    #     matrix2 = cv2.getPerspectiveTransform(
    #         points_package.astype(np.float32), points_package_dst)
    #
    #     # 展示透视变换后的图片
    #     gray_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY)  # 转变为灰度图
    #     perspective_img = cv2.warpPerspective(orig_img, matrix2, (int(3*max_l), int(3*max_l)))
    #     cv2.imshow("perspective_img", perspective_img)
    #     cv2.waitKey(0)

    if vis_result:
        points_label_dst = target_vertax_point(points_label_ordered,  # 计算包裹目标边缘点，有偏移，用于展示
                                               x_offset=max_l, y_offset=max_l)
        matrix = cv2.getPerspectiveTransform(
            points_label_ordered.astype(np.float32), points_label_dst.astype(np.float32))

        # 展示透视变换后的图片
        gray_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY)  # 转变为灰度图
        perspective_img = cv2.warpPerspective(orig_img, matrix, (int(2*max_l), int(2*max_l)))
        #cv2.imshow("perspective_img", perspective_img)
        #cv2.waitKey(0)

    return length_01_23, length_03_12



# 根据标准边长计算映射后的坐标位置
def target_vertax_point(clockwise_point, x_offset=0, y_offset=0,
                        STANDARD_WIDTH=100, STANDARD_HEIGHT = 100):
    # 以宽度为准，计算图像像素的实际边长
    # 计算顶点的宽度(取最大宽度)
    w1 = np.linalg.norm(clockwise_point[0] - clockwise_point[1])
    w2 = np.linalg.norm(clockwise_point[2] - clockwise_point[3])
    w = w1 if w1 > w2 else w2

    # 计算顶点的高度(取最大高度)
    h1 = np.linalg.norm(clockwise_point[1] - clockwise_point[2])
    h2 = np.linalg.norm(clockwise_point[3] - clockwise_point[0])
    h = h1 if h1 > h2 else h2

    # 判断哪一条边为长边
    if h > w:            # 说明此时0-3/1-2为长边
        long_length = STANDARD_HEIGHT  # h
        short_length = STANDARD_WIDTH  # w
        top_left = [0+x_offset, 0+y_offset]
        top_right = [short_length+x_offset, 0+y_offset]
        bottom_right = [short_length+x_offset, long_length+y_offset]
        bottom_left = [0+x_offset, long_length+y_offset]
    else:                # 说明此时0-1/2-3为长边
        long_length = STANDARD_HEIGHT  # w
        short_length = STANDARD_WIDTH  # h
        top_left = [0+x_offset, 0+y_offset]
        top_right = [long_length+x_offset, 0+y_offset]
        bottom_right = [long_length+x_offset, short_length+y_offset]
        bottom_left = [0+x_offset, short_length+y_offset]

    return np.array([top_left, bottom_left, bottom_right, top_right], dtype=np.float32)



# 确定包裹签所在平面四个点
def find_lb_area(lb_points, pk_points, img):
    h, w, _ = img.shape
    mask_img = np.zeros((h, w))
    zero = pk_points[0]
    one = pk_points[1]
    two = pk_points[2]
    three = pk_points[3]
    four = pk_points[4]
    five = pk_points[5]
    six = pk_points[6]
    areas = [[six, five, zero, one],
             [six, one, two, three],
             [six, three, four, five]]

    mask_img = cv2.fillConvexPoly(mask_img, np.array(areas[0]), 1)
    mask_img = cv2.fillConvexPoly(mask_img, np.array(areas[1]), 2)
    mask_img = cv2.fillConvexPoly(mask_img, np.array(areas[2]), 3)

    lb_center_x = int(np.average(np.array(lb_points)[:, 0]))
    lb_center_y = int(np.average(np.array(lb_points)[:, 1]))

    # 根据包裹签中心mask值确定包裹签所在平面的4个点
    if mask_img[lb_center_y, lb_center_x] == 1:
        print('label on area 6-5-0-1')
        return np.array(areas[0])
    elif mask_img[lb_center_y, lb_center_x] == 2:
        print('label on area 6-1-2-3')
        return np.array(areas[1])
    else:
        print('label on area 6-3-4-5')
        return np.array(areas[2])


# 对交点坐标进行排序,只排序4个点
def order_point(points):
    """对交点坐标进行排序
    :param points:
    :return:
    """
    points_array = np.array(points)
    # 对x的大小进行排序
    x_sort = np.argsort(points_array[:, 0])
    # 对y的大小进行排序
    y_sort = np.argsort(points_array[:, 1])
    # 获取最左边的顶点坐标
    left_point = points_array[x_sort[0]]
    # 获取最右边的顶点坐标
    right_point = points_array[x_sort[-1]]
    # 获取最上边的顶点坐标
    top_point = points_array[y_sort[0]]
    # 获取最下边的顶点坐标
    bottom_point = points_array[y_sort[-1]]
    return np.array([left_point, top_point, right_point, bottom_point], dtype=np.float32)
    #return np.array([top_point, right_point, bottom_point, left_point], dtype=np.float32)




