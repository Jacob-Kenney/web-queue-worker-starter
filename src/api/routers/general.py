from fastapi import APIRouter

from contract.celery import queue

router = APIRouter()


@router.get("/result/{task_id}")
async def get_result(task_id: str):
    result = queue.AsyncResult(task_id)
    if result.status == "SUCCESS":
        return {"status": result.status, "data": result.result}
    return {"status": result.status}
