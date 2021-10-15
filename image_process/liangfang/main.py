import copy
import os
import sys
import cv2
import numpy
import requests

from module.volume import cal_area
from module.weight import weighting
from ui.ui_window import *
from threading import *


#控制是否关闭线程
threadstop = False

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.brgFrame = None

        self.lengthResult = None
        self.widthResult = None
        self.lengthAndWidthResultPic = None
        self.heightResult = None
        self.heightResultPic = None
        self.volumeResult = None
        self.weightResult = None
        self.weightResultPic = None

        # 添加登录按钮信号和槽。注意display函数不加小括号()
        self.camera_button.clicked.connect(self.controlCamera)
        self.volume_download_button_1.clicked.connect(lambda:self.getUploadPic("first.jpg", "http://storage.jd.local/cloud-print/weighingSquare1.jpg"))
        self.volume_button_1.clicked.connect(self.getVolumeInfo1)
        self.volume_download_button_2.clicked.connect(lambda:self.getUploadPic("second.jpg", "http://storage.jd.local/cloud-print/weighingSquare2.jpg"))
        self.volume_button_2.clicked.connect(self.getVolumeInfo2)
        self.weight_download_button.clicked.connect(lambda:self.getUploadPic("third.jpg", "http://storage.jd.local/cloud-print/weighingSquare3.jpg"))
        self.weight_button.clicked.connect(self.getWeightInfo)

        self.volume_local_button_1.clicked.connect(self.getLocalFileInfo)
        self.volume_local_button_2.clicked.connect(self.getLocalFileInfo)
        self.weight_local_button.clicked.connect(self.getLocalFileInfo)


    def setpic(self, brgFrame, img):
        # 通过graphicsView无法显示摄像头图片，不知道怎么调整
        # pix = QPixmap.fromImage(img)
        # item = QGraphicsPixmapItem(pix)
        # item.setScale(1)
        # scene = QGraphicsScene()
        # scene.addItem(item)
        # self.graphicsView.setScene(scene)

        # 图片显示
        # self.pixmap = QPixmap.fromImage(img)
        # self.label.setPixmap(QPixmap.fromImage(img))

        # 图片显示
        self.brgFrame = brgFrame
        self.camera_label.setBackgroundImg(img)

    def getVolumeInfo1(self):

        # 长度、宽度计算
        self.lengthAndWidthResultPic, self.lengthResult, self.widthResult, errorMsg = cal_area.cal_area_process_lb(self.brgFrame,
                                                                                                                   (self.camera_label.startX, self.camera_label.startY, self.camera_label.rectWidth, self.camera_label.rectHeight))

        self.lengthResult = round(self.lengthResult, 3)
        self.widthResult = round(self.widthResult, 3)

        # resize处理返回图片的大小
        lengthAndWidthScale = min(numpy.float32(self.volume_label_1.width() / self.lengthAndWidthResultPic.shape[1]),
                    numpy.float32(self.volume_label_1.height() / self.lengthAndWidthResultPic.shape[0]))
        self.lengthAndWidthResultPic = cv2.resize(self.lengthAndWidthResultPic, (0, 0), None, lengthAndWidthScale, lengthAndWidthScale)

        # 图片显示
        lengthAndWidthResultimg = QImage(self.lengthAndWidthResultPic.data, self.lengthAndWidthResultPic.shape[1], self.lengthAndWidthResultPic.shape[0], self.lengthAndWidthResultPic.shape[1]*3, QImage.Format_RGB888)
        self.volume_label_1.setPixmap(QPixmap.fromImage(lengthAndWidthResultimg))

        # 长度、宽度显示
        if self.lengthAndWidthResultPic is None or self.lengthResult is None or self.widthResult is None :
            self.volume_text_browser.setText("提示：" + str(errorMsg))
        else:
            self.volume_text_browser.setText("长："+str(self.lengthResult)
                                         +"\n宽："+str(self.widthResult))

    def getVolumeInfo2(self):
        # 高度计算
        self.heightResultPic, self.heightResult, errorMsg = cal_area.cal_area_process_wo_lb(self.brgFrame,
                                                                                            (self.camera_label.startX, self.camera_label.startY, self.camera_label.rectWidth, self.camera_label.rectHeight),
                                                                                            self.widthResult,
                                                                                            self.lengthResult)
        self.heightResult = round(self.heightResult, 3)

        # resize处理返回图片的大小
        heightScale = min(numpy.float32(self.volume_label_2.width() / self.heightResultPic.shape[1]),
                    numpy.float32(self.volume_label_2.height() / self.heightResultPic.shape[0]))
        self.heightResultPic = cv2.resize(self.heightResultPic, (0, 0), None, heightScale, heightScale)

        # 图片显示
        heightResultimg = QImage(self.heightResultPic.data, self.heightResultPic.shape[1], self.heightResultPic.shape[0], self.heightResultPic.shape[1]*3, QImage.Format_RGB888)
        self.volume_label_2.setPixmap(QPixmap.fromImage(heightResultimg))

        # 高度显示
        if self.heightResultPic is None or self.heightResult is None:
            self.volume_text_browser.setText("提示：" + str(errorMsg))
        else:
            self.getVolumeInfo()

    def getWeightInfo(self):
        self.weightResult = None

        weightingFrame = copy.copy(self.brgFrame)
        weightingFrame = weightingFrame[self.camera_label.startY: self.camera_label.startY+self.camera_label.rectHeight,
                         self.camera_label.startX: self.camera_label.startX+self.camera_label.rectWidth, :]

        # 计算重量
        self.weightResult,self.weightResultPic = weighting.digitalrec(weightingFrame)

        # resize处理返回图片的大小
        self.weightResultPic = cv2.resize(self.weightResultPic, (0, 0), None,
                                          numpy.float32(self.weight_label.width() / self.weightResultPic.shape[1]),
                                          numpy.float32(self.weight_label.height() / self.weightResultPic.shape[0]))

        # 图片显示
        weightResultimg = QImage(self.weightResultPic.data, self.weightResultPic.shape[1], self.weightResultPic.shape[0], self.weightResultPic.shape[1]*3, QImage.Format_RGB888)
        self.weight_label.setPixmap(QPixmap.fromImage(weightResultimg))

        # 重量显示
        self.weight_text_browser.setText("重量："+str(self.weightResult))

    def getVolumeInfo(self):
        self.volumeResult = self.lengthResult * self.widthResult * self.heightResult
        self.volumeResult = round(self.volumeResult, 3)
        self.volume_text_browser.setText("长："+str(self.lengthResult)
                                         +"\n宽："+str(self.widthResult)
                                         +"\n高："+str(self.heightResult)
                                         +"\n体积："+str(self.volumeResult))

    def getUploadPic(self, fileName, imgUrlPath):
        fileAbsPath = os.path.join(os.path.dirname(os.path.abspath("__file__")), fileName);
        req = requests.get(imgUrlPath)
        with open(fileAbsPath, "wb") as uploadFile:
            uploadFile.write(req.content)
        uploadBrgFrame = cv2.imread(fileAbsPath)
        downScale = min(numpy.float32(self.camera_label.width() / uploadBrgFrame.shape[1]),
                          numpy.float32(self.camera_label.height() / uploadBrgFrame.shape[0]))
        uploadBrgFrame = cv2.resize(uploadBrgFrame, (0, 0), None, downScale, downScale)
        uploadBrgFrame = cv2.cvtColor(uploadBrgFrame, cv2.COLOR_RGB2BGR)
        uploadQimg = QImage(uploadBrgFrame.data, uploadBrgFrame.shape[1], uploadBrgFrame.shape[0], uploadBrgFrame.shape[1]*3, QImage.Format_RGB888)
        self.setpic(uploadBrgFrame, uploadQimg)

    def controlCamera(self):
        global threadstop
        threadstop = not threadstop


    def getLocalFileInfo(self):
        fileLocalPath = self.file_path_lineEdit.text()
        localBrgFrame = cv2.imread(fileLocalPath)
        localScale = min(numpy.float32(self.camera_label.width() / localBrgFrame.shape[1]),
                        numpy.float32(self.camera_label.height() / localBrgFrame.shape[0]))
        localBrgFrame = cv2.resize(localBrgFrame, (0, 0), None, localScale, localScale)
        localBrgFrame = cv2.cvtColor(localBrgFrame, cv2.COLOR_RGB2BGR)
        localQimg = QImage(localBrgFrame.data, localBrgFrame.shape[1], localBrgFrame.shape[0],
                            localBrgFrame.shape[1] * 3, QImage.Format_RGB888)
        self.setpic(localBrgFrame, localQimg)

# 上面的这个来控制进程结束
def showcamera():
    # 参数0代表系统第一个摄像头,第二就用1 以此类推
    cap = cv2.VideoCapture(0)
    # 设置显示分辨率和FPS ,不设置的话会非常卡
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 520)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 450)
    cap.set(cv2.CAP_PROP_FPS, 20)
    while cap.isOpened():
        if threadstop:
            continue
        ret, frame = cap.read()
        if not ret:
            continue

        # path = 'D:\\project\python\\Test_python\\resource\\second.jpg'
        # frame = cv2.imread(path)

        # 图片大小缩放
        scale = min(numpy.float32(myWin.camera_label.width() / frame.shape[1]),
                        numpy.float32(myWin.camera_label.height() / frame.shape[0]))
        scale = round(scale,2)
        frame = cv2.resize(frame, (0, 0), None, scale, scale)

        # frame = cv2.resize(frame, (0, 0), None, 0.35, 0.35)
        # cv2.imshow("test", frame)
        # cv2.waitKey(0)

        # 水平翻转,很有必要
        # frame = cv2.flip(frame, 1)
        # opencv 默认图像格式是rgb qimage要使用BRG,这里进行格式转换,不用这个的话,图像就变色了,困扰了半天,翻了一堆资料
        brgFrame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # mat-->qimage
        qimg = QImage(brgFrame.data, brgFrame.shape[1], brgFrame.shape[0], brgFrame.shape[1]*3, QImage.Format_RGB888)
        myWin.setpic(brgFrame, qimg)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = MyWindow()
    myWin.show()
    # 全屏显示
    # myWin.showFullScreen()
    # 使用线程,否则程序卡死
    th = Thread(target=showcamera)
    th.start()
    app.exec_()
    # 退出的时候,结束进程,否则,关不掉进程
    threadstop = True
