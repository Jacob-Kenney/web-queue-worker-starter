from fastapi import APIRouter

from contract.celery import queue
from contract.queues import UPLOAD_QUEUE
from contract.schemas.upload import UploadRequest
from contract.tasks import UPLOAD_FILE

router = APIRouter()


@router.post("/upload")
async def upload(body: UploadRequest):
    task = queue.send_task(UPLOAD_FILE, args=[body.dict()], queue=UPLOAD_QUEUE)
    return {"task_id": task.id}
