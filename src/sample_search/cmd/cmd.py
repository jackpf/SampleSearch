from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from gen.cmds_pb2 import Request as ProtoRequest, Response as ProtoResponse

Request = TypeVar("Request")
Response = TypeVar("Response")


class Cmd(ABC, Generic[Request, Response]):
    def __init__(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def name() -> str: ...

    @abstractmethod
    def extract_request(self, request: ProtoRequest) -> Request: ...

    @abstractmethod
    def pack_response(self, response: Response) -> ProtoResponse: ...

    @abstractmethod
    def run(self, request: Request) -> Response: ...
