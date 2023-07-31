import numpy as np
import pyqtgraph as pg
from imagehash import average_hash
from PIL import Image
from PySide6.QtWidgets import QWidget

from squasher_py.helpers.interfaces.widget import Widget
from squasher_py.helpers.state import State


class HashWidget(Widget):
    scatterPlotItem = pg.PlotCurveItem()

    def __init__(self, state: State) -> None:
        self.state = state

    def get(self) -> QWidget:
        widget = pg.GraphicsLayoutWidget()
        plotItem = pg.PlotItem()
        plotItem.addItem(self.scatterPlotItem)

        # config
        plotItem.showGrid(x=True, y=True)
        plotItem.setTitle("Hash")
        plotItem.setLabel("left", "Hash")
        plotItem.setLabel("bottom", "Frame")
        plotItem.setMouseEnabled(x=True, y=True)
        plotItem.setYRange(0, 0xFFFFFFFFFFFFFFFF)

        widget.addItem(plotItem)
        return widget

    def update(self) -> None:
        __state = self.state
        __frameBuff = __state.frameBuff
        __frameIdx = __state.frameIndex
        __hashArr = __state.hashArr

        hash = average_hash(Image.fromarray(__frameBuff))
        hashInt = int(str(hash), base=16)

        self.state.hashArr = np.append(self.state.hashArr, hashInt)

        self.scatterPlotItem.setData(
            x=np.arange(__frameIdx - 1)[-100:],  # なぜか -1
            y=__hashArr[-100:],
        )
