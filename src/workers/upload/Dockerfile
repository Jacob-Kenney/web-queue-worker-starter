FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install  --no-cache-dir .

COPY workers/upload ./
COPY workers/shared shared/
COPY contract/ contract/

RUN useradd --create-home app

USER app

CMD ["celery", "-A", "main", "worker", "--loglevel=info", "--queues=upload"]
