# type: ignore

import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget

from squasher_py.helpers.interfaces.widget import Widget
from squasher_py.helpers.state import State


class HashWidget(Widget):
    widePlotItem: pg.PlotItem
    wideScatterPlotItem = pg.PlotCurveItem()

    narrowPlotItem: pg.PlotItem
    narrowScatterPlotItem = pg.PlotCurveItem()

    slopePlotItem: pg.PlotCurveItem
    slopeScatterPlotItem = pg.ScatterPlotItem()
    slopeThresholdPlotItem = pg.PlotCurveItem()

    def __init__(self, state: State) -> None:
        self.state = state

    def get(self) -> QWidget:
        widget = pg.GraphicsLayoutWidget()
        self.widePlotItem = pg.PlotItem()
        self.narrowPlotItem = pg.PlotItem()
        self.slopePlotItem = pg.PlotItem()

        self.widePlotItem.addItem(self.wideScatterPlotItem)
        self.narrowPlotItem.addItem(self.narrowScatterPlotItem)
        self.slopePlotItem.addItem(self.slopeScatterPlotItem)
        self.slopePlotItem.addItem(self.slopeThresholdPlotItem)

        # config
        self.widePlotItem.showGrid(x=True, y=True)
        self.widePlotItem.setTitle("Hash")
        self.widePlotItem.setLabel("left", "Hash")
        self.widePlotItem.setLabel("bottom", "Frame")
        self.widePlotItem.setMouseEnabled(x=True, y=True)
        self.widePlotItem.setYRange(0, 0xFFFFFFFFFFFFFFFF)

        self.narrowPlotItem.showGrid(x=True, y=True)
        self.narrowPlotItem.setTitle("Hash")
        self.narrowPlotItem.setLabel("left", "Hash")
        self.narrowPlotItem.setLabel("bottom", "Frame")
        self.narrowPlotItem.setMouseEnabled(x=True, y=True)
        self.narrowPlotItem.setYRange(0, 0xFFFFFFFFFFFFFFFF)

        self.slopePlotItem.showGrid(x=True, y=True)
        self.slopePlotItem.setTitle("hash slope")
        self.slopePlotItem.setLabel("left", "Hash")
        self.slopePlotItem.setLabel("bottom", "Frame")
        self.slopePlotItem.setMouseEnabled(x=True, y=True)

        widget.addItem(self.widePlotItem, 0, 0)
        widget.addItem(self.narrowPlotItem, 0, 1)
        widget.addItem(self.slopePlotItem, 1, 0, 1, 2)
        return widget

    def update(self) -> None:
        __state = self.state
        __frameIdx = __state.frameIndex
        __hashArr = __state.hashArr
        __FPS = __state.FPS
        __slopeArr = __state.slopeArr
        __slopeThresholdArr = __state.slopeThresholdArr

        self.wideScatterPlotItem.setData(
            x=np.arange(__frameIdx),
            y=__hashArr,
        )

        self.narrowScatterPlotItem.setData(
            x=np.arange(__frameIdx)[-50:],
            y=__hashArr[-50:],
        )

        self.slopeScatterPlotItem.setData(
            x=np.arange(int(__frameIdx / int(__FPS))),
            y=__slopeArr,
            symbol="x",
            pen="y",
        )

        self.slopeThresholdPlotItem.setData(
            x=np.arange(int(__frameIdx / int(__FPS))),
            y=__slopeThresholdArr,
            pen="r",
        )
