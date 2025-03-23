# FROM scratch as ENV_SETUP
# can be ovveriden by --build-arg PY_VERSION=3.9.16
ARG PY_VERSION=3.9.16
FROM python:${PY_VERSION}-slim-bullseye as base

# ENV PY_RUNTIME=${PY_VERSION}

FROM base as builder

COPY poetry.lock pyproject.toml ./

# Configure installation location, for 'install.python-poetry.org' script
ENV POETRY_HOME=/opt/poetry

# Install Poetry
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python
# Install plugin for 'poetry export' command
RUN "$POETRY_HOME/bin/poetry" self add poetry-plugin-export

FROM builder AS prod_builder

#  & export pinned Prod (install only) dependencies, into pip format
RUN "$POETRY_HOME/bin/poetry" export -f requirements.txt > requirements.txt

FROM builder AS test_builder

RUN "$POETRY_HOME/bin/poetry" export -f requirements.txt -E test > requirements-test.txt


FROM scratch as source

WORKDIR /app

COPY --from=prod_builder requirements.txt .
# Copy Source Code
# COPY . .
COPY src src
COPY pyproject.toml .
COPY poetry.lock .
COPY LICENSE .
COPY README.rst .


FROM base as base_env

# Wheels Directory for Distro and its Dependencies (aka requirements)
ENV DISTRO_WHEELS=/app/dist

FROM base_env AS build_wheels

# Essential build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    pip install -U pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Essential build-time dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry-core && \
    pip install --no-cache-dir build

WORKDIR /app
COPY --from=source /app .

# Build Wheels for Distro's Dependencies, from /app/requirements.txt file
RUN pip wheel --wheel-dir "${DISTRO_WHEELS}" -r ./requirements.txt

# Build Wheels for Distro's Package
RUN python -m build --outdir "/tmp/build-wheels" && \
    mv /tmp/build-wheels/*.whl "${DISTRO_WHEELS}"

# Now all wheels are in DISTRO_WHEELS folder

FROM base_env AS install

# At runtime our app needs git binary
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# we copy the wheels built in 'build_wheels' stage
COPY --from=build_wheels ${DISTRO_WHEELS} dist

# Install wheels for our Distro and its Install/Runtime Dependencies
# in user site-packages (ie /root/.local/lib/python3.11/site-packages)
RUN pip install --no-cache-dir --user ./dist/*.whl


## TEST ##

# EDIT MODE TEST
FROM base AS test_dev
WORKDIR /app

COPY --from=test_builder requirements-test.txt .

# Install test dependencies
RUN pip install --no-cache-dir --user -r requirements-test.txt

# Copy Source Code
COPY src src
COPY pyproject.toml .
# COPY poetry.lock .
COPY LICENSE .
COPY README.rst .
# COPY tests tests

# Install in Editable Mode
RUN pip install --no-cache-dir --user -e .

# Add Pytest, installed in user's bin folder, to PATH
ENV PATH="/root/.local/bin:$PATH"

CMD [ "pytest", "-vvs", "-ra", "tests" ]

# docker build --target test_dev -t ela-test-dev .
# docker run --rm -v /data/repos/cookiecutter-python-package/.github/biskotaki.yaml:/app/.github/biskotaki.yaml -v /data/repos/cookiecutter-python-package/tests:/app/tests -it ela-test-dev


# WHEEL TEST
FROM install AS test

COPY --from=test_builder requirements-test.txt .

# Install test dependencies
RUN pip install --no-cache-dir --user -r requirements-test.txt

# Add Pytest, installed in user's bin folder, to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy Test Suite, aka Unit Tests
COPY tests tests

# Copy Pytest Configuration
COPY pyproject.toml .

CMD [ "pytest", "-vvs", "-ra", "tests" ]


## PROD ##

FROM install AS prod

# Add Pytest, installed in user's bin folder, to PATH
ENV PATH="/root/.local/bin:$PATH"

ENTRYPOINT [ "generate-python" ]

# docker build -t generate-python .

# docker run -it --rm -v ${PWD}/.github/biskotaki.yaml:/app/config.yml -v /tmp/gen:/tmp/gen generate-python --config-file /app/config.yml -o /tmp/gen --no-input
