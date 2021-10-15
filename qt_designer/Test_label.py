import sys
import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Label(QLabel):
    def __init__(self):
        super().__init__()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        path = 'D:\\project\python\\Test_python\\resource\\test.png'
        image = QImage(path)
        qp.drawImage(QPoint(), image)
        #
        # pen = QPen(Qt.red)
        # pen.setWidth(2)
        # qp.setPen(pen)
        #
        # font = QFont()
        # font.setFamily('Times')
        # font.setBold(True)
        # font.setPointSize(24)
        # qp.setFont(font)

        qp.drawText(150, 250, "Hello World !")

        qp.end()


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 660, 620)
        self.setWindowTitle("Add a text on image")

        self.label = Label()

        self.grid = QGridLayout()
        self.grid.addWidget(self.label)
        self.setLayout(self.grid)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())