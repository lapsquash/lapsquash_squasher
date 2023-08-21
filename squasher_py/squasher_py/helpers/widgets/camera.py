import cv2
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget

import squasher_py.model.utils.types.cv2 as tcv2
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
        camera.addItem(self.imageItem)  # type: ignore
        camera.setAspectLocked(True)
        widget.addItem(pg.PlotItem(viewBox=camera))  # type: ignore
        return widget

    def update(self) -> None:
        state = self.state
        __frameBuff = state.frameBuff

        # BGR -> RGB
        __frameBuff = tcv2.cvtColor(__frameBuff, cv2.COLOR_BGR2RGB)
        __frameBuff = tcv2.rotate(__frameBuff, cv2.ROTATE_90_CLOCKWISE)

        self.imageItem.setImage(__frameBuff)  # type: ignore
