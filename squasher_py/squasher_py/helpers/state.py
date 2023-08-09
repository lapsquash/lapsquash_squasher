from dataclasses import dataclass
from typing import Tuple

import cv2
import numpy as np

TypeFrame = Tuple[int, int, int]  # RGB
TypeHash = int
TypeSlope = float
TypeSlopeThreshold = float

TypeFrameBuff = np.ndarray[TypeFrame, np.dtype[np.uint8]]
TypeHashArr = np.ndarray[TypeHash, np.dtype[np.uint64]]
TypeSlopeArr = np.ndarray[TypeSlope, np.dtype[np.float64]]
TypeSlopeThresholdArr = np.ndarray[TypeSlopeThreshold, np.dtype[np.float64]]


@dataclass
class StateData:
    CAPTURE: cv2.VideoCapture
    FPS: float
    frameIndex: int
    """
    frameBuff =
      [
        [
        #   R   G   B
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
    frameBuff: TypeFrameBuff
    hashArr: TypeHashArr
    slopeArr: TypeSlopeArr
    slopeThresholdArr: TypeSlopeThresholdArr


class State(StateData):
    def __init__(self):
        self.frameIndex: int = 0
        self.frameBuff = np.array([], dtype=np.uint8)
        self.hashArr = np.array([], dtype=np.uint64)
        self.slopeArr = np.array([], dtype=np.float64)
        self.slopeThresholdArr = np.array([], dtype=np.float64)
