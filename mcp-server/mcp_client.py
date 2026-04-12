import argparse
import json

import anyio
from mcp import ClientSession
from mcp.client.sse import sse_client


async def run(url: str, tool_name: str | None, tool_args: dict) -> int:
    async with sse_client(url) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            if not tool_name:
                result = await session.list_tools()
                print("Dostepne narzedzia:")
                for tool in result.tools:
                    print(f"- {tool.name}")
                return 0

            result = await session.call_tool(tool_name, tool_args)
            print(result.model_dump_json(indent=2))
            return 0


def build_tool_args(parsed: argparse.Namespace) -> dict:
    if parsed.args:
        return json.loads(parsed.args)

    tool_args: dict = {}

    if parsed.namespace is not None:
        tool_args["namespace"] = parsed.namespace
    if parsed.name is not None:
        tool_args["name"] = parsed.name
    if parsed.replicas is not None:
        tool_args["replicas"] = parsed.replicas
    if parsed.users is not None:
        tool_args["users"] = parsed.users
    if parsed.rate is not None:
        tool_args["rate"] = parsed.rate

    return tool_args


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8000/sse")
    parser.add_argument("--tool", default=None)
    parser.add_argument("--args", default=None)
    parser.add_argument("--namespace", default=None)
    parser.add_argument("--name", default=None)
    parser.add_argument("--replicas", type=int, default=None)
    parser.add_argument("--users", type=int, default=None)
    parser.add_argument("--rate", type=int, default=None)
    parsed = parser.parse_args()

    try:
        tool_args = build_tool_args(parsed)
    except json.JSONDecodeError as exc:
        print(f"Niepoprawny JSON w --args: {exc}")
        return 1

    try:
        return anyio.run(run, parsed.url, parsed.tool, tool_args)
    except Exception as exc:
        print(f"Blad: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
