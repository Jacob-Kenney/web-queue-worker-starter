FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install  --no-cache-dir .

COPY api/ ./
COPY contract/ contract/

RUN useradd --create-home app

USER app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
