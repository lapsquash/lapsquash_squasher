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
        _frameBuff = self.state.frameBuff

        print(
            f"{self.state.frameIndex}\t{(self.state.frameIndex/self.state.FPS):.2f}",  # noqa
            end="\r",
        )

        # BGR -> RGB
        _frameBuff = cv2.cvtColor(_frameBuff, cv2.COLOR_BGR2RGB)
        _frameBuff = cv2.rotate(_frameBuff, cv2.ROTATE_90_CLOCKWISE)

        self.imageItem.setImage(_frameBuff)
