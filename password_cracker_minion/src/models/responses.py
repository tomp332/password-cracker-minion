from typing import List

from pydantic import BaseModel


class StopCrackTaskResponse(BaseModel):
    """
    Response model for stop_crack_task endpoint
    """
    task_id: str


class StartCrackTaskResponse(BaseModel):
    """
    Response model for start_crack_task endpoint
    """
    task_id: str
    crack_hash_range: List[str]
    password: str


class MinionSignUpResponse(BaseModel):
    """
    Minion sign up response
    """
    minion_id: str
