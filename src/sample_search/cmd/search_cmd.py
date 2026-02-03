from gen.cmds_pb2 import SearchRequest, SearchResponse, SearchResult, Request, Response
from .cmd import Cmd, Request
from ..model.model import Model
from ..repository.samples_repository import SamplesRepository


class SearchCmd(Cmd[SearchRequest, SearchResponse]):
    _model: Model
    _sample_repo: SamplesRepository

    def __init__(self, model: Model, sample_repo: SamplesRepository) -> None:
        super().__init__()
        self._model = model
        self._sample_repo = sample_repo

    @staticmethod
    def name() -> str:
        return "search"

    def extract_request(self, request: Request) -> SearchRequest:
        return request.search

    def pack_response(self, response: SearchResponse) -> Response:
        return Response(success=True, search=response)

    def run(self, request: SearchRequest) -> SearchResponse:
        query_vector = self._model.text_embedding(request.query)

        samples = self._sample_repo.search(query_vector)

        results = []
        for sample in samples:
            results.append(SearchResult(
                path=str(sample.sample_info.path),
                score=sample.score,
            ))

        return SearchResponse(results=results)
