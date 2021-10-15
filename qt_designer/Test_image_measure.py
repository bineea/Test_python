import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ImageMeasure import *


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        # 添加登录按钮信号和槽。注意display函数不加小括号()
        self.pushButton.clicked.connect(self.display)
    def display(self):
        # 利用line Edit控件对象text()函数获取界面输入
        name = self.lineEdit.text()
        # 利用text Browser控件对象setText()函数设置界面显示
        self.textBrowser.setText("名称是: " + name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())