from dataclasses import dataclass
from os import path
from pathlib import Path

import cv2
import numpy as np


@dataclass
class StateData:
    CAPTURE: cv2.VideoCapture
    FPS: float
    frameIndex: int
    frameBuff: np.ndarray
    hashArr: np.ndarray


class State(StateData):
    def __init__(self):
        # self.CAPTURE = cv2.VideoCapture(0)
        self.CAPTURE = cv2.VideoCapture(
            path.join(Path.home(), "Downloads", "sample.mp4")
        )
        self.FPS = self.CAPTURE.get(cv2.CAP_PROP_FPS)

        if not self.CAPTURE.isOpened():
            raise IOError("Cannot open")

        self.frameIndex: int = 0
        self.frameBuff = np.array([], dtype=np.uint64)
        self.hashArr = np.array([], dtype=np.uint64)

    def __del__(self):
        print("Releasing capture")
        self.CAPTURE.release()
