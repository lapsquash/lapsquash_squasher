from concurrent.futures import ThreadPoolExecutor
from os import makedirs, path

from cv2 import VideoWriter

from squasher_py.helpers.constants import OUTPUT_SPLIT_DIR, getOutputSplitPath
from squasher_py.helpers.interfaces.model import Model
from squasher_py.helpers.state import State, TypeFrameBuff


class OutputModel(Model):
    threadPool = ThreadPoolExecutor()
    writer: VideoWriter | None = None

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

    def update(self) -> None:
        state = self.state
        __frameBuff = state.frameBuff
        __frameIdx = state.frameIndex
        __FPS = state.FPS
        __frameBuff = state.frameBuff

        height, width, _ = __frameBuff.shape

        # Initialize writer (only once)
        if self.writer is None:
            MP4_CODEC = 0x00000020
            self.writer = VideoWriter(
                getOutputSplitPath(1),
                MP4_CODEC,
                __FPS,
                (width, height),
            )

        self.threadPool.submit(
            lambda: self.__writeFrame(
                __frameBuff,
                __frameIdx,
            )
        )

    def __del__(self) -> None:
        print("Releasing output...")
        self.threadPool.shutdown(wait=True)
        print("Output released!")
        pass
