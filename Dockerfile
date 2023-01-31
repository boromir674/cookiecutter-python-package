FROM python:3.9.16-slim-bullseye as builder
# See https://github.com/python-poetry/poetry/discussions/1879#discussioncomment-216865
# for inspiration
COPY poetry.lock pyproject.toml ./

# Envrironment Configuration
## See https://github.com/alejandro-angulo/poetry/blob/master/docs/configuration.md
# Determine where to install poetry
ENV POETRY_HOME=/opt/poetry

# Install Poetry & generate a requirements.txt file
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python && \
    "$POETRY_HOME/bin/poetry" export -f requirements.txt > requirements.txt

FROM python:3.9.16-slim-bullseye

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

CMD [ "generate-python" ]
