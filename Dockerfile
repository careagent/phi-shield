FROM python:3.12-slim

WORKDIR /app

# Install Tesseract OCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first for caching
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY phi_shield.py server.py section_parser.py tokenizer.py ocr.py ./

# Download model at build time so it's baked into the image
RUN uv run python -c "from gliner2 import GLiNER2; GLiNER2.from_pretrained('fastino/gliner2-large-v1'); print('Model cached')"

ENV PORT=18820
EXPOSE 18820

CMD ["uv", "run", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "18820"]
