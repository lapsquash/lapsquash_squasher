import sys

import cv2
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget

from squasher_py.helpers.state import State
from squasher_py.helpers.widgets.camera import CameraWidget
from squasher_py.helpers.widgets.data import DataWidget
from squasher_py.helpers.widgets.hash import HashWidget
from squasher_py.model.log import LogModel


class MainWindow(QWidget):
    def __init__(self, state: State) -> None:
        super().__init__()
        self.state = state

        self.hashWidget = HashWidget(self.state)
        self.cameraWidget = CameraWidget(self.state)
        self.dataWidget = DataWidget(self.state)
        self.logModel = LogModel(self.state)

        self.setWindowTitle("Squasher")

        layout = QVBoxLayout(self)
        layout.addWidget(self.cameraWidget.get())
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.hashWidget.get())
        layout.addLayout(hLayout)
        layout.addWidget(self.dataWidget.get())

        # Event loop
        timer = QTimer(self)

        # SHOULD use lambda when using timer.timeout.connect
        # ref: https://qiita.com/Kanahiro/items/8075546b2fea0b6baf5d
        timer.timeout.connect(lambda: self.__update())
        timer.start(int(1000 / self.state.FPS))

    def __update(self) -> None:
        __state = self.state
        __CAPTURE = __state.CAPTURE

        ret, frame = __CAPTURE.read()

        if not ret:
            print("No frame captured")
            sys.exit()

        self.state.frameIndex += 1
        self.state.frameBuff = frame

        try:
            self.cameraWidget.update()
            self.hashWidget.update()
            self.dataWidget.update()
            self.logModel.update()
        except Exception as e:
            print(e)
            sys.exit()

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
