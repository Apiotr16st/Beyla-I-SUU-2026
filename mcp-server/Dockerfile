FROM python:3.11-slim

WORKDIR /app

COPY requirements-server.txt .
RUN pip install --no-cache-dir -r requirements-server.txt

COPY mcp_server.py .

CMD ["python", "mcp_server.py"]
