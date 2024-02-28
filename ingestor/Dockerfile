FROM python:3.11-slim


# Configure Poetry
ENV POETRY_VERSION=1.5.1

# Install poetry separated from system interpreter
RUN python3 -m pip install --user pipx \
    && python3 -m pipx ensurepath \
    && python3 -m pipx install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-root --no-ansi

COPY ./ ./


CMD ["poetry", "run",  "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]