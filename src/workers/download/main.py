from shared.s3 import s3

from contract.celery import queue
from contract.queues import DOWNLOAD_QUEUE
from contract.schemas.download import DownloadRequest
from contract.tasks import DOWNLOAD_FILE


@queue.task(name=DOWNLOAD_FILE, queue=DOWNLOAD_QUEUE)
def download_file(request: dict):
    request = DownloadRequest(**request)
    file = s3.download("downloads", request.key)
    return {"file": file}
