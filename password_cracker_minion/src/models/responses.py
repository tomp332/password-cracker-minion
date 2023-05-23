from pydantic import BaseModel


class StopCrackTaskResponse(BaseModel):
    """
    Response model for stop_crack_task endpoint
    """
    task_id: str
