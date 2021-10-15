
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MyLabel(QLabel):
    def __init__(self, centralwidget):
        super(MyLabel, self).__init__(centralwidget)
        self.backgroundImg = None
        self.startX = None
        self.startY = None
        self.rectWidth = None
        self.rectHeight = None

    def paintEvent(self, e):
        # print("执行paintEvent")
        qp = QPainter()
        qp.begin(self)

        if not (self.backgroundImg is None):
            qp.drawImage(QPoint(), self.backgroundImg)

        # 自定义画点方法
        if isinstance(self.rect, tuple):
            self.drawRect(qp)
        # 结束在窗口的绘制
        qp.end()

    def drawRect(self, qp):
        # 创建红色，宽度为4像素的画笔
        pen = QPen(Qt.red, 4)
        qp.setPen(pen)
        qp.drawRect(*self.rect)

    # 重写三个时间处理
    def mousePressEvent(self, event):
        # print("mouse press")
        self.rect = (event.x(), event.y(), 0, 0)

    # def mouseReleaseEvent(self, event):
    # print("mouse release")

    def mouseMoveEvent(self, event):
        self.startX, self.startY = self.rect[0:2]
        self.rectWidth = event.x() - self.startX
        self.rectHeight = event.y() - self.startY
        self.rect = (self.startX, self.startY, self.rectWidth, self.rectHeight)
        self.update()

    def setBackgroundImg(self, img):
        # print("set backgroundimg")
        self.backgroundImg = img
        self.update()