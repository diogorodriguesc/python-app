# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.5
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN apt-get update
RUN apt install -y  \
    postgresql  \
    postgresql-contrib  \
    gcc  \
    libpq-dev  \
    python3-dev \
    netcat-openbsd

RUN pip install --upgrade pip

RUN pip install psycopg2-binary

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python3 -m pip install -r requirements.txt

USER appuser

EXPOSE 5000

CMD sh bin/run_migrations.sh && flask --debug --app main run --host=0.0.0.0
