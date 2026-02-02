from gen.cmds_pb2 import IndexRequest, IndexResponse

from .cmd import Cmd


class IndexCmd(Cmd[IndexRequest, IndexResponse]):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def name() -> str:
        return "index"

    def run(self, request: IndexRequest) -> IndexResponse:
        # TODO: Implement indexing logic
        return IndexResponse()
