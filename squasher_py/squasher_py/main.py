import sys

import cv2
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget

from squasher_py.helpers.state import State
from squasher_py.helpers.widgets.camera import CameraWidget
from squasher_py.helpers.widgets.data import DataWidget
from squasher_py.helpers.widgets.hash import HashWidget
from squasher_py.model.camera import CaptureModel
from squasher_py.model.hash import HashModel
from squasher_py.model.log import LogModel


class MainWindow(QWidget):
    def __init__(self, state: State) -> None:
        super().__init__()
        self.state = state

        self.__defineModelOrWidget()
        self.__defineLayout()
        self.__defineEventLoop()

    def __defineModelOrWidget(self) -> None:
        # Instantiate models
        self.captureModel = CaptureModel(self.state)
        self.logModel = LogModel(self.state)
        self.hashModel = HashModel(self.state)

        # Instantiate widgets
        self.hashWidget = HashWidget(self.state)
        self.cameraWidget = CameraWidget(self.state)
        self.dataWidget = DataWidget(self.state)

    def __defineLayout(self) -> None:
        # Set config for window
        self.setWindowTitle("Squasher")

        # Set layout
        hLayout = QHBoxLayout(self)

        vLayout = QVBoxLayout()
        vLayout.addWidget(self.cameraWidget.get())
        vLayout.addWidget(self.dataWidget.get())

        hLayout.addLayout(vLayout)
        hLayout.addWidget(self.hashWidget.get())

    def __defineEventLoop(self) -> None:
        # Event loop
        timer = QTimer(self)
        # SHOULD use lambda when using timer.timeout.connect
        # ref: https://qiita.com/Kanahiro/items/8075546b2fea0b6baf5d
        timer.timeout.connect(lambda: self.__update())
        timer.start(int(1000 / self.state.FPS))

    def __update(self) -> None:
        # This method is called every frame
        try:
            self.captureModel.update()
            self.hashModel.update()
            self.logModel.update()
            self.cameraWidget.update()
            self.hashWidget.update()
            self.dataWidget.update()

        except Exception as e:
            raise e

        if cv2.waitKey(1) & 0xFF == ord("q"):
            sys.exit()
        pass

    def __del__(self) -> None:
        print("\ndispose")
        del self.captureModel
        del self.logModel
        del self.hashModel


if __name__ == "__main__":
    state = State()

    app = QApplication()
    win = MainWindow(state)
    win.show()

    app.exec()

    # dispose
    del win
    sys.exit()
