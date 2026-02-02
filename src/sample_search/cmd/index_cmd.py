from cmd import Cmd


class IndexCmd(Cmd):
    @staticmethod
    def name() -> str:
        return "index"

    def __init__(self) -> None:
        super().__init__()

    def run(self) -> str:
        return "Dummy"
