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
            color: #fff;
            """,
        )
        return self.label

    def update(self) -> None:
        state = self.state
        __FPS = state.FPS
        __frameIdx = state.frameIndex
        __hashArr = state.hashArr
        __slopeArr = state.slopeArr
        __slopeThresholdArr = state.slopeThresholdArr

        # slop init (< 1s)
        if len(__slopeArr) == 0:
            self.label.setText("__\n\n\n")
            return

        hash = __hashArr[-1]
        self.label.setText(
            f"""
{__FPS:.2f} FPS
#{__frameIdx}\t{(__frameIdx/__FPS):.2f}s
0x{int(hash):016X} = {str(int(hash))}
         __slopeArr[-1]: 0x{int(__slopeArr[-1]):016X}
__slopeThresholdArr[-1]: 0x{int(__slopeThresholdArr[-1]):016X}
               needTrim: {__slopeArr[-1] > __slopeThresholdArr[-1]}
            """
        )
