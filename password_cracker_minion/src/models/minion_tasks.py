from pydantic import BaseModel, Field, validator

from password_cracker_minion.schemas.enums import StatusEnum


class MinionFinishTaskModel(BaseModel):
    """
    Minion finish task model

    """
    minion_id: str = Field(...)
    hashed_password: str = Field(...)
    password_plaintext: str = Field(default="")
    task_id: str = Field(...)
    status: str = Field(default=StatusEnum.COMPLETED.value)

    @validator('status', pre=True, always=True)
    def set_status(cls, v):
        """
        Set status to match the proper enum value
        :param v:
        :return: StatusEnum
        """
        return f'{StatusEnum(v).value}'
