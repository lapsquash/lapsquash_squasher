import sys
from os import path
from pathlib import Path

import cv2
import pyqtgraph as pg
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

CAPTURE = cv2.VideoCapture(path.join(Path.home(), "Downloads", "sample.mp4"))
# CAPTURE = cv2.VideoCapture(0)
FPS = CAPTURE.get(cv2.CAP_PROP_FPS)

if not CAPTURE.isOpened():
    raise IOError("Cannot open webcam")


class MainWindow(QWidget):
    frameIndex = 0
    imageItem = pg.ImageItem()

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Squasher")

        QVBoxLayout(self).addWidget(self.getCameraWidget())

        # Event loop
        timer = QTimer(self)
        timer.timeout.connect(self.__update)
        timer.start(int(1000 / FPS))

    def getCameraWidget(self) -> QWidget:
        widget = pg.GraphicsLayoutWidget()
        camera = pg.ViewBox()
        camera.addItem(self.imageItem)
        camera.setAspectLocked(True)
        widget.addItem(pg.PlotItem(viewBox=camera))
        return widget

    def __update(self) -> None:
        self.frameIndex += 1
        ret, frame = CAPTURE.read()

        if not ret:
            print("No frame captured")
            sys.exit()

        print(
            f"{self.frameIndex}\t{(self.frameIndex/FPS):.2f}\t{FPS}",
            end="\r",
        )
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        self.imageItem.setImage(frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            sys.exit()
        pass


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()

    app.exec()

    # dispose
    CAPTURE.release()
    sys.exit()
