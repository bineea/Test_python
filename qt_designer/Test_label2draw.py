import sys
import cv2
from label2draw import *


class Label2Draw(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Label2Draw, self).__init__()
        self.setupUi(self)

        # path = 'D:\\project\python\\Test_python\\resource\\20210829140835.jpg'
        # img = cv2.imread(path)
        # qimg = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        # self.label.setPixmap(QPixmap.fromImage(qimg))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Label2Draw()
    ex.show()
    sys.exit(app.exec_())