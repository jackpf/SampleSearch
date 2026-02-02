from abc import ABC, abstractmethod


class Cmd(ABC):
    def __init__(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def name() -> str: ...

    @abstractmethod
    def run(self) -> str: ...
