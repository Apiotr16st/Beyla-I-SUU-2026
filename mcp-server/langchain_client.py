import argparse
import json
from typing import Any

import anyio
from langchain.agents import AgentType, initialize_agent
from langchain.tools import StructuredTool
from langchain_ollama import ChatOllama
from mcp import ClientSession
from mcp.client.sse import sse_client


SYSTEM_GUIDANCE = """
You are a Kubernetes operations assistant.
Always verify deployment names before making changes.
If the user uses a fuzzy name like "ad service", first call list_deployments.
Prefer namespace "app" unless the user explicitly asks for another namespace.
Be concise.
""".strip()


async def _call_mcp_tool(tool_name: str, arguments: dict[str, Any], mcp_url: str) -> str:
    async with sse_client(mcp_url) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            if hasattr(result, "model_dump_json"):
                return result.model_dump_json(indent=2)
            if hasattr(result, "model_dump"):
                return json.dumps(result.model_dump(), ensure_ascii=False, indent=2)
            return json.dumps(result, ensure_ascii=False, default=str, indent=2)


def make_tools(mcp_url: str) -> list[StructuredTool]:
    def list_deployments(namespace: str = "app") -> str:
        """List deployments in the selected namespace."""
        return anyio.run(_call_mcp_tool, "list_deployments", {"namespace": namespace}, mcp_url)

    def list_pods(namespace: str = "app") -> str:
        """List pods in the selected namespace."""
        return anyio.run(_call_mcp_tool, "list_pods", {"namespace": namespace}, mcp_url)

    def scale_deployment(name: str, replicas: int, namespace: str = "app") -> str:
        """Scale a deployment to the requested number of replicas."""
        return anyio.run(
            _call_mcp_tool,
            "scale_deployment",
            {"name": name, "replicas": replicas, "namespace": namespace},
            mcp_url,
        )

    def restart_deployment(name: str, namespace: str = "app") -> str:
        """Trigger a rolling restart of a deployment."""
        return anyio.run(
            _call_mcp_tool,
            "restart_deployment",
            {"name": name, "namespace": namespace},
            mcp_url,
        )

    def set_loadgenerator(users: int, rate: int, namespace: str = "app") -> str:
        """Set USERS and RATE on the loadgenerator deployment."""
        return anyio.run(
            _call_mcp_tool,
            "set_loadgenerator",
            {"users": users, "rate": rate, "namespace": namespace},
            mcp_url,
        )

    return [
        StructuredTool.from_function(list_deployments),
        StructuredTool.from_function(list_pods),
        StructuredTool.from_function(scale_deployment),
        StructuredTool.from_function(restart_deployment),
        StructuredTool.from_function(set_loadgenerator),
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--model", default="qwen3")
    parser.add_argument("--ollama-url", default="http://localhost:11434")
    parser.add_argument("--mcp-url", default="http://localhost:8000/sse")
    args = parser.parse_args()

    llm = ChatOllama(
        model=args.model,
        base_url=args.ollama_url,
        temperature=0,
    )
    tools = make_tools(args.mcp_url)

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )

    final_prompt = f"{SYSTEM_GUIDANCE}\n\nUser request: {args.prompt}"
    result = agent.run(final_prompt)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
