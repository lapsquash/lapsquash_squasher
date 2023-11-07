import pyqtgraph as pg
from PySide6.QtWidgets import QLabel, QWidget

from squasher_core.helpers.interfaces.widget import Widget
from squasher_core.helpers.state import State


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

        cRangeStr = ""

        # < 1s のときの表示
        if len(__slopeArr) == 0:
            self.label.setText("__")
            return

        # for cRange in __clippingRangeArr:
        #     cRangeStr += f"{cRange.start} - {cRange.end}\n"

        hash = __hashArr[-1]
        self.label.setText(
            f"""
{__FPS:.2f} FPS
#{__frameIdx}\t{(__frameIdx/__FPS):.2f}s
0x{int(hash):016X} = {int(hash)!s}
         __slopeArr[-1]: 0x{int(__slopeArr[-1]):016X}
__slopeThresholdArr[-1]: 0x{int(__slopeThresholdArr[-1]):016X}
               needTrim: {__slopeArr[-1] > __slopeThresholdArr[-1]}
clipping range:
{cRangeStr}
            """
        )
