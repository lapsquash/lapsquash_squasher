# type: ignore

import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget

from squasher_py.helpers.interfaces.widget import Widget
from squasher_py.helpers.state import State


def getWidePlotItem() -> pg.PlotItem:
    plotItem = pg.PlotItem()

    plotItem.showGrid(x=True, y=True)
    plotItem.setTitle("Hash")
    plotItem.setLabel("left", "hash")
    plotItem.setLabel("bottom", "frame")
    plotItem.setMouseEnabled(x=True, y=True)
    plotItem.setYRange(0, 2**64)

    return plotItem


def getNarrowPlotItem() -> pg.PlotItem:
    plotItem = pg.PlotItem()

    plotItem.showGrid(x=True, y=True)
    plotItem.setTitle("Hash (last 50fr)")
    plotItem.setLabel("left", "hash")
    plotItem.setLabel("bottom", "frame")
    plotItem.setMouseEnabled(x=True, y=True)
    plotItem.setYRange(0, 2**64)

    return plotItem


def getWideSlopePlotItem() -> pg.PlotItem:
    plotItem = pg.PlotItem()

    plotItem.showGrid(x=True, y=True)
    plotItem.setTitle("Hash slope")
    plotItem.setLabel("left", "slope")
    plotItem.setLabel("bottom", "second")
    plotItem.setMouseEnabled(x=True, y=True)

    return plotItem


def getNarrowSlopePlotItem() -> pg.PlotItem:
    plotItem = pg.PlotItem()

    plotItem.showGrid(x=True, y=True)
    plotItem.setTitle("Hash slope (last 50s)")
    plotItem.setLabel("left", "slope")
    plotItem.setLabel("bottom", "second")
    plotItem.setMouseEnabled(x=True, y=True)

    return plotItem


class HashWidget(Widget):
    wideScatterPlotItem = pg.PlotCurveItem()
    narrowScatterPlotItem = pg.PlotCurveItem()
    wideSlopeScatterPlotItem = pg.ScatterPlotItem()
    sideSlopeThresholdPlotItem = pg.PlotCurveItem()
    narrowSlopeScatterPlotItem = pg.ScatterPlotItem()
    narrowSlopeThresholdPlotItem = pg.PlotCurveItem()

    def __init__(self, state: State) -> None:
        self.state = state

    def get(self) -> QWidget:
        widget = pg.GraphicsLayoutWidget()
        widePlotItem = getWidePlotItem()
        narrowPlotItem = getNarrowPlotItem()
        wideSlopePlotItem = getWideSlopePlotItem()
        narrowSlopePlotItem = getNarrowSlopePlotItem()

        widePlotItem.addItem(self.wideScatterPlotItem)
        narrowPlotItem.addItem(self.narrowScatterPlotItem)
        wideSlopePlotItem.addItem(self.wideSlopeScatterPlotItem)
        wideSlopePlotItem.addItem(self.sideSlopeThresholdPlotItem)
        narrowSlopePlotItem.addItem(self.narrowSlopeScatterPlotItem)
        narrowSlopePlotItem.addItem(self.narrowSlopeThresholdPlotItem)

        widget.addItem(widePlotItem, 0, 0)
        widget.addItem(narrowPlotItem, 0, 1)
        widget.addItem(wideSlopePlotItem, 1, 0)
        widget.addItem(narrowSlopePlotItem, 1, 1)

        widget.ci.layout.setColumnStretchFactor(0, 1)
        widget.ci.layout.setColumnStretchFactor(1, 1)

        return widget

    def update(self) -> None:
        state = self.state
        __frameIdx = state.frameIndex
        __hashArr = state.hashArr
        __FPS = state.FPS
        __slopeArr = state.slopeArr
        __slopeThresholdArr = state.slopeThresholdArr

        secRange = np.arange(int(__frameIdx / int(__FPS)))

        self.wideScatterPlotItem.setData(
            x=np.arange(__frameIdx),
            y=__hashArr,
        )

        self.narrowScatterPlotItem.setData(
            x=np.arange(__frameIdx)[-50:],
            y=__hashArr[-50:],
        )

        self.wideSlopeScatterPlotItem.setData(
            x=secRange,
            y=__slopeArr,
            symbol="x",
            pen="y",
        )

        self.sideSlopeThresholdPlotItem.setData(
            x=secRange,
            y=__slopeThresholdArr,
            pen="r",
        )

        self.narrowSlopeScatterPlotItem.setData(
            x=secRange[-50:],
            y=__slopeArr[-50:],
            symbol="x",
            pen="y",
        )

        self.narrowSlopeThresholdPlotItem.setData(
            x=secRange[-50:],
            y=__slopeThresholdArr[-50:],
            pen="r",
        )
