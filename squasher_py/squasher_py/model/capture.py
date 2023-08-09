import cv2

from squasher_py.helpers.constants import CAPTURE_RESOURCE
from squasher_py.helpers.interfaces.model import Model
from squasher_py.helpers.state import State


class CaptureModel(Model):
    def __init__(self, state: State) -> None:
        super().__init__(state)
        self.state = state

        self.state.CAPTURE = cv2.VideoCapture(CAPTURE_RESOURCE)
        self.state.FPS = self.state.CAPTURE.get(cv2.CAP_PROP_FPS)

        if not self.state.CAPTURE.isOpened():
            raise IOError("Cannot open")

    def update(self) -> None:
        state = self.state
        __CAPTURE = state.CAPTURE

        ret, frame = __CAPTURE.read()  # type: ignore

        if not ret:
            raise RuntimeError("No frame captured")

        self.state.frameIndex += 1
        self.state.frameBuff = frame

    def __del__(self) -> None:
        print("Releasing capture...")
        self.state.CAPTURE.release()
        return
