from pydantic import BaseModel, Field


class MinionFinishTaskModel(BaseModel):
    """
    Minion finish task model

    """
    hashed_password: str
    password_plaintext: str
    task_id: str
    password_cracked: bool = Field(default=True)
