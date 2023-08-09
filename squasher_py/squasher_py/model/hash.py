import numpy as np
import pandas as pd
from imagehash import dhash  # type: ignore
from PIL import Image

from squasher_py.helpers.constants import (
    CLIP_RANGE_MIN_SECOND,
    SLOPE_THRESHOLD_MAX,
    SLOPE_THRESHOLD_MIN,
)
from squasher_py.helpers.interfaces.model import Model
from squasher_py.helpers.state import ClipRange, State, TypeSlopeArr, TypeSlopeThreshold


class HashModel(Model):
    def __init__(self, state: State) -> None:
        super().__init__(state)
        self.state = state

    @staticmethod
    def applyFilter2ThresholdSlope(data: TypeSlopeThreshold) -> float:
        print(
            f"({SLOPE_THRESHOLD_MIN} < {data} < {SLOPE_THRESHOLD_MAX})",
            end=" -> ",
        )
        data = max(data, SLOPE_THRESHOLD_MIN)
        data = min(data, SLOPE_THRESHOLD_MAX)
        print(data, end="\r")
        return data

    @staticmethod
    def computeEMA(arr: TypeSlopeArr) -> float:
        return pd.Series(arr).ewm(span=10).mean().values[-1]  # type: ignore

    def __computeHash(self) -> None:
        state = self.state
        __FPS = state.FPS
        __frameIdx = state.frameIndex

        range = int(__FPS)
        partialHashArr = self.state.hashArr[-range:]

        frame = np.arange(__frameIdx - range, __frameIdx)
        hash = partialHashArr

        [slope, _] = np.polyfit(frame, hash, 1)
        self.state.slopeArr = np.append(self.state.slopeArr, abs(slope))

        slopeThreshold = self.computeEMA(self.state.slopeArr)
        self.state.slopeThresholdArr = np.append(
            self.state.slopeThresholdArr, slopeThreshold
        )

    def __computeClipRange(self) -> None:
        state = self.state
        __FPS = state.FPS
        __frameIdx = state.frameIndex
        __slopeArr = state.slopeArr
        __slopeThresholdArr = state.slopeThresholdArr
        __clippingRangeArr = state.clippingRangeArr

        slope = __slopeArr[-1]
        slopeThreshold = __slopeThresholdArr[-1]
        clippingRangeLength = len(__clippingRangeArr)
        clippingIdx = clippingRangeLength - 1

        # New clip range
        if clippingRangeLength == 0 or __clippingRangeArr[-1].end is not None:
            if slope > slopeThreshold:
                print()
                print(
                    f"[{clippingRangeLength}] CLIPPING START #{__frameIdx}..None",
                )
                self.state.clippingRangeArr.append(
                    ClipRange(
                        start=__frameIdx,
                        end=None,
                    ),
                )
            return

        # Existing clip range
        latestClipRange = __clippingRangeArr[-1]

        # Check whether clip range is in progress
        minFrame = CLIP_RANGE_MIN_SECOND * int(__FPS)
        clipRangeMinFrame = latestClipRange.start + minFrame
        if __frameIdx <= clipRangeMinFrame:
            print(f"|  Continue frame while #{__frameIdx} <= #{clipRangeMinFrame}")
            return

        assert latestClipRange.end is None

        # Mark end of clip range
        if slope < slopeThreshold:
            print(
                f"[{clippingIdx}] CLIPPING END #{__clippingRangeArr[-1].start}..#{__frameIdx}"
            )
            self.state.clippingRangeArr[-1] = ClipRange(
                start=latestClipRange.start,
                end=__frameIdx,
            )
            return

        print("|  Continue frame...")

    def __on_unit_time(self) -> None:
        self.__computeHash()
        self.__computeClipRange()

    def update(self) -> None:
        state = self.state
        __FPS = state.FPS
        __frameBuff = state.frameBuff
        __frameIdx = state.frameIndex

        hash = dhash(Image.fromarray(__frameBuff))  # type: ignore
        hashInt = int(str(hash), base=16)

        self.state.hashArr = np.append(self.state.hashArr, hashInt)

        # On every second
        if __frameIdx % int(__FPS) == 0:
            self.__on_unit_time()

    def __del__(self) -> None:
        return
