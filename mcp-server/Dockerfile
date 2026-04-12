FROM python:3.11-slim

# Instalacja zależności systemowych (curl do sprawdzania połączenia)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalacja bibliotek pod Ollamę i MCP
RUN pip install --no-cache-dir \
    mcp[cli] \
    kubernetes \
    langchain \
    langchain-community \
    langchain-mcp-adapters \
    fastapi \
    uvicorn

# Kopiujemy kod
COPY mcp_server.py .
COPY mcp_client.py .

# Domyślnie uruchamiamy serwer, ale w K8s i tak nadpiszemy to przez 'command'
CMD ["python", "mcp_server.py"]