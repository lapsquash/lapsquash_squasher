import pyqtgraph as pg
from PySide6.QtWidgets import QLabel, QWidget

from squasher_py.helpers.interfaces.widget import Widget
from squasher_py.helpers.state import State


class DataWidget(Widget):
    label: QLabel
    scatterPlotItem = pg.PlotCurveItem()

    def __init__(self, state: State) -> None:
        self.state = state

    def get(self) -> QWidget:
        self.label = QLabel()
        self.label.setStyleSheet(
            """
            font-family: 'UDEV Gothic 35NF';
            """,
        )
        return self.label

    def update(self) -> None:
        __state = self.state
        __FPS = __state.FPS
        __frameIdx = __state.frameIndex
        __hashArr = __state.hashArr

        hash = __hashArr[-1]

        data = f"#{__frameIdx}\t{(__frameIdx/__FPS):.2f}s\t0x{int(hash):016X}\t{int(hash)}"  # noqa
        print(data, end="\r")
        self.label.setText(data)
