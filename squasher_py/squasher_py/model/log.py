from os import makedirs, path

from squasher_py.helpers.constants import LOG_DIR, LOG_PATH
from squasher_py.helpers.interfaces.model import Model
from squasher_py.helpers.state import State


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
        __hashArr = __state.hashArr

        hash = __hashArr[-1]
        data = f"{__FPS:.2f}\t0x{int(hash):016X}"

        with open(LOG_PATH, "a") as file:
            file.write(data + "\n")

    def __del__(self) -> None:
        pass
