import sys
from os import path
from pathlib import Path

import cv2
import numpy as np
import pyqtgraph as pg
from imagehash import average_hash
from PIL import Image
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QHBoxLayout, QWidget

# CAPTURE = cv2.VideoCapture(path.join(Path.home(), "Downloads", "sample.mp4"))
CAPTURE = cv2.VideoCapture(0)
FPS = CAPTURE.get(cv2.CAP_PROP_FPS)

if not CAPTURE.isOpened():
    raise IOError("Cannot open webcam")


class MainWindow(QWidget):
    frameIndex = 0
    imageItem = pg.ImageItem()
    scatterPlotItem = pg.PlotCurveItem()

    hashArr = np.array([])

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Squasher")

        layout = QHBoxLayout(self)

        layout.addWidget(self.getCameraWidget())
        layout.addWidget(self.getHashWidget())

        # Event loop
        timer = QTimer(self)
        timer.timeout.connect(self.__update)
        timer.start(int(1000 / FPS))

    def getHashWidget(self) -> QWidget:
        widget = pg.GraphicsLayoutWidget()
        plotItem = pg.PlotItem()
        plotItem.addItem(self.scatterPlotItem)
        widget.addItem(plotItem)
        return widget

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
        hash = average_hash(Image.fromarray(frame))
        hashInt = int(str(hash), base=16)

        if not ret:
            print("No frame captured")
            sys.exit()

        print(
            f"{self.frameIndex}\t{(self.frameIndex/FPS):.2f}\t{hash}",
            end="\r",
        )

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        self.hashArr = np.append(self.hashArr, hashInt)

        self.imageItem.setImage(frame)
        self.scatterPlotItem.setData(
            x=np.arange(self.frameIndex),
            y=self.hashArr,
        )

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
