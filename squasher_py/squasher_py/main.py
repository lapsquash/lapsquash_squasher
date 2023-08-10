import sys

import cv2
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget

from squasher_py.helpers.state import State
from squasher_py.helpers.widgets.camera import CameraWidget
from squasher_py.helpers.widgets.data import DataWidget
from squasher_py.helpers.widgets.hash import HashWidget
from squasher_py.model.capture import CaptureModel
from squasher_py.model.hash import HashModel
from squasher_py.model.log import LogModel
from squasher_py.model.output import OutputModel


class MainWindow(QWidget):
    def __init__(self, state: State) -> None:
        super().__init__()
        self.state = state

        self.__defineModelOrWidget()
        self.__defineLayout()
        self.__defineEventLoop()

    def __defineModelOrWidget(self) -> None:
        # Model の初期化
        self.captureModel = CaptureModel(self.state)
        self.logModel = LogModel(self.state)
        self.hashModel = HashModel(self.state)
        self.outputModel = OutputModel(self.state)

        # Widget の初期化
        self.hashWidget = HashWidget(self.state)
        self.cameraWidget = CameraWidget(self.state)
        self.dataWidget = DataWidget(self.state)

    def __defineLayout(self) -> None:
        # Window の設定
        self.setWindowTitle("Squasher")
        self.setStyleSheet("background-color: #000")

        cameraWidget = self.cameraWidget.get()
        dataWidget = self.dataWidget.get()
        hashWidget = self.hashWidget.get()

        # レイアウトの設定
        hLayout = QHBoxLayout(self)
        left = QVBoxLayout()
        right = QVBoxLayout()

        left.addWidget(
            cameraWidget,
            stretch=2,
        )
        left.addWidget(
            dataWidget,
            stretch=3,
            alignment=Qt.AlignmentFlag.AlignTop,
        )

        right.addWidget(hashWidget)

        hLayout.addLayout(left, 1)
        hLayout.addLayout(right, 2)

    def __defineEventLoop(self) -> None:
        timer = QTimer(self)

        # SHOULD: `timer.timeout.connect` のときは lambda を使う
        # ref: https://qiita.com/Kanahiro/items/8075546b2fea0b6baf5d
        timer.timeout.connect(lambda: self.__update())

        timer.start(int(1000 / self.state.FPS))

    def __update(self) -> None:
        """イベントループ"""
        try:
            # MUST: capture は必ず最初
            self.captureModel.update()
            self.hashModel.update()
            self.outputModel.update()
            self.logModel.update()

            # TODO: Widget のレンダーはマルチスレッドにしても良いかもしれない
            self.cameraWidget.update()
            self.hashWidget.update()
            self.dataWidget.update()

        except Exception as e:
            raise e

        if cv2.waitKey(1) & 0xFF == ord("q"):
            sys.exit()
        return

    def __del__(self) -> None:
        print("\ndispose")
        del self.captureModel
        del self.hashModel
        del self.outputModel
        del self.logModel


if __name__ == "__main__":
    state = State()

    app = QApplication()
    win = MainWindow(state)
    win.show()

    app.exec()

    del win
    sys.exit()
