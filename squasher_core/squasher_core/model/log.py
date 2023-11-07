import json
from os import makedirs, path
from time import time

from squasher_core.helpers.constants import (
    LOG_DIR,
    LOG_PATH,
    OUTPUT_DIR,
    OUTPUT_MANIFEST_PATH,
    OUTPUT_SPLIT_DIR,
    OUTPUT_TILES_DIR,
)
from squasher_core.helpers.interfaces.model import Model
from squasher_core.helpers.state import State
from squasher_core.model.utils.types.manifest import Manifest, ManifestAsset


class LogModel(Model):
    def __init__(self, state: State) -> None:
        super().__init__(state)
        self.state = state
        self.state.manifest = Manifest(
            name="sample",
            description="",
            version="",
            startWith=int(time()),
            assets=[],
        )

        self.prepareDir()
        self.__writeManifest()

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

    def __writeManifest(self) -> None:
        manifestJson = self.state.manifest.to_json(  # type: ignore
            indent=2,
            ensure_ascii=False,
        )

        with open(OUTPUT_MANIFEST_PATH, "w") as file:
            file.write(manifestJson)

    def __writeLog(self, data: str) -> None:
        with open(LOG_PATH, "a") as file:
            file.write(data + "\n")

    def __updateManifest(self) -> None:
        state = self.state
        __frameIdx = state.frameIndex
        __clippingRangeArr = state.clippingRangeArr
        __projectManifest = state.manifest

        # 切り抜き動画の生成完了 → manifest の assets に追加
        if __frameIdx == __clippingRangeArr[-1].end:
            lastClippingRange = __clippingRangeArr[-1]

            if lastClippingRange.end is None:
                raise RuntimeError("Clipping range is not set")

            durationSec = lastClippingRange.end - lastClippingRange.start
            elapsedSec = (int(time()) - __projectManifest.startWith) * 1000

            self.state.manifest.assets.append(
                ManifestAsset(
                    elapsedMs=elapsedSec * 1000,
                    durationMs=durationSec * 1000,
                    analysis=None,
                )
            )
            self.__writeManifest()

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
        self.__updateManifest()

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
