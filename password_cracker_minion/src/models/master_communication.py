from pydantic import BaseModel


class MinionSignUpModel(BaseModel):
    """
    Minion sign up model
    """
    minion_hostname: str


class MinionSignUpResponse(BaseModel):
    """
    Minion sign up response
    """
