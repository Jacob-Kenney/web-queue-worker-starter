# Queue Worker Starter

A starter template for the **API → Queue → Worker → Storage** pattern using FastAPI, Celery, RabbitMQ, Redis, and MinIO. Includes an optional logging extension with Fluentd, Elasticsearch, and Kibana.

## Architecture

```
Client
  │
  ▼
POST /upload ──► FastAPI (api/main.py)
  │  POST /download        │ Celery send_task()
  │  GET  /result/{id}     ▼
  │                  RabbitMQ (broker)
  │                       │
  │         ┌─────────────┼─────────────┐
  │         ▼             ▼             ▼
  │   worker-upload  worker-download  Redis (results)
  │         │             │
  │         ▼             ▼
  │         └─── MinIO (S3) ──┘
  │
  └─── Client polls GET /result/{id} for completion
```

## Services

| Service | Role | Exposed |
|---|---|---|
| `api` | FastAPI application (uvicorn) | `:8000` |
| `worker-upload` | Celery worker — upload queue | internal |
| `worker-download` | Celery worker — download queue | internal |
| `rabbitmq` | Message broker | internal |
| `redis` | Result backend | internal |
| `minio` | S3-compatible object storage | internal |

## Quick Start

```bash
docker compose up --build
```

## API Reference

### Upload a file

```bash
curl -X POST http://localhost:8000/upload \
  -H "Content-Type: application/json" \
  -d '{"filename": "hello.txt", "content": "Hello, World!"}'
# → {"task_id": "<uuid>"}
```

### Check task result

```bash
curl http://localhost:8000/result/<task_id>
# → {"status": "SUCCESS", "data": {"key": "downloads/hello.txt"}}
```

### Download a file

```bash
curl -X POST http://localhost:8000/download \
  -H "Content-Type: application/json" \
  -d '{"key": "downloads/hello.txt"}'
# → {"task_id": "<uuid>"}
# Poll /result/<task_id> for the file content.
```

## Local Development

Requires Python ≥3.14 and `uv`:

```bash
cd src
uv venv && source .venv/bin/activate
uv sync
```

You'll need RabbitMQ, Redis, and MinIO running locally (e.g. via Docker) before starting services:

```bash
uvicorn api.main:app --reload
celery -A workers.upload.main worker --queues=upload
celery -A workers.download.main worker --queues=download
```

## Logging Extension

An optional EFK stack is available in `examples/logging/`:

```bash
docker compose -f examples/logging/docker-compose.yaml up --build
```

Adds Fluentd (`:24224`), Elasticsearch, and Kibana (`:5601`).

## Project Structure

```
├── docker-compose.yaml
├── examples/logging/          # EFK logging extension
└── src/
    ├── api/                   # FastAPI routes, entrypoint, Dockerfile
    │   └── routers/
    ├── contract/              # Shared schemas, queue/task names, Celery app
    │   └── schemas/
    └── workers/               # Celery workers + shared S3 client
        ├── upload/
        ├── download/
        └── shared/
```

## License

MIT © 2026 Jacob Kenney
