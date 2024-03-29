from datetime import datetime
from os import path

import squasher_core

__now = datetime.now(tz=datetime.now().astimezone().tzinfo)
__now_str = __now.strftime("%Y-%m-%d_%H-%M-%S")

OUTPUT_DIR = path.join(
    path.dirname(squasher_core.__file__),
    "..",
    "..",
    "out",
)

LOG_DIR = path.join(OUTPUT_DIR, "logs")
LOG_PATH = path.join(LOG_DIR, f"{__now_str}.log")

OUTPUT_SPLIT_DIR = path.join(OUTPUT_DIR, "splits")
OUTPUT_TILES_DIR = path.join(OUTPUT_DIR, "tiles")
OUTPUT_MANIFEST_PATH = path.join(OUTPUT_DIR, "manifest.json")


def getOutputSplitPath(idx: int) -> str:
    return path.join(OUTPUT_SPLIT_DIR, f"{idx}.mp4")


# CAPTURE_RESOURCE: int | str = path.join(
#     Path.home(),
#     "Downloads",
#     "_videoplayback.mp4",
# )
CAPTURE_RESOURCE: int | str = 0
CAPTURE_SCALE_FACTOR: float = 0.5
CAPTURE_FPS: int = 30

SLOPE_THRESHOLD_MIN: int = 2**20
SLOPE_THRESHOLD_MAX: int = 2**60
CLIP_RANGE_MIN_SECOND: int = 3
