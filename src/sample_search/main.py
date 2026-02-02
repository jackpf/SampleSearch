import argparse
import json
import sys

from sample_search.cmd.index_cmd import IndexCmd


def process_command(cmd: str) -> str:
    if cmd == IndexCmd.name():
        return IndexCmd().run()
    else:
        raise Exception(f"Unknown command: {cmd}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sample search")
    parser.add_argument("--db", type=str, required=True, help="Database file")

    for cmd in sys.stdin:
        response = process_command(cmd)
        print(json.dumps(response), flush=True)
