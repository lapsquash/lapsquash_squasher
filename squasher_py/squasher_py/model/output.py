from concurrent.futures import ThreadPoolExecutor
from os import makedirs, path

from cv2 import VideoWriter

from squasher_py.helpers.constants import OUTPUT_SPLIT_DIR, getOutputSplitPath
from squasher_py.helpers.interfaces.model import Model
from squasher_py.helpers.state import State, TypeFrame


class OutputModel(Model):
    threadPool = ThreadPoolExecutor(max_workers=1000)
    writer: VideoWriter | None = None
    latestClippingRangeArrLen: int = 0

    def __init__(self, state: State) -> None:
        super().__init__(state)
        self.state = state

        if not path.exists(OUTPUT_SPLIT_DIR):
            print("Creating output directory...")
            makedirs(OUTPUT_SPLIT_DIR, exist_ok=True)

    def __writeFrame(
        self,
        frame: TypeFrame,
        frameIdx: int,
    ) -> None:
        print(f"#{frameIdx} Writing frame...", end="\r")
        self.writer.write(frame)  # type: ignore

    def __onUnitTime(self) -> None:
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

        if clippingRangeArrLen == 0:
            return

        # 切り抜き範囲の数が変化したら, 新しいファイルの準備
        if clippingRangeArrLen != self.latestClippingRangeArrLen:
            print(f"{clippingIdx}.mp4: Creating output...")
            MP4_CODEC = 0x00000020
            self.writer = VideoWriter(
                getOutputSplitPath(clippingIdx),
                MP4_CODEC,
                __FPS,
                (width, height),
            )
            self.latestClippingRangeArrLen = clippingRangeArrLen

        # 最後の切り抜き範囲の終点が None (= 未確定) のとき, 書き込む
        if __clippingRangeArr[-1].end is None:
            self.threadPool.submit(
                lambda: self.__writeFrame(
                    __frameBuff,
                    __frameIdx,
                )
            )

        if __frameIdx % int(__FPS) == 0:
            self.__onUnitTime()

    def __del__(self) -> None:
        print("Releasing output...")
        self.threadPool.shutdown(wait=True)
        print("Output released!")
        return
