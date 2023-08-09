from abc import ABCMeta, abstractmethod

from squasher_py.helpers.interfaces.event_loop import EventLoop
from squasher_py.helpers.state import State


class Model(EventLoop, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, state: State) -> None:
        return

    @abstractmethod
    def update(self) -> None:
        return

    @abstractmethod
    def __del__(self) -> None:
        return
