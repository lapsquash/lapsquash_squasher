from os import path

import cv2
import numpy as np

import squasher_py.model.utils.typed_cv2 as tcv2
from squasher_py.helpers.constants import OUTPUT_SPLIT_DIR, OUTPUT_TILES_DIR
from squasher_py.helpers.state import TypeFrame
from squasher_py.model.log import LogModel

source = path.join(OUTPUT_SPLIT_DIR, "1.mp4")
capture = cv2.VideoCapture(source)

if not capture.isOpened():
    raise RuntimeError("Error opening video stream or file")


def __createTile(frames: list[TypeFrame]) -> TypeFrame:
    width = 10
    tiles: list[TypeFrame] = []
    for i in range(0, len(frames), width):
        tile = np.hstack(frames[i : (i + width)])  # noqa: E203 # FIXME: なぜ？？？
        tiles.append(tile)
    return np.vstack(tiles)


def __saveTiledImg(tiledFrame: TypeFrame) -> None:
    LogModel.prepareDir()
    tcv2.imwrite(
        path.join(OUTPUT_TILES_DIR, "1.jpg"),
        tiledFrame,
    )


def createTiledImg(idx: int) -> None:
    frameIdx: int = 0
    frames: list[TypeFrame] = []

    while True:
        ret, frame = tcv2.readNextFrame(capture)

        if not ret:
            print("Capture end")
            break

        height, width, _ = frame.shape
        frames.append(frame)
        print(f"#{frameIdx}, {width}x{height}", end="\r")

        frameIdx += 1

    print("Creating tiled image...")
    tiledFrame = __createTile(frames)
    __saveTiledImg(tiledFrame)

    return


if __name__ == "__main__":
    createTiledImg(0)
