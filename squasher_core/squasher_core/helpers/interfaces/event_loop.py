from abc import ABCMeta, abstractmethod

from squasher_core.helpers.state import State


class EventLoop(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, state: State) -> None:
        return

    @abstractmethod
    def update(self) -> None:
        return
