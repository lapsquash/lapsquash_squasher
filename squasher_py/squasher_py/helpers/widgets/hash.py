import numpy as np
import pyqtgraph as pg
from imagehash import average_hash
from PIL import Image
from PySide6.QtWidgets import QWidget

from squasher_py.helpers.interfaces.widget import Widget
from squasher_py.helpers.state import State


class HashWidget(Widget):
    scatterPlotItem = pg.PlotCurveItem()
    hashArr = np.array([], dtype=np.uint64)

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
        _frameBuff = self.state.frameBuff

        if len(_frameBuff) == 0:
            raise ValueError("Frame buffer is empty")

        hash = average_hash(Image.fromarray(_frameBuff))
        hashInt = int(str(hash), base=16)

        self.hashArr = np.append(self.hashArr, hashInt)
        self.scatterPlotItem.setData(
            x=np.arange(self.state.frameIndex)[-100:],
            y=(self.hashArr)[-100:],
        )
