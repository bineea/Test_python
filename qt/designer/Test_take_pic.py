import sys
import cv2
from TakePic import *
from threading import *


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

    def setpic(self, img):
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
        self.label.setBackgroundImg(img)


thstop = False
brgFrame = None


# 上面的这个来控制进程结束
def showcamre():
    # 参数0代表系统第一个摄像头,第二就用1 以此类推
    cap = cv2.VideoCapture(0)
    # 设置显示分辨率和FPS ,不设置的话会非常卡
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
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
        myWin.setpic(qimg)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = MyWindow()
    myWin.show()
    # 全屏显示
    # myWin.showFullScreen()
    # 使用线程,否则程序卡死
    th = Thread(target=showcamre)
    th.start()
    app.exec_()
    # 退出的时候,结束进程,否则,关不掉进程
    thstop = True
