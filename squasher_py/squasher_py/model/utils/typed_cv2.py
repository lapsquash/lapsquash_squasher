# type: ignore

import cv2
from cv2 import VideoCapture

from squasher_py.helpers.state import TypeFrame


def cvtColor(src: TypeFrame, code: int) -> TypeFrame:
    return cv2.cvtColor(src, code)


def rotate(src: TypeFrame, rotateCode: int) -> TypeFrame:
    return cv2.rotate(src, rotateCode)


def readNextFrame(capture: VideoCapture) -> tuple[bool, TypeFrame]:
    return capture.read()


def hconcat(src: list[TypeFrame]) -> TypeFrame:
    return cv2.hconcat(src)


def vconcat(src: list[TypeFrame]) -> TypeFrame:
    return cv2.vconcat(src)


def imwrite(path: str, img: TypeFrame) -> bool:
    return cv2.imwrite(path, img)
