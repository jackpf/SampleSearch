import json
import sys
import traceback
from pathlib import Path

from google.protobuf.json_format import MessageToDict, Parse

from gen.cmds_pb2 import Request, Response

from .cmd.index_cmd import IndexCmd
from .cmd.search_cmd import SearchCmd
from .model.model import Model
from .repository.samples_repository import SamplesRepository

model = Model("laion/clap-htsat-unfused")
samples_repo = SamplesRepository(Path("db.db"))  # TODO Configurable
commands = {
    IndexCmd.name(): IndexCmd(model, samples_repo),
    SearchCmd.name(): SearchCmd(model, samples_repo),
}


def process_command(request: Request) -> Response:
    cmd = request.WhichOneof("payload")
    instance = commands.get(cmd)
    if instance:
        result = instance.run(instance.extract_request(request))
        return instance.pack_response(result)
    else:
        return Response(success=False, error_message=f"Unknown command: {cmd}")


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            request = Parse(line, Request())
            response = process_command(request)
        except Exception as e:
            # TODO Only if --verbose
            full_trace = traceback.format_exc()
            print(full_trace)
            response = Response(success=False, error_message=str(e))

        print(json.dumps(MessageToDict(response)), flush=True)


if __name__ == "__main__":
    main()
