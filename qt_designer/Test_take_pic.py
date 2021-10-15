import sys
import cv2
from TakePic import *
from threading import *

#控制是否关闭线程
thstop = False



class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.brgFrame = None
        self.lengthResult = None
        self.widthResult = None
        self.heightResult = None
        self.volumeResult = None
        self.weightResult = None

        # 添加登录按钮信号和槽。注意display函数不加小括号()
        self.volume_button_1.clicked.connect(self.getVolumeInfo1)
        self.volume_button_2.clicked.connect(self.getVolumeInfo2)
        self.weight_button.clicked.connect(self.getWeightInfo)

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
        # resize处理返回图片的大小
        self.lengthResult = None
        self.widthResult = None
        # TODO 需要根据第二张图片进行数据计算，所以第一张图片不做数据展示，是否也不应该展示第一张图片的处理数据
        # self.volume_text_browser.setText("startX="+str(self.camera_label.startX)
        #                                  +"\nstartY="+str(self.camera_label.startY)
        #                                  +"\nrectWidth="+str(self.camera_label.rectWidth)
        #                                  +"\nrectHeight="+str(self.camera_label.rectHeight))

        print("brgFrame:"+str(self.brgFrame))


    def getVolumeInfo2(self):
        # resize处理返回图片的大小

        print(str(self.volume_label_2.width()))
        print(str(self.volume_label_2.height()))


        self.heightResult = None

        self.volume_text_browser.setText("startX="+str(self.camera_label.startX)
                                         +"\nstartY="+str(self.camera_label.startY)
                                         +"\nrectWidth="+str(self.camera_label.rectWidth)
                                         +"\nrectHeight="+str(self.camera_label.rectHeight))



    def getWeightInfo(self):
        self.weightResult = None
        # resize处理返回图片的大小
        self.weight_text_browser.setText("重量："+str(self.weightResult))


    def getVolumeInfo(self):
        self.volumeResult = self.lengthResult * self.widthResult * self.heightResult
        self.volume_text_browser.setText("长："+str(self.lengthResult)
                                         +"\n宽："+str(self.widthResult)
                                         +"\n高："+str(self.heightResult)
                                         +"\n体积："+str(self.volumeResult))



# 上面的这个来控制进程结束
def showcamera():
    # 参数0代表系统第一个摄像头,第二就用1 以此类推
    cap = cv2.VideoCapture(0)
    # 设置显示分辨率和FPS ,不设置的话会非常卡
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 520)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 450)
    cap.set(cv2.CAP_PROP_FPS, 20)
    while cap.isOpened():
        if thstop:
            return
        ret, frame = cap.read()
        if not ret:
            continue
        # 水平翻转,很有必要
        frame = cv2.flip(frame, 1)
        # opencv 默认图像格式是rgb qimage要使用BRG,这里进行格式转换,不用这个的话,图像就变色了,困扰了半天,翻了一堆资料
        brgFrame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # mat-->qimage
        qimg = QImage(brgFrame.data, brgFrame.shape[1], brgFrame.shape[0], QImage.Format_RGB888)
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
    thstop = True
