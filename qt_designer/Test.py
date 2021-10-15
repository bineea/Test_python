from Test_take_pic import *


class Drawing(MyWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Drawing, self).__init__(parent)
        self.rect = None

    # 重写绘制函数
    def paintEvent(self, event):
        # 初始化绘图工具
        qp = QPainter()
        # 开始在窗口绘制
        qp.begin(self)
        # 自定义画点方法
        if self.rect:
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

thstop = False
brgFrame = None

# 上面的这个来控制进程结束
def showcamre():
    # 参数0代表系统第一个摄像头,第二就用1 以此类推
    cap = cv2.VideoCapture(0)
    # 设置显示分辨率和FPS ,不设置的话会非常卡
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
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
        demo.setpic(qimg)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = Drawing()
    demo.show()
    # 全屏显示
    # ex.showFullScreen()
    # 使用线程,否则程序卡死
    th = Thread(target=showcamre)
    th.start()
    app.exec_()
    # 退出的时候,结束进程,否则,关不掉进程
    thstop = True
