import numpy as np
from imagehash import average_hash  # type: ignore
from PIL import Image

from squasher_py.helpers.constants import LOG_PATH
from squasher_py.helpers.interfaces.model import Model
from squasher_py.helpers.state import State


class HashModel(Model):
    def __init__(self, state: State) -> None:
        super().__init__(state)
        self.state = state

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

        hash = average_hash(Image.fromarray(__frameBuff))  # type: ignore
        hashInt = int(str(hash), base=16)

        self.state.hashArr = np.append(self.state.hashArr, hashInt)

        # Print hash every second
        if __frameIdx % int(__FPS) == 0:
            self.__on_unit_time()

    def __del__(self) -> None:
        pass
