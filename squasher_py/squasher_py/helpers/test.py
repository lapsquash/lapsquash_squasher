import sys

import cv2
import pyqtgraph as pg
from PyQt6 import QtWidgets
from PyQt6.QtCore import QTimer

app = QtWidgets.QApplication(sys.argv)
# ウィンドウ作成
window = pg.GraphicsLayoutWidget()


image = pg.ImageItem()
capture = cv2.VideoCapture(0)
_, data = capture.read()

fps = 60


def update():
    global image
    _, frame = capture.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    image.setImage(frame)


timer = QTimer()
timer.timeout.connect(update)
timer.start(int(1 / fps * 1000))

if __name__ == "__main__":
    # 画像オブジェクト作成 & 画像をセット
    image.setImage(data)
    # 画像を格納するボックス作成 & 画像オブジェクトをセット
    view_box = pg.ViewBox()
    view_box.addItem(image)
    view_box.setAspectLocked(True)
    # プロットオブジェクト作成 & 上で作成したview_boxをセット
    plot = pg.PlotItem(viewBox=view_box)
    # ウィンドウにplotを追加
    window.addItem(plot)
    # ウィンドウ表示
    window.show()
    # プログラム終了
    sys.exit(app.exec())
