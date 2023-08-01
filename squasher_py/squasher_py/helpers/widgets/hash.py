import numpy as np
import pyqtgraph as pg
from imagehash import average_hash
from PIL import Image
from PySide6.QtWidgets import QWidget

from squasher_py.helpers.interfaces.widget import Widget
from squasher_py.helpers.state import State


class HashWidget(Widget):
    widePlotItem: pg.PlotItem
    wideScatterPlotItem = pg.PlotCurveItem()

    narrowPlotItem: pg.PlotItem
    narrowScatterPlotItem = pg.PlotCurveItem()

    def __init__(self, state: State) -> None:
        self.state = state

    def get(self) -> QWidget:
        widget = pg.GraphicsLayoutWidget()
        self.widePlotItem = pg.PlotItem()
        self.narrowPlotItem = pg.PlotItem()

        self.widePlotItem.addItem(self.wideScatterPlotItem)

        self.narrowPlotItem.addItem(self.narrowScatterPlotItem)

        # config
        self.widePlotItem.showGrid(x=True, y=True)
        self.widePlotItem.setTitle("Hash")
        self.widePlotItem.setLabel("left", "Hash")
        self.widePlotItem.setLabel("bottom", "Frame")
        self.widePlotItem.setMouseEnabled(x=True, y=True)
        self.widePlotItem.setYRange(0, 0xFFFFFFFFFFFFFFFF)
        # self.widePlotItem.sigXRangeChanged.connect(
        #     lambda: self.__onXRangeChanged(),
        # )

        self.narrowPlotItem.showGrid(x=True, y=True)
        self.narrowPlotItem.setTitle("Hash")
        self.narrowPlotItem.setLabel("left", "Hash")
        self.narrowPlotItem.setLabel("bottom", "Frame")
        self.narrowPlotItem.setMouseEnabled(x=True, y=True)
        self.narrowPlotItem.setYRange(0, 0xFFFFFFFFFFFFFFFF)

        widget.addItem(self.widePlotItem, 0, 0)
        widget.addItem(self.narrowPlotItem, 0, 1)
        return widget

    # def __onRegionChanged(self) -> None:
    #     self.narrowPlotItem.setXRange(
    #         *self.wideLineRegionItem.getRegion(),
    #         padding=0,
    #     )
    #     self.narrowPlotItem.setYRange(0, 2**64)

    # def __onXRangeChanged(self) -> None:
    #     viewBox = self.narrowPlotItem.getViewBox()
    #     if viewBox is None:
    #         return
    #     self.wideLineRegionItem.setRegion(viewBox.viewRange()[0])
    #     self.narrowPlotItem.setYRange(0, 0xFFFFFFFFFFFFFFFF)

    def update(self) -> None:
        __state = self.state
        __frameBuff = __state.frameBuff
        __frameIdx = __state.frameIndex
        __hashArr = __state.hashArr

        hash = average_hash(Image.fromarray(__frameBuff))
        hashInt = int(str(hash), base=16)

        self.state.hashArr = np.append(self.state.hashArr, hashInt)

        self.wideScatterPlotItem.setData(
            x=np.arange(__frameIdx - 1),  # なぜか -1
            y=__hashArr,
        )

        self.narrowScatterPlotItem.setData(
            x=np.arange(__frameIdx - 1)[-50:],  # なぜか -1
            y=__hashArr[-50:],
        )
