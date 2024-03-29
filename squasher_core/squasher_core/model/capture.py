import cv2

import squasher_core.model.utils.types.cv2 as tcv2
from squasher_core.helpers.constants import (
    CAPTURE_FPS,
    CAPTURE_RESOURCE,
    CAPTURE_SCALE_FACTOR,
)
from squasher_core.helpers.interfaces.model import Model
from squasher_core.helpers.state import State


class CaptureModel(Model):
    def __init__(self, state: State) -> None:
        super().__init__(state)
        self.state = state

        self.state.CAPTURE = cv2.VideoCapture(CAPTURE_RESOURCE)

        _height = self.state.CAPTURE.get(cv2.CAP_PROP_FRAME_HEIGHT)
        _width = self.state.CAPTURE.get(cv2.CAP_PROP_FRAME_WIDTH)
        _fps = self.state.CAPTURE.get(cv2.CAP_PROP_FPS)

        self.state.CAPTURE.set(
            cv2.CAP_PROP_FRAME_HEIGHT, _height * CAPTURE_SCALE_FACTOR
        )
        self.state.CAPTURE.set(cv2.CAP_PROP_FRAME_WIDTH, _width * CAPTURE_SCALE_FACTOR)
        self.state.CAPTURE.set(cv2.CAP_PROP_FPS, CAPTURE_FPS)

        self.state.FPS = self.state.CAPTURE.get(cv2.CAP_PROP_FPS)

        if not self.state.CAPTURE.isOpened():
            raise OSError("Cannot open")

    def update(self) -> None:
        state = self.state
        __CAPTURE = state.CAPTURE

        ret, frame = tcv2.readNextFrame(__CAPTURE)

        if not ret:
            raise RuntimeError("No frame captured")

        self.state.frameIndex += 1
        self.state.frameBuff = frame

    def __del__(self) -> None:
        print("Releasing capture...")
        self.state.CAPTURE.release()
