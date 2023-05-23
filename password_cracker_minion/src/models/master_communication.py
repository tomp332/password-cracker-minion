from pydantic import BaseModel


class MinionSignUpResponse(BaseModel):
    """
    Minion sign up response
    """
    minion_id: str
