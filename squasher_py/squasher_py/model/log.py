import json
from os import makedirs, path

from squasher_py.helpers.constants import (
    LOG_DIR,
    LOG_PATH,
    OUTPUT_DIR,
    OUTPUT_SPLIT_DIR,
    OUTPUT_TILES_DIR,
)
from squasher_py.helpers.interfaces.model import Model
from squasher_py.helpers.state import State


class LogModel(Model):
    def __init__(self, state: State) -> None:
        super().__init__(state)
        self.state = state

        self.prepareDir()

    @staticmethod
    def prepareDir() -> None:
        for dir in [
            LOG_DIR,
            OUTPUT_DIR,
            OUTPUT_SPLIT_DIR,
            OUTPUT_TILES_DIR,
        ]:
            if not path.exists(dir):
                print(f"Creating output directory...: {dir}")
                makedirs(dir, exist_ok=True)

    def __writeLog(self, data: str) -> None:
        with open(LOG_PATH, "a") as file:
            file.write(data + "\n")

    def __onUnitTime(self) -> None:
        state = self.state
        __FPS = state.FPS
        __frameIdx = state.frameIndex

        __slopeArr = state.slopeArr
        __slopeThresholdArr = state.slopeThresholdArr
        __clippingRange = state.clippingRangeArr

        data = {
            "frameIdx": __frameIdx,
            "FPS": __FPS,
            "hash": str(state.hashArr[-1]),
            "slope": str(__slopeArr[-1]),
            "slopeThreshold": str(__slopeThresholdArr[-1]),
            "clippingIdx": len(__clippingRange) - 1,
        }

        data["clippingRange"] = str(
            __clippingRange[-1] if len(__clippingRange) > 0 else None
        )

        self.__writeLog(json.dumps(data, ensure_ascii=False, indent=2))

    def update(self) -> None:
        state = self.state
        __FPS = state.FPS
        __frameIdx = state.frameIndex

        # On every second
        if __frameIdx % int(__FPS) == 0:
            self.__onUnitTime()

    def __del__(self) -> None:
        state = self.state
        __clippingRange = state.clippingRangeArr

        self.__writeLog(
            json.dumps(
                __clippingRange,
                ensure_ascii=False,
                indent=2,
            ),
        )
        return
