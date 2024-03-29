# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'label2draw.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import cv2

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Label(QLabel):
    def __init__(self, centralwidget):
        super(Label,self).__init__(centralwidget)

    def paintEvent(self, e):
        print("执行paintEvent")
        qp = QPainter()
        qp.begin(self)

        path = 'D:\\project\python\\Test_python\\resource\\20210829140835.jpg'
        image = QImage(path)
        qp.drawImage(QPoint(), image)

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
        print("mouse press")
        self.rect = (event.x(), event.y(), 0, 0)

    def mouseReleaseEvent(self, event):
        print("mouse release")

    def mouseMoveEvent(self, event):
        start_x, start_y = self.rect[0:2]
        self.rect = (start_x, start_y, event.x() - start_x, event.y() - start_y)
        self.update()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = Label(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 581, 271))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
