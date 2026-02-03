from pathlib import Path

from gen.cmds_pb2 import IndexRequest, IndexResponse, Request, Response

from ..model.model import Model
from ..repository.samples_repository import SampleInfo, SamplesRepository
from .cmd import Cmd


class IndexCmd(Cmd[IndexRequest, IndexResponse]):
    _model: Model
    _sample_repo: SamplesRepository

    _supported_file_types = {".wav", ".mp3", ".aiff", ".flac", ".ogg"}

    def __init__(self, model: Model, sample_repo: SamplesRepository) -> None:
        super().__init__()
        self._model = model
        self._sample_repo = sample_repo

    @staticmethod
    def name() -> str:
        return "index"

    def extract_request(self, request: Request) -> IndexRequest:
        return request.index

    def pack_response(self, response: IndexResponse) -> Response:
        return Response(success=True, index=response)

    def _expand_path(self, path: Path) -> list[Path]:
        if path.is_dir():
            return [
                p.resolve()
                for p in path.rglob("*")
                if p.is_file() and p.suffix in self._supported_file_types
            ]
        else:
            return [path.resolve()]

    def run(self, request: IndexRequest) -> IndexResponse:
        files = self._expand_path(Path(request.path))

        samples = []
        inserted = []
        for file in files:
            audio_embedding = self._model.audio_embedding(request.path)
            mtime = 0.0  # TODO
            file_hash = ""  # TODO

            samples.append(
                SampleInfo(
                    id=None,
                    path=file,
                    mtime=mtime,
                    file_hash=file_hash,
                    vector=audio_embedding,
                )
            )
            inserted.append(str(file))

        self._sample_repo.upsert(samples)

        return IndexResponse(paths_indexed=inserted)
