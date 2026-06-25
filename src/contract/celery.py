import os

from celery import Celery

queue = Celery(
    backend=os.environ["BACKEND_URL"],
    broker=os.environ["BROKER_URL"],
)
