from fastapi import APIRouter

from contract.celery import queue
from contract.queues import DOWNLOAD_QUEUE
from contract.schemas.download import DownloadRequest
from contract.tasks import DOWNLOAD_FILE

router = APIRouter()


@router.post("/download")
async def download(body: DownloadRequest):
    task = queue.send_task(DOWNLOAD_FILE, args=[body.dict()], queue=DOWNLOAD_QUEUE)
    return {"task_id": task.id}
