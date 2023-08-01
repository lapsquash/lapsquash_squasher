from abc import ABCMeta, abstractmethod

from squasher_py.helpers.interfaces.event_loop import EventLoop
from squasher_py.helpers.state import State


class Model(EventLoop, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, state: State) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def dispose(self) -> None:
        pass
