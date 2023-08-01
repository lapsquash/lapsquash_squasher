from dataclasses import dataclass
from typing import Tuple

import cv2
import numpy as np


@dataclass
class StateData:
    CAPTURE: cv2.VideoCapture
    FPS: float
    frameIndex: int
    """
    frameBuff =
      [
        [
          [ 20  13   5]
          [ 21  14   6]
          [ 34  22   8]
          ...
          [100 100  98]
          [128 133 131]
          [147 152 150]
        ]
          ...
      ]
    """
    frameBuff: np.ndarray[Tuple[int, int, int], np.dtype[np.uint8]]
    hashArr: np.ndarray[int, np.dtype[np.uint64]]


class State(StateData):
    def __init__(self):
        self.frameIndex: int = 0
        self.frameBuff = np.array([], dtype=np.uint8)
        self.hashArr = np.array([], dtype=np.uint64)
