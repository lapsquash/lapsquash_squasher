# type: ignore

import cv2
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget

from squasher_py.helpers.interfaces.widget import Widget
from squasher_py.helpers.state import State


class CameraWidget(Widget):
    def __init__(self, state: State) -> None:
        self.state = state

    scatterPlotItem = pg.PlotCurveItem()
    imageItem = pg.ImageItem()

    def get(self) -> QWidget:
        widget = pg.GraphicsLayoutWidget()
        camera = pg.ViewBox()
        camera.addItem(self.imageItem)
        camera.setAspectLocked(True)
        widget.addItem(pg.PlotItem(viewBox=camera))
        return widget

    def update(self) -> None:
        __state = self.state
        __frameBuff = __state.frameBuff

        # BGR -> RGB
        __frameBuff = cv2.cvtColor(__frameBuff, cv2.COLOR_BGR2RGB)
        __frameBuff = cv2.rotate(__frameBuff, cv2.ROTATE_90_CLOCKWISE)

        self.imageItem.setImage(__frameBuff)
