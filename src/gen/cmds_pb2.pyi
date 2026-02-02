from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Request(_message.Message):
    __slots__ = ()
    INDEX_FIELD_NUMBER: _ClassVar[int]
    index: IndexRequest
    def __init__(self, index: _Optional[_Union[IndexRequest, _Mapping]] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ()
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_message: str
    index: IndexResponse
    def __init__(self, success: _Optional[bool] = ..., error_message: _Optional[str] = ..., index: _Optional[_Union[IndexResponse, _Mapping]] = ...) -> None: ...

class IndexRequest(_message.Message):
    __slots__ = ()
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    filename: str
    def __init__(self, filename: _Optional[str] = ...) -> None: ...

class IndexResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
