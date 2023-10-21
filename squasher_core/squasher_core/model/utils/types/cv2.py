# type: ignore

from typing import Callable

import cv2
from cv2 import VideoCapture

from squasher_core.helpers.state import TypeFrame

cvtColor: Callable[[TypeFrame, int], TypeFrame] = cv2.cvtColor

rotate: Callable[[TypeFrame, int], TypeFrame] = cv2.rotate


def readNextFrame(capture: VideoCapture) -> tuple[bool, TypeFrame]:
    return capture.read()


hconcat: Callable[[list[TypeFrame]], TypeFrame] = cv2.hconcat
vconcat: Callable[list[TypeFrame], TypeFrame] = cv2.vconcat
imwrite: Callable[[str, TypeFrame], bool] = cv2.imwrite
