from shared.s3 import s3

from contract.celery import queue
from contract.queues import UPLOAD_QUEUE
from contract.schemas.upload import UploadRequest
from contract.tasks import UPLOAD_FILE


@queue.task(name=UPLOAD_FILE, queue=UPLOAD_QUEUE)
def upload_file(request: dict):
    request = UploadRequest(**request)
    key = s3.upload("downloads", request.filename, request.content)
    return {"key": key}
