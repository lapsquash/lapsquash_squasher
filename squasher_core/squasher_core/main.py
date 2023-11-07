import sys

import cv2
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget

from squasher_core.helpers.interfaces.model import Model
from squasher_core.helpers.interfaces.widget import Widget
from squasher_core.helpers.state import State
from squasher_core.helpers.widgets.camera import CameraWidget
from squasher_core.helpers.widgets.data import DataWidget
from squasher_core.helpers.widgets.hash import HashWidget
from squasher_core.model.capture import CaptureModel
from squasher_core.model.hash import HashModel
from squasher_core.model.log import LogModel
from squasher_core.model.output import OutputModel


class MainWindow(QWidget):
    def __init__(self, state: State) -> None:
        super().__init__()
        self.state = state

        self.__defineModelOrWidget()
        self.__defineLayout()
        self.__defineEventLoop()

    def __defineModelOrWidget(self) -> None:
        # Model の初期化
        self.models: list[Model] = [
            # MUST: capture は必ず最初
            CaptureModel(self.state),
            HashModel(self.state),
            LogModel(self.state),
            OutputModel(self.state),
        ]

        # Widget の初期化
        self.widgets: list[Widget] = [
            CameraWidget(self.state),
            DataWidget(self.state),
            HashWidget(self.state),
        ]

    def __defineLayout(self) -> None:
        # Window の設定
        self.setWindowTitle("Squasher")
        self.setStyleSheet("background-color: #000")

        cameraWidget = self.widgets[0].get()
        dataWidget = self.widgets[1].get()
        hashWidget = self.widgets[2].get()

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

        # timer.start(int(1000 / self.state.FPS))
        timer.start(0)

    def __update(self) -> None:
        """イベントループ"""
        try:
            for model in self.models:
                model.update()

            # TODO: Widget のレンダーはマルチスレッドにしても良いかもしれない
            for widget in self.widgets:
                widget.update()

        except Exception as e:
            raise e

        if cv2.waitKey(1) & 0xFF == ord("q"):
            sys.exit()

    def __del__(self) -> None:
        print("\ndispose")
        for model in self.models:
            del model


if __name__ == "__main__":
    state = State()

    app = QApplication()
    win = MainWindow(state)
    win.show()

    app.exec()

    del win
    sys.exit()
