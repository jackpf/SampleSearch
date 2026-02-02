import sys

from google.protobuf.json_format import MessageToJson, Parse

from gen.cmds_pb2 import Request, Response

from .cmd.index_cmd import IndexCmd

commands = {
    IndexCmd.name(): IndexCmd,
}


def process_command(request: Request) -> Response:
    cmd = request.WhichOneof("payload")
    instance = commands.get(cmd)
    if instance:
        result = instance().run(request.index)
        return Response(success=True, index=result)
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
            response = Response(success=False, error_message=str(e))

        print(MessageToJson(response), flush=True)


if __name__ == "__main__":
    main()
