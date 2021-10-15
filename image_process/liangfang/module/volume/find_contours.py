import cv2
import contourutil


def img_show(window_name, img, need_close_window=True):
    # 展示图片(展示后关闭)
    cv2.imshow(window_name, img)
    if need_close_window:
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    '''
    img = cv2.imread("D:\\luojiaqi\\LA-General\\HackerMarathon\\Pics_or_videos\\contours_test.jpg")
    img, app = getContours(img)

    img_show('img', img)
    '''

    # 设置是否打开摄像机
    webcam = False

    # 定义使用图片路径（绝对路径或相对路径）
    # path = 'D://Project//Python//Test_python//resource//example_object_measurement.jpg'
    # path = 'D:/Project/Python/Test_python/resource/example_object_measurement.jpg'
    path = 'D:\\luojiaqi\\LA-General\\HackerMarathon\\Pics_or_videos\\contours_test.jpg'
    # 定义相机对象，并设置使用的相机ID
    cap = cv2.VideoCapture(0)

    # 设置宽度、高度
    cap.set(10, 160)
    cap.set(3, 1920)
    cap.set(4, 1080)

    scale = 2

    width_paper = 210 * scale
    heigh_paper = 290 * scale

    while True:
        # 判断是否开启摄像
        if webcam:
            success, img = cap.read()
        else:
            img = cv2.imread(path)

        # 找到A4纸的轮廓
        imgContours0, contours0 = contourutil.getContours(img,
                                                          showCanny=False,
                                                          minArea=50000,
                                                          filter=4,
                                                          draw=True)

        if len(contours0) != 0:
            # 按A4纸轮廓进行变换
            biggest = contours0[0][2]
            imgWarp = contourutil.warpImg(img, biggest, width_paper, heigh_paper)

            # 获得图像边缘和6个角点
            imgContours1, contours1 = contourutil.getContours(imgWarp,
                                                              cThr=[50, 50],
                                                              showCanny=False,
                                                              minArea=2000,
                                                              filter=6,
                                                              draw=True)


            '''
            if len(contours0) != 0 :
                for obj in contours1 :
                    cv2.polylines(imgContours1,[obj[2]],True,(0,255,0),2)
                    nPoints = contourutil.recorder(obj[2])   # 这里需要改，先找到4个点再找边
                    width = round(contourutil.findDis(nPoints[0][0]//scale,nPoints[1][0]//scale)/10)
                    heigh = round(contourutil.findDis(nPoints[0][0]//scale,nPoints[2][0]//scale)/10)
                    cv2.arrowedLine(imgContours1, (nPoints[0][0][0], nPoints[0][0][1]),
                                    (nPoints[1][0][0], nPoints[1][0][1]),
                                    (255, 0, 255), 3, 8, 0, 0.05)
                    cv2.arrowedLine(imgContours1, (nPoints[0][0][0], nPoints[0][0][1]),
                                    (nPoints[2][0][0], nPoints[2][0][1]),
                                    (255, 0, 255), 3, 8, 0, 0.05)
                    x, y, w, h = obj[3]
                    cv2.putText(imgContours1, '{}cm'.format(width), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                                (255, 0, 255), 2)
                    cv2.putText(imgContours1, '{}cm'.format(heigh), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                                (255, 0, 255), 2)
            cv2.imshow('A4',imgContours1)
            '''

        # 调整图像的大小
        img = cv2.resize(img, (0, 0), None, 0.25, 0.25)

        # 显示图像
        cv2.imshow('Original', img)
        cv2.waitKey(1)



