from concurrent.futures import ThreadPoolExecutor
from os import makedirs, path

from cv2 import VideoWriter

from squasher_py.helpers.constants import OUTPUT_SPLIT_DIR, getOutputSplitPath
from squasher_py.helpers.interfaces.model import Model
from squasher_py.helpers.state import State, TypeFrameBuff


class OutputModel(Model):
    threadPool = ThreadPoolExecutor(max_workers=1000)
    writer: VideoWriter | None = None
    latestClippingRangeArrLength: int = 0

    def __init__(self, state: State) -> None:
        super().__init__(state)
        self.state = state

        if not path.exists(OUTPUT_SPLIT_DIR):
            print("Creating output directory...")
            makedirs(OUTPUT_SPLIT_DIR, exist_ok=True)

    def __writeFrame(
        self,
        frame: TypeFrameBuff,
        frameIdx: int,
    ) -> None:
        print(f"#{frameIdx} Writing frame...", end="\r")
        self.writer.write(frame)  # type: ignore

    def __on_unit_time(self) -> None:
        return

    def update(self) -> None:
        state = self.state
        __frameBuff = state.frameBuff
        __frameIdx = state.frameIndex
        __FPS = state.FPS
        __frameBuff = state.frameBuff
        __clippingRangeArr = state.clippingRangeArr

        clippingRangeArrLen = len(__clippingRangeArr)
        clippingIdx = clippingRangeArrLen - 1
        height, width, _ = __frameBuff.shape

        if clippingRangeArrLen != self.latestClippingRangeArrLength:
            print(f"{clippingIdx}.mp4: Creating output...")
            MP4_CODEC = 0x00000020
            self.writer = VideoWriter(
                getOutputSplitPath(clippingIdx),
                MP4_CODEC,
                __FPS,
                (width, height),
            )
            self.latestClippingRangeArrLength = clippingRangeArrLen

        if clippingRangeArrLen != 0 and __clippingRangeArr[-1].end is None:
            self.threadPool.submit(
                lambda: self.__writeFrame(
                    __frameBuff,
                    __frameIdx,
                )
            )

        # On every second
        if __frameIdx % int(__FPS) == 0:
            self.__on_unit_time()

    def __del__(self) -> None:
        print("Releasing output...")
        self.threadPool.shutdown(wait=True)
        print("Output released!")
        return
