from fastapi import APIRouter
from uvicorn.main import logger

from password_cracker_minion import minion_context
from password_cracker_minion.src.models.responses import StopCrackTaskResponse

tasks_router = APIRouter(prefix="/api/tasks")


@tasks_router.get("/stop", response_model=StopCrackTaskResponse, summary="Stop current crack task")
async def stop_current_crack_process():
    # if minion_context.current_task_id is None:
    #     raise HTTPException(status_code=404, detail="No crack task is running")
    # Stop the current background tasks
    logger.debug("Stopping current crack task..")
    minion_context.stop_current_task = True
    return StopCrackTaskResponse(message="Stopping current crack task..")
