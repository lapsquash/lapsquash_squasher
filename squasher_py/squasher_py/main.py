import sys

import cv2
import pyqtgraph as pg
from PyQt6.QtCore import QTimer

CAPTURE = cv2.VideoCapture(0)
FPS = CAPTURE.get(cv2.CAP_PROP_FPS)

frame_index = 0
image_item = pg.ImageItem()


def update():
    global image_item, frame_index
    frame_index += 1
    _, frame = CAPTURE.read()
    print(f"{frame_index}\t{(frame_index/FPS):.2f}", end="\r")
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    image_item.setImage(frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        sys.exit()
    pass


def get_widget_camera():
    camera = pg.ViewBox()
    camera.addItem(image_item)
    camera.setAspectLocked(True)
    return pg.PlotItem(viewBox=camera)


def get_win():
    win = pg.GraphicsLayoutWidget()

    win.addItem(get_widget_camera())

    return win


if __name__ == "__main__":
    app = pg.mkQApp()
    win = get_win()

    timer = QTimer()
    timer.timeout.connect(update)
    timer.start()

    win.show()
    app.exec()

    CAPTURE.release()
    sys.exit()
