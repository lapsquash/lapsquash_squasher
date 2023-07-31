import sys

import cv2
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QHBoxLayout, QWidget

from squasher_py.helpers.state import State
from squasher_py.helpers.widgets.camera import CameraWidget
from squasher_py.helpers.widgets.hash import HashWidget


class MainWindow(QWidget):
    def __init__(self, state: State) -> None:
        super().__init__()
        self.state = state

        self.hashWidget = HashWidget(self.state)
        self.cameraWidget = CameraWidget(self.state)

        self.setWindowTitle("Squasher")

        layout = QHBoxLayout(self)

        layout.addWidget(self.cameraWidget.get())
        layout.addWidget(self.hashWidget.get())

        # Event loop
        timer = QTimer(self)
        timer.timeout.connect(self.__update)
        timer.start(int(1000 / self.state.FPS))

    def __update(self) -> None:
        ret, frame = self.state.CAPTURE.read()

        if not ret:
            print("No frame captured")
            sys.exit()

        self.state.frameIndex += 1
        self.state.frameBuff = frame

        self.hashWidget.update()
        self.cameraWidget.update()

        if cv2.waitKey(1) & 0xFF == ord("q"):
            sys.exit()
        pass


if __name__ == "__main__":
    state = State()

    app = QApplication()
    win = MainWindow(state)
    win.show()

    app.exec()

    # dispose
    # FIXME: 絶対呼ばれている気がしない
    del state
    sys.exit()
