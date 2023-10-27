from os import path

from squasher_inspector.helpers.env import getEnv
from squasher_inspector.utils.parser import manifest2clippingRange  # noqa
from squasher_inspector.utils.parser import parseManifest
from squasher_inspector.utils.types.clipping import ClippingRange


def calculateMatchRate(
    rangeListTrue: list[ClippingRange],
    rangeListTarget: list[ClippingRange],
    errStart: int = 0,
    errEnd: int = 0,
) -> float:
    def extractRangeSet(range_list: list[ClippingRange]) -> set[int]:
        numbers: set[int] = set()
        for start, end in range_list:
            numbers.update(range(start - errStart, end + 1 + errEnd))
        return numbers

    setTrue = extractRangeSet(rangeListTrue)
    setTarget = extractRangeSet(rangeListTarget)

    # 一致した数値を数える
    matchedNumbers = setTrue.intersection(setTarget)

    # 一致率を計算
    return len(matchedNumbers) / len(setTrue) * 100


if __name__ == "__main__":
    env = getEnv()
    outDirTrue = env.INSPECT_TRUE_OUT_DIR
    outDirTarget = env.INSPECT_TARGET_OUT_DIR

    manifestTrue = parseManifest(path.join(outDirTrue, "manifest.json"))
    manifestTarget = parseManifest(path.join(outDirTarget, "manifest.json"))

    matchRate = calculateMatchRate(
        rangeListTrue=manifest2clippingRange(manifestTrue),
        rangeListTarget=manifest2clippingRange(manifestTarget),
    )
