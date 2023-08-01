from os import makedirs, path

from squasher_py.helpers.interfaces.model import Model
from squasher_py.helpers.state import State
from squasher_py.model.constants import LOG_DIR, LOG_PATH


class LogModel(Model):
    def __init__(self, state: State) -> None:
        super().__init__(state)
        self.state = state

        if not path.exists(LOG_DIR):
            print("Creating output directory...")
            makedirs(LOG_DIR, exist_ok=True)

    def update(self) -> None:
        __state = self.state
        __FPS = __state.FPS
        __frameIdx = __state.frameIndex
        __hashArr = __state.hashArr

        hash = __hashArr[-1]
        data = f"#{__frameIdx}\t{(__frameIdx/__FPS):.2f}s\t0x{int(hash):016X}\t{int(hash)}"  # noqa

        with open(LOG_PATH, "a") as file:
            file.write(data + "\n")

    def dispose(self) -> None:
        pass
