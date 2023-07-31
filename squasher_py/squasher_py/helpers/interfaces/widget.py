from abc import ABCMeta, abstractmethod

from PySide6.QtWidgets import QWidget

from squasher_py.helpers.state import State


class Widget(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, state: State) -> None:
        pass

    @abstractmethod
    def get(self) -> QWidget:
        pass

    @abstractmethod
    def update(self) -> None:
        pass
