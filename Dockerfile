# ---- Build stage ----
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

# Install dependencies first (cache-friendly layer ordering)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy source and install the project
COPY src/ src/
RUN uv sync --frozen --no-dev

# ---- Runtime stage ----
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy the virtual environment from the builder
COPY --from=builder /app/.venv /app/.venv

# Ensure the venv binaries are on PATH
ENV PATH="/app/.venv/bin:$PATH"

# stdio transport -- no EXPOSE needed
ENTRYPOINT ["garmin-mcp"]
