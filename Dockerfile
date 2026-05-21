FROM python:3.13-alpine

LABEL maintainer="Peng Xiao <xiaoquwl@gmail.com>"

# Install uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:0.9.15 /uv /bin/uv

RUN apk add --no-cache gcc musl-dev g++

COPY . /yabgp

WORKDIR /yabgp

ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

EXPOSE 8801

VOLUME ["~/data"]

ENTRYPOINT ["/yabgp/.venv/bin/yabgpd"]

CMD []
