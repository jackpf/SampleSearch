from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Request = TypeVar("Request")
Response = TypeVar("Response")


class Cmd(ABC, Generic[Request, Response]):
    def __init__(self) -> None:
        pass


    @staticmethod
    @abstractmethod
    def name() -> str: ...

    @abstractmethod
    def run(self, request: Request) -> Response: ...
