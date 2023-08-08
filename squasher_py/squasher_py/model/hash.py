import numpy as np
import pandas as pd
from imagehash import dhash  # type: ignore
from PIL import Image

from squasher_py.helpers.constants import (
    LOG_PATH,
    SLOPE_THRESHOLD_MAX,
    SLOPE_THRESHOLD_MIN,
)
from squasher_py.helpers.interfaces.model import Model
from squasher_py.helpers.state import State


class HashModel(Model):
    def __init__(self, state: State) -> None:
        super().__init__(state)
        self.state = state

    @staticmethod
    def applyFilter2ThresholdSlope(data: float) -> float:
        print(
            f"{SLOPE_THRESHOLD_MIN} < {data} < {SLOPE_THRESHOLD_MAX}",
            end=" -> ",
        )
        data = max(data, SLOPE_THRESHOLD_MIN)
        data = min(data, SLOPE_THRESHOLD_MAX)
        print(data, end="\r")
        return data

    @staticmethod
    def computeEMA(
        arr: np.ndarray[float, np.dtype[np.float64]],
    ) -> float:
        return pd.Series(arr).ewm(span=10).mean().values[-1]  # type: ignore

    def __on_unit_time(self) -> None:
        __state = self.state
        __FPS = __state.FPS
        __frameIdx = __state.frameIndex

        range = int(__FPS)
        partialHashArr = self.state.hashArr[-range:]

        frame = np.arange(__frameIdx - range, __frameIdx)
        hash = partialHashArr

        [slope, _] = np.polyfit(frame, hash, 1)
        self.state.slopeArr = np.append(self.state.slopeArr, abs(slope))
        self.state.slopeThresholdArr = np.append(
            self.state.slopeThresholdArr,
            self.computeEMA(
                self.state.slopeArr,
            ),
        )

        __slopeArr = self.state.slopeArr
        __slopeThresholdArr = self.state.slopeThresholdArr

        if __slopeArr[-1] > __slopeThresholdArr[-1]:
            print(f"{__slopeArr[-1] } > {__slopeThresholdArr[-1]}")
        data = "\t".join(
            [
                f"#{__frameIdx - int(__FPS)}..#{__frameIdx}",
                f"| {(slope):.2f}",
            ]
        )
        with open(LOG_PATH, "a") as file:
            file.write(data + "\n")

    def update(self) -> None:
        __state = self.state
        __FPS = __state.FPS
        __frameBuff = __state.frameBuff
        __frameIdx = __state.frameIndex

        hash = dhash(Image.fromarray(__frameBuff))  # type: ignore
        hashInt = int(str(hash), base=16)

        self.state.hashArr = np.append(self.state.hashArr, hashInt)

        # Print hash every second
        if __frameIdx % int(__FPS) == 0:
            self.__on_unit_time()

    def __del__(self) -> None:
        pass
