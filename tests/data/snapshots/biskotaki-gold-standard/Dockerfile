# Wheels Directory for Distro and its Dependencies (aka requirements)
ARG DISTRO_WHEELS=/app/dist
# https://docs.docker.com/build/building/variables/#scoping

# can be ovveriden by --build-arg PYTHON_TAG=3.11.12
ARG PY_VERSION=3.11.12
FROM python:${PY_VERSION}-alpine AS python_alpine

# ENV PY_RUNTIME=${PY_VERSION}

FROM python_alpine AS builder

COPY uv.lock pyproject.toml ./

# Install uv
COPY --from=ghcr.io/astral-sh/uv@sha256:2381d6aa60c326b71fd40023f921a0a3b8f91b14d5db6b90402e65a635053709 /uv /uvx /bin/

# Export Exact/Pinned Prod (install only) dependencies, into pip format
FROM builder AS prod_builder
RUN uv export --no-dev --frozen --no-emit-project -f requirements-txt -o requirements.txt

# Export Exact/Pinned Prod + Test dependencies, into pip format
FROM builder AS test_builder
RUN uv export --no-dev --frozen --no-emit-project -f requirements-txt -o requirements.txt --extra test

# Export Exact/Pinned Prod + Docs dependencies, into pip format
FROM builder AS docs_builder
RUN uv export --no-dev --frozen --no-emit-project -f requirements-txt -o requirements.txt --extra docs


#### PLACE SOURCE FILES - STAGE ####
FROM scratch as source

WORKDIR /app

COPY --from=prod_builder requirements.txt .
# Copy Source Code
# COPY . .
COPY src src
COPY pyproject.toml .
COPY uv.lock .
COPY LICENSE .
COPY README.md .


###### BUILD WHEELS from Sources - STAGE ######
FROM python_alpine AS build_wheels
ARG DISTRO_WHEELS

# Essential build tools
RUN apk update && \
    apk add --no-cache build-base && \
    pip install -U pip && \
    rm -rf /var/cache/apk/*

# Essential build-time dependencies
COPY --from=ghcr.io/astral-sh/uv@sha256:2381d6aa60c326b71fd40023f921a0a3b8f91b14d5db6b90402e65a635053709 /uv /uvx /bin/
# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir poetry-core && \
#     pip install --no-cache-dir build

WORKDIR /app
COPY --from=source /app .

# Build Wheels for Distro's Dependencies, from /app/requirements.txt file
RUN pip wheel --wheel-dir "${DISTRO_WHEELS}" -r ./requirements.txt

# Build Wheels for Distro's (own) Package
RUN uv build --wheel --out-dir "/tmp/build-wheels" && \
    mkdir -p "${DISTRO_WHEELS}" && \
    find /tmp/build-wheels -name "*.whl" -exec mv {} "${DISTRO_WHEELS}" \;

# Now runtime required wheels are in DISTRO_WHEELS folder


###### INSTALL WHEELS into env - STAGE ######
FROM python_alpine AS install
ARG DISTRO_WHEELS

# If at runtime our app needs external packages, do apk install here
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends git && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

WORKDIR /app

# we copy the wheels built in 'build_wheels' stage
COPY --from=build_wheels ${DISTRO_WHEELS} dist

# Install wheels for our Distro and its Install/Runtime Dependencies
# in user site-packages (ie /root/.local/lib/python3.11/site-packages)
RUN pip install --no-deps --no-cache-dir --user ./dist/*.whl



## TEST Prod Wheels - Leaf STAGE ##
FROM python_alpine AS test_wheels
ARG DISTRO_WHEELS
WORKDIR /app

# Install uv for faster test dependencies installation than 'pip install'
COPY --from=ghcr.io/astral-sh/uv@sha256:2381d6aa60c326b71fd40023f921a0a3b8f91b14d5db6b90402e65a635053709 /uv /uvx /bin/
RUN uv venv

# Install Wheel of Package and Wheels its Prod dependencies
COPY --from=build_wheels ${DISTRO_WHEELS} dist
RUN uv pip install --no-deps --no-cache-dir ./dist/*.whl

# Install test dependencies (pytest, pytest-object-getter, etc) from pypi
COPY --from=test_builder requirements.txt .
RUN uv pip install --no-deps -r requirements.txt

# Add Pytest, installed in uv controlled venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Configure Pytest: runner, test discovery, etc
COPY pyproject.toml .

CMD [ "-ra", "tests" ]
# docker build --target test_wheels -t test-wheels-dev .
# docker run -it --rm -v "${PWD}/tests:/app/tests" --entrypoint pytest test-wheels-dev
# docker run -it --rm -v "${PWD}/tests:/app/tests" --entrypoint pytest test-wheels-dev -ra -vvs



## PROD - Leaf STAGE ##

FROM install AS prod

# Add user's bin folder, to PATH to make biskotakigold CLI available
ENV PATH="/root/.local/bin:$PATH"

ENTRYPOINT [ "biskotakigold" ]

# docker build -t biskotakigold .
# docker run -it --rm biskotakigold --help
# docker run -it --rm biskotakigold --version
