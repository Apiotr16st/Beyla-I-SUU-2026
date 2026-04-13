import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from langchain_client import run_prompt


DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
DEFAULT_MCP_URL = os.getenv("MCP_URL", "http://host.docker.internal:8000/sse")

app = FastAPI(title="Prompt Service", version="1.0.0")


class PromptRequest(BaseModel):
    prompt: str
    model: str = DEFAULT_MODEL


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "default_model": DEFAULT_MODEL,
        "mcp_url": DEFAULT_MCP_URL,
    }


@app.post("/prompt")
def prompt(request: PromptRequest) -> dict:
    try:
        answer = run_prompt(
            prompt=request.prompt,
            model=request.model,
            mcp_url=DEFAULT_MCP_URL,
        )
        return {"answer": answer}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
