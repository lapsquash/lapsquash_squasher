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

    def __writeLog(self, data: str) -> None:
        with open(LOG_PATH, "a") as file:
            file.write(data + "\n")

    def __on_unit_time(self) -> None:
        state = self.state
        __FPS = state.FPS
        __frameIdx = state.frameIndex

        __slopeArr = state.slopeArr
        __slopeThresholdArr = state.slopeThresholdArr

        data = "\t".join(
            [
                f"#{__frameIdx - int(__FPS)}..#{__frameIdx}",
                f"| {(__slopeArr[-1]):.2f}",
                f"| {(__slopeThresholdArr[-1]):.2f}",
            ]
        )

        self.__writeLog(data)

    def update(self) -> None:
        state = self.state
        __FPS = state.FPS
        __frameIdx = state.frameIndex

        # On every second
        if __frameIdx % int(__FPS) == 0:
            self.__on_unit_time()

    def __del__(self) -> None:
        return
