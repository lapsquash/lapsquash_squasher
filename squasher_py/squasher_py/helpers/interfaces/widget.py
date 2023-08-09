from abc import ABCMeta, abstractmethod

from PySide6.QtWidgets import QWidget

from squasher_py.helpers.interfaces.event_loop import EventLoop
from squasher_py.helpers.state import State


class Widget(EventLoop, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, state: State) -> None:
        return

    @abstractmethod
    def get(self) -> QWidget:
        return

    @abstractmethod
    def update(self) -> None:
        return
