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
from squasher_py.helpers.state import (
    ClippingRange,
    State,
    TypeSlopeArr,
    TypeSlopeThreshold,
)


class HashModel(Model):
    def __init__(self, state: State) -> None:
        super().__init__(state)
        self.state = state

    @staticmethod
    def applyFilter2ThresholdSlope(data: TypeSlopeThreshold) -> float:
        """動的なしきい値にフィルター (最大, 最小) を適用する"""
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
        """指数移動平均を計算する"""
        return pd.Series(arr).ewm(span=10).mean().values[-1]  # type: ignore

    def __computeSlope(self) -> None:
        """類似度ハッシュの変化率を計算する"""
        state = self.state
        __FPS = state.FPS
        __frameIdx = state.frameIndex

        # 過去 1 秒の類似度ハッシュの配列の取得
        range = int(__FPS)
        partialHashArr = self.state.hashArr[-range:]

        # 1 秒前から現時点の累計フレーム数の等差数列
        partialFrameIdx = np.arange(__frameIdx - range, __frameIdx)

        # 最小二乗法で変化率を計算
        [slope, _] = np.polyfit(
            partialFrameIdx,  # x 軸
            partialHashArr,  # y 軸
            1,  # 次元
        )
        self.state.slopeArr = np.append(self.state.slopeArr, abs(slope))

        # 変化率から動的なしきい値を計算
        slopeThreshold = self.computeEMA(self.state.slopeArr)
        self.state.slopeThresholdArr = np.append(
            self.state.slopeThresholdArr, slopeThreshold
        )

    def __createNewClippingRange(self) -> None:
        """新しい切り抜き範囲を作成する"""
        state = self.state
        __frameIdx = state.frameIndex
        __slopeArr = state.slopeArr
        __slopeThresholdArr = state.slopeThresholdArr
        __clippingRangeArr = state.clippingRangeArr

        slope = __slopeArr[-1]
        slopeThreshold = __slopeThresholdArr[-1]
        clippingRangeLen = len(__clippingRangeArr)

        # 切り抜き範囲の開始をマーク
        if slope > slopeThreshold:
            print(
                f"\n[{clippingRangeLen}] CLIPPING START #{__frameIdx}..None",
            )
            self.state.clippingRangeArr.append(
                ClippingRange(
                    start=__frameIdx,
                    end=None,
                ),
            )

    def __computeClippingRange(self) -> None:
        state = self.state
        __FPS = state.FPS
        __frameIdx = state.frameIndex
        __slopeArr = state.slopeArr
        __slopeThresholdArr = state.slopeThresholdArr
        __clippingRangeArr = state.clippingRangeArr

        slope = __slopeArr[-1]
        slopeThreshold = __slopeThresholdArr[-1]
        clippingRangeLen = len(__clippingRangeArr)
        clippingIdx = clippingRangeLen - 1

        # 新しい切り抜き範囲をセット
        if clippingRangeLen == 0 or __clippingRangeArr[-1].end is not None:
            self.__createNewClippingRange()
            return

        latestClippingRange = __clippingRangeArr[-1]
        minFrame = CLIP_RANGE_MIN_SECOND * int(__FPS)
        clippingRangeMinFr = latestClippingRange.start + minFrame

        # 切り抜き範囲が最低フレーム数を満たしていない場合は継続
        if __frameIdx <= clippingRangeMinFr:
            print(
                "|  Continue frame while #{} <= #{}".format(
                    __frameIdx, clippingRangeMinFr
                ),
            )
            return

        assert latestClippingRange.end is None

        # 切り抜き範囲の終了をマーク
        if slope < slopeThreshold:
            print(
                "[{}] CLIPPING END #{}..#{}".format(
                    clippingIdx, __clippingRangeArr[-1].start, __frameIdx
                )
            )
            self.state.clippingRangeArr[-1] = ClippingRange(
                start=latestClippingRange.start,
                end=__frameIdx,
            )
            return

        print("|  Continue frame...")

    def __onUnitTime(self) -> None:
        self.__computeSlope()
        self.__computeClippingRange()

    def update(self) -> None:
        state = self.state
        __FPS = state.FPS
        __frameBuff = state.frameBuff
        __frameIdx = state.frameIndex

        # 類似度ハッシュの計算
        hash = dhash(Image.fromarray(__frameBuff))  # type: ignore
        hashInt = int(str(hash), base=16)

        self.state.hashArr = np.append(self.state.hashArr, hashInt)

        # 毎秒ごとの処理
        if __frameIdx % int(__FPS) == 0:
            self.__onUnitTime()

    def __del__(self) -> None:
        return
