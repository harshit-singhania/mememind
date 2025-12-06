# Using Python 3.11 Slim (matching pyproject.toml requirement)
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Add poetry to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install system dependencies and Poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency definition
COPY pyproject.toml poetry.lock ./

# Install dependencies (runtime only)
RUN poetry install --no-root --only main

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run the application
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
