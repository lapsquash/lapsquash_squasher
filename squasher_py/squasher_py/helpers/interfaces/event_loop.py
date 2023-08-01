from abc import ABCMeta, abstractmethod

from squasher_py.helpers.state import State


class EventLoop(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, state: State) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass