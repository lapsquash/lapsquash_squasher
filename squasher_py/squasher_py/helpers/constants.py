from datetime import datetime
from os import path
from pathlib import Path

import squasher_py

__now = datetime.now()
__now_str = __now.strftime("%Y-%m-%d_%H-%M-%S")

OUTPUT_DIR = path.join(path.dirname(squasher_py.__file__), "..", "out")
LOG_DIR = path.join(OUTPUT_DIR, "logs")
LOG_PATH = path.join(LOG_DIR, f"{__now_str}.log")

OUTPUT_SPLIT_DIR = path.join(OUTPUT_DIR, "splits")


def getOutputSplitPath(idx: int):
    return path.join(OUTPUT_SPLIT_DIR, f"{idx}.mp4")


CAPTURE_RESOURCE: int | str = path.join(
    Path.home(),
    "Downloads",
    "videoplayback.mp4",
)
# CAPTURE_RESOURCE: int | str = 0

SLOPE_THRESHOLD_MIN = 2**20
SLOPE_THRESHOLD_MAX = 2**60
