import cv2
import numpy as np


# 获取轮廓
def getContours(img, cThr=[100, 100], showCanny=False, minArea=1000, filter=0, draw=False):
    # 图像转为灰度
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 设置高斯模糊（图像，高斯内核大小，标准差）
    # img = cv2.GaussianBlur(src, (blur1, blur2), 0)，其中src是要进行滤波的原图像，（blur1，blur2）是高斯核的大小，blur1和blur2的选取一般是奇数，blur1和blur2的值可以不同。参数0表示标准差取0。
    # 当blur1=blur2=1时，相当于不对原始图像做操作。blur1和blur2越大，图像的模糊程度越大。但不是blur1和blur2越大越好，blur1和blur2太大，不仅会滤除噪音，还会平滑掉图像中有用的信息。所以blur的选取要进行测试。
    # 如果要进行滤波的图像的长宽比大致为1:1，那么选取blur时，一般设置blur1=blur2。
    # 如果要进行滤波的图像的长宽比大致为m: n，那么选取blur时，blur1: blur2 = m:n。
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    # 设置边缘检测（图像，最小阈值，最大阈值）
    imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1])

    # 设置图像膨胀、腐蚀内核大小
    kernal = np.ones((5, 5))
    # cv2.dilate(img, kernel, iteration)，其中img是要进行膨胀操作的目标图片，kernel是进行操作的内核，iterations是迭代次数
    # 输入图像用特定结构元素进行膨胀操作，该结构元素确定膨胀操作过程中的邻域的形状，各点像素值将被替换为对应邻域上的最大值
    # 膨胀操作原理：存在一个kernel，在图像上进行从左到右，从上到下的平移，如果方框中存在白色，那么这个方框内所有的颜色都是白色
    imgDial = cv2.dilate(imgCanny, kernal, iterations=3)
    # cv2.erode(src, kernel, iteration)，其中img是要进行腐蚀操作的目标图片，kernel是进行操作的内核，iterations是迭代次数
    # 腐蚀操作原理：存在一个kernel，比如(3, 3)，在图像中不断的平移，在这个9方框中，哪一种颜色所占的比重大，9个方格中将都是这种颜色
    imgThre = cv2.erode(imgDial, kernal, iterations=2)

    # 显示图像
    if showCanny: cv2.imshow('Canny', imgCanny)

    # 检测轮廓
    # cv2.RETR_EXTERNAL：表示只检测外轮廓
    # cv2.RETR_LIST：检测的轮廓不建立等级关系
    # cv2.RETR_CCOMP：建立两个等级的轮廓，上面的一层为外边界，里面的一层为内孔的边界信息。如果内孔内还有一个连通物体，这个物体的边界也在顶层。
    # cv2.RETR_TREE：建立一个等级树结构的轮廓。
    #
    # cv2.CHAIN_APPROX_NONE：存储所有的轮廓点，相邻的两个点的像素位置差不超过1，即max（abs（x1 - x2），abs（y2 - y1）） == 1
    # cv2.CHAIN_APPROX_SIMPLE：压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标，例如一个矩形轮廓只需4个点来保存轮廓信息
    # cv2.CHAIN_APPROX_TC89_L1，CV_CHAIN_APPROX_TC89_KCOS：使用teh - Chinlchain近似算法
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

    finalContours = sorted(finalContours, key=lambda x: x[1], reverse=True)

    if draw:
        for con in finalContours:
            # 绘制轮廓
            cv2.drawContours(img, con[4], -1, (0, 0, 255), 3)

    return img, finalContours

# 获取矩形轮廓的顶点
#     ^
#     |    (a)*-------*(b)
#     |      /       /
#     |  (c)*-------*(d)
#------------------------------->
#     |
# 简单示意：a，b，c，d为四边形的顶点，每个顶点由（x,y）二维坐标表示；则 x+y 值最大的为b；x+y值最小的为c，y-x值最大的为a，y-x值最小的为d
def recorder(myPoints):
    # 构造一个矩阵myPointsNew，其维度与矩阵myPoints一致，并为其初始化为全0
    myPointsNew = np.zeros_like(myPoints)
    # reshape改变矩阵结构，并且原始数据不发生变化
    print('原始myPoint:' + str(myPoints))
    myPoints = myPoints.reshape((4, 2))
    print("处理myPoints：" + str(myPoints))
    # 二维数组myPoints，代码myPoints.sum(axis=0)指定对数组myPoints对每列求和，myPoints.sum(axis=1)是对每行求和，返回的都是一维数组（维度降了一维）
    # axis=0：在第一维操作
    # axis=1：在第二维操作
    # axis=-1：在最后一维操作
    # x = [[a11,a12,a13,a14],[a21,a22,a23,a24],[a31,a32,a33,a34],[a41,a42,a43,a44]]
    # axis=0: out[x] = a(i+1)x + a(i)x
    # axis=1: out[x] = ax(i+1) + ax(i)
    # y = [[[a111,a112],[a121,a122]],[[a211,a212],[a221,a222]],[[a311,a312],[a321,a322]]]
    # axis=2: out[x] = axy(i+1) + axy(i)
    add = myPoints.sum(1)
    print("add:"+str(add))
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    # axis=0：在第一维操作
    # axis=1：在第二维操作
    # axis=-1：在最后一维操作
    # axis=i：在第i维操作
    # x = [[a11,a12,a13,a14],[a21,a22,a23,a24],[a31,a32,a33,a34],[a41,a42,a43,a44]]
    # axis=0: out[x] = a(i+1)x - a(i)x
    # axis=1: out[x] = ax(i+1) - ax(i)
    # y = [[[a111,a112],[a121,a122]],[[a211,a212],[a221,a222]],[[a311,a312],[a321,a322]]]
    # axis=2: out[x] = axy(i+1) - axy(i)
    diff = np.diff(myPoints, axis=1)
    print("diff:"+str(diff))
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]

    return myPointsNew


#
def warpImg(img, pionts, w, h, pad=20):
    pionts = recorder(pionts)
    print("pionts:"+str(pionts))
    pts1 = np.float32(pionts)
    print("pts1:"+str(pts1))
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    # 透视变换是将成像投影到一个新的视平面(Viewing Plane)，也称作投影映射(Projective Mapping)。通过透视变换ABC变换到A'B'C'
    # cv2.getPerspectiveTransform(src, dst) → retval
    # src：源图像中待测矩形的四点坐标
    # sdt：目标图像中矩形的四点坐标
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    # 逆透视变换
    # cv2.warpPerspective(src, M, dsize[, dst[, flags[, borderMode[, borderValue]]]]) → dst
    # src：输入图像;
    # M：变换矩阵;
    # dsize：目标图像shape;
    # flags：插值方式，interpolation方法INTER_LINEAR或INTER_NEAREST;
    # borderMode：边界补偿方式，BORDER_CONSTANT or BORDER_REPLICATE;
    # borderValue：边界补偿大小，常值，默认为0
    imgWarp = cv2.warpPerspective(img, matrix, (w, h))

    # 填充
    # shape读取矩阵结构信息
    imgWarp = imgWarp[pad: imgWarp.shape[0] - pad, pad: imgWarp.shape[1] - pad]

    return imgWarp

# 通过勾股定理计算边长
# a**2 + b**2 = c**2
def findDis(pts1, pts2):
    return ((pts2[0] - pts1[0]) ** 2 + (pts2[1] - pts1[1]) ** 2) ** 0.5
