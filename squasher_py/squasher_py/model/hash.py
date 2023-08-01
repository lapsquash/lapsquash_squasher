import numpy as np
from imagehash import average_hash  # type: ignore
from PIL import Image

from squasher_py.helpers.interfaces.model import Model
from squasher_py.helpers.state import State


class HashModel(Model):
    def __init__(self, state: State) -> None:
        super().__init__(state)
        self.state = state

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
            print(f"#{__frameIdx:03} \t| 0x{hashInt:016X}")

    def __del__(self) -> None:
        pass
