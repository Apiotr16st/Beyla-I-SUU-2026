import argparse
import json
import traceback
from typing import Any
from urllib import request

import anyio
from mcp import ClientSession
from mcp.client.sse import sse_client


SYSTEM_PROMPT = (
    "You are a Kubernetes operations assistant. "
    "Use tools when they are needed. "
    "Prefer namespace app unless the user explicitly asks for another namespace. "
    "Be concise and operational."
)


def to_ollama_tool(tool: Any) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description or "",
            "parameters": tool.inputSchema or {"type": "object", "properties": {}},
        },
    }


def ollama_chat(ollama_url: str, model: str, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> dict[str, Any]:
    payload = {
        "model": model,
        "messages": messages,
        "tools": tools,
        "stream": False,
    }
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url=f"{ollama_url.rstrip('/')}/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


def stringify_tool_result(result: Any) -> str:
    if hasattr(result, "model_dump"):
        return json.dumps(result.model_dump(), ensure_ascii=False)
    if hasattr(result, "dict"):
        return json.dumps(result.dict(), ensure_ascii=False)
    return json.dumps(result, ensure_ascii=False, default=str)


async def run(prompt: str, model: str, mcp_url: str, ollama_url: str, max_steps: int) -> int:
    async with sse_client(mcp_url) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            tools_result = await session.list_tools()
            ollama_tools = [to_ollama_tool(tool) for tool in tools_result.tools]

            messages: list[dict[str, Any]] = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ]

            for step in range(1, max_steps + 1):
                response = await anyio.to_thread.run_sync(
                    ollama_chat,
                    ollama_url,
                    model,
                    messages,
                    ollama_tools,
                )
                message = response["message"]
                assistant_message: dict[str, Any] = {
                    "role": "assistant",
                    "content": message.get("content", ""),
                }

                tool_calls = message.get("tool_calls") or []
                if tool_calls:
                    assistant_message["tool_calls"] = tool_calls
                messages.append(assistant_message)

                if not tool_calls:
                    print(message.get("content", "").strip())
                    return 0

                print(f"Krok {step}: model wybral {len(tool_calls)} narzedzie(a).")

                for call in tool_calls:
                    function = call["function"]
                    tool_name = function["name"]
                    arguments = function.get("arguments", {})
                    print(f"-> {tool_name}({json.dumps(arguments, ensure_ascii=False)})")

                    tool_result = await session.call_tool(tool_name, arguments)
                    tool_content = stringify_tool_result(tool_result)
                    messages.append(
                        {
                            "role": "tool",
                            "tool_name": tool_name,
                            "content": tool_content,
                        }
                    )

            print(f"Przekroczono limit krokow: {max_steps}")
            return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--model", default="llama3")
    parser.add_argument("--mcp-url", default="http://localhost:8000/sse")
    parser.add_argument("--ollama-url", default="http://localhost:11434")
    parser.add_argument("--max-steps", type=int, default=5)
    args = parser.parse_args()

    try:
        return anyio.run(run, args.prompt, args.model, args.mcp_url, args.ollama_url, args.max_steps)
    except Exception as exc:
        print(f"Blad: {exc}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
