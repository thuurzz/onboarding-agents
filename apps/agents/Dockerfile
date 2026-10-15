FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

# Instala dependências (cache-friendly)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copia o código
COPY app ./app

EXPOSE 8002

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
