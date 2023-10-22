import json
from os import makedirs, path

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
from squasher_core.model.utils.types.manifest import (
    ProjectManifest,
    ProjectManifestAsset,
)


class LogModel(Model):
    projectManifest: ProjectManifest

    def __init__(self, state: State) -> None:
        super().__init__(state)
        self.state = state
        self.projectManifest = ProjectManifest(
            name="saple",
            description="sadfasd",
            version="",
            startWith=0,
            assets=[],
        )

        self.prepareDir()
        self.__writePjManifest()

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

    def __writePjManifest(self) -> None:
        pjManifestJson = self.projectManifest.to_json(  # type: ignore
            indent=2,
            ensure_ascii=False,
        )

        with open(OUTPUT_MANIFEST_PATH, "w") as file:
            file.write(pjManifestJson)

    def __writeLog(self, data: str) -> None:
        with open(LOG_PATH, "a") as file:
            file.write(data + "\n")

    def __updatePjManifest(self) -> None:
        state = self.state
        __frameIdx = state.frameIndex
        __clippingRangeArr = state.clippingRangeArr

        # 切り抜き動画の生成完了 → PjManifest の assets に追加
        if __frameIdx == __clippingRangeArr[-1].end:
            assert __clippingRangeArr[-1].end is not None

            durationMs = (
                __clippingRangeArr[-1].end - __clippingRangeArr[-1].start
            ) * 1000

            self.projectManifest.assets.append(
                ProjectManifestAsset(
                    elapsedMs=0,
                    durationMs=durationMs,
                    analysis=None,
                )
            )
            self.__writePjManifest()

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
        self.__updatePjManifest()

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
