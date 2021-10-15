import cv2
import math
import numpy as np
import contourutil
import find_target
import package_cal


def img_show(window_name, img, need_close_window=True):
    # 展示图片(展示后关闭)
    cv2.imshow(window_name, img)
    if need_close_window:
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def cal_area_process_lb(img, rect, vis_result=False):
    # -------------- 包裹区域定位 -------------------
    filter_src = find_target.find_package(img, rect, vis_result)
    #cv2.imwrite('filter_src.jpg', filter_src)


    # ------------ 包裹区域内标签定位 ----------------
    #img = cv2.imread('filter_src.jpg')
    label_points = find_target.find_package_label(filter_src)
    print('包裹签边缘点：',  label_points)

    # ------------ 包裹区域角点签定位 ----------------
    # 获得图像边缘和6个角点
    filter_src, package_points = contourutil.get_package_Contours(filter_src, cThr=[50, 50], showCanny=False,
                                                                  minArea=1000, filter=6, draw=False)
    # 重新排序6个顶点
    package_points = contourutil.point_reorder(package_points)
    if True:#vis_result:
        kp_img1 = img.copy()
        keyPoints = cv2.KeyPoint_convert(package_points)
        kp_img1= cv2.drawKeypoints(kp_img1, keyPoints, None, color=(0, 0, 255))
        for i in range(len(package_points)):
            kp_img1 = cv2.putText(kp_img1, str(i), package_points[i], cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)
        img = kp_img1.copy()
        if vis_result:
            cv2.imshow('package_6_points', kp_img1)
            cv2.waitKey(0)

    # 根据上述6个角点计算第七个点
    o = contourutil.computeO(package_points)
    package_points.append(np.array(o))
    print(package_points)

    if vis_result:
        kp_img2 = img.copy()
        keyPoints = cv2.KeyPoint_convert(package_points)
        kp_img2 = cv2.drawKeypoints(kp_img2, keyPoints, None, color=(0, 0, 255))
        for i in range(len(package_points)):
            kp_img2 = cv2.putText(kp_img2, str(i), package_points[i], cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)

        cv2.imshow('package_7_points', kp_img2)
        cv2.waitKey(0)

    # 确定包裹签所在平面的4个点
    package_lb_points = package_cal.find_lb_area(label_points, package_points, img)

    # 计算包裹签所在面的边长
    length_01_23, length_03_12 = package_cal.length_cal(img, label_points, package_lb_points)
    pos_center_23 = (package_lb_points[2] + package_lb_points[3])/2
    pos_center_12 = (package_lb_points[1] + package_lb_points[2])/2
    kp_img3 = img.copy()
    kp_img3 = cv2.putText(kp_img3, str(int(length_01_23)), pos_center_23.astype(np.uint32),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
    kp_img3 = cv2.putText(kp_img3, str(int(length_03_12)), pos_center_12.astype(np.uint32),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    kp_img3 = cv2.line(kp_img3, package_lb_points[2].astype(np.uint32),
                        package_lb_points[3].astype(np.uint32), (255, 0, 0), 3)
    kp_img3 = cv2.line(kp_img3, package_lb_points[2].astype(np.uint32),
                        package_lb_points[1].astype(np.uint32), (255, 0, 0), 3)

    if vis_result:
        cv2.imshow('package_length', kp_img3)
        cv2.waitKey(0)

    return kp_img3, length_03_12, length_01_23, "边长分别为："+str(int(length_03_12))+", "+str(int(length_01_23))





def cal_area_process_wo_lb(img, rect, real_line_v, real_line_h, vis_result=False):

    # -------------- 包裹区域定位 -------------------
    #filter_src = cv2.imread('filter_src2.jpg')
    # filter_src = cv2.erode(filter_src, np.ones((5, 5)), iterations=3)
    # filter_src = cv2.GaussianBlur(filter_src, (5, 5), 1)
    filter_src = find_target.find_package(img, rect, vis_result=0)
    # cv2.imwrite('filter_src2.jpg', filter_src)


    # ------------ 包裹区域角点签定位 ----------------
    # 获得图像边缘和6个角点
    filter_src, package_points = contourutil.get_package_Contours(filter_src, cThr=[50, 50], showCanny=False,
                                                                  minArea=2000, filter=6, draw=False)
    # 重新排序6个顶点
    package_points = contourutil.point_reorder(package_points)

    # 判断当前面是否为左右两面
    pt0, pt1, pt2 = package_points[0], package_points[1], package_points[-1]
    is_lr_mode = False
    THRESH = 50
    if abs(pt2[1] - pt0[1]) > THRESH and abs(pt1[1] - pt0[1]) >= THRESH:
        is_lr_mode = True
    elif abs(pt2[1] - pt0[1]) > THRESH and abs(pt1[1] - pt0[1]) <= THRESH:
        # 说明此时0号顶点在右侧，需要后移一位
        package_points = [pt for pt in package_points[1:]]
        package_points.append(pt0)
    elif abs(pt2[1] - pt0[1]) < THRESH and abs(pt1[1] - pt0[1]) >= THRESH:
        # 说明此时0号顶点在左侧，不需要后移
        print('no need to move')
    else:
        return img, None, str('请调正拍摄角度')

    # 判断拍摄角度是否足够正
    THRESH_PARREL = 60    # 两条平行线间差距最大阈值，理性情况下对应平行线差值应当为0
    if is_lr_mode:
        #12、03、45为平行线
        if contourutil.findDis(package_points[0], package_points[1]) > THRESH_PARREL or \
            contourutil.findDis(package_points[0], package_points[1]) > THRESH_PARREL :
            return img, None, str('请调正拍摄角度')
        else:
            # demo图暂时无法满足此场景，未开发
            return img, None, str('请旋转拍摄角度')

    else:
        #05、14、23为平行线
        if abs(contourutil.findDis(package_points[0], package_points[1]) -
               contourutil.findDis(package_points[4], package_points[5])) > THRESH_PARREL :
            return img, None, str('请调正拍摄角度')
        else:
            pt_top = (package_points[0] + package_points[5]) / 2.0
            pt_mid = (package_points[1] + package_points[4]) / 2.0
            pt_btm = (package_points[2] + package_points[3]) / 2.0
            print('看看是不是垂直共线了~~ ', pt_top, pt_mid, pt_btm)

            l1 = contourutil.findDis(pt_top, pt_mid)
            l2 = contourutil.findDis(pt_mid, pt_btm)

            # 边长计算关键步骤
            # step 1 根据pt[1]-pt[4]成像长度，计算缩放比例
            scale_rate = real_line_h / contourutil.findDis(package_points[1], package_points[4])
            l1 *= scale_rate
            l2 *= scale_rate

            l_out = real_line_v * l2 / math.sqrt(real_line_v * real_line_v - l1 * l1)
            print('另一条边长：', l_out)

            # 计算包裹签所在面的边长
            pos_center_45 = (package_points[4] + package_points[5]) / 2
            pos_center_14 = (package_points[1] + package_points[4]) / 2
            pos_center_34 = (package_points[3] + package_points[4]) / 2   # new cal
            kp_img3 = img.copy()
            kp_img3 = cv2.putText(kp_img3, str(int(real_line_h)), pos_center_14.astype(np.uint32),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            kp_img3 = cv2.putText(kp_img3, str(int(real_line_v)), pos_center_45.astype(np.uint32),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            kp_img3 = cv2.putText(kp_img3, str(int(l_out)), pos_center_34.astype(np.uint32),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            kp_img3 = cv2.line(kp_img3, package_points[1].astype(np.uint32),
                               package_points[4].astype(np.uint32), (255, 0, 0), 3)
            kp_img3 = cv2.line(kp_img3, package_points[4].astype(np.uint32),
                               package_points[5].astype(np.uint32), (255, 0, 0), 3)
            kp_img3 = cv2.line(kp_img3, package_points[3].astype(np.uint32),
                               package_points[4].astype(np.uint32), (0, 0, 255), 3)

            keyPoints = cv2.KeyPoint_convert(package_points)
            kp_img3 = cv2.drawKeypoints(kp_img3, keyPoints, None, color=(0, 0, 255))
            for i in range(len(package_points)):
                kp_img3 = cv2.putText(kp_img3, str(i), package_points[i], cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)

            if vis_result:
                cv2.imshow('package_length', kp_img3)
                cv2.waitKey(0)

            return kp_img3, l_out, '边长'+str(int(l_out))

