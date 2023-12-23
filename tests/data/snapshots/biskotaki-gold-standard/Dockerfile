FROM python:3.9.16-slim-bullseye as builder

COPY poetry.lock pyproject.toml ./

# Determine where to install poetry
ENV POETRY_HOME=/opt/poetry

# Install Poetry & generate a requirements.txt file
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python && \
    "$POETRY_HOME/bin/poetry" export -f requirements.txt > requirements.txt

FROM python:3.9.16-slim-bullseye as install

# Keep the requirements.txt file from the builder image
COPY --from=builder requirements.txt .

# Pre emptively add the user's bin folder to PATH
ENV PATH="/root/.local/bin:$PATH"

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    pip install -U pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --user -r requirements.txt

COPY . .
RUN pip install --no-cache-dir --user .
