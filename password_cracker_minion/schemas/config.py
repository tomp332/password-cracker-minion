import random
import string
from typing import Optional

from pydantic import BaseSettings, Field, validator


class MinionBaseSettings(BaseSettings):
    """
    Minion src base settings
    """
    # Framework Settings
    master_hostname: str = Field(default='localhost', env='MASTER_HOSTNAME')
    master_port: int = Field(default=5000, env='MASTER_PORT')
    minion_hostname: Optional[str] = Field(env='MINION_HOSTNAME')
    minion_host: str = Field(default='0.0.0.0', env='MINION_HOSTNAME')
    minion_port: int = Field(default=5000, env='MINION_PORT')
    minion_password_limit: int = Field(default=500, env='MINION_PASSWORD_LIMIT')
    waiting_interval: int = Field(default=5, env='WAITING_INTERVAL')

    @validator("minion_hostname", pre=True, always=True)
    def set_minion_hostname(cls, _):
        """
        set_minion_hostname is the function that sets the minion hostname
        :return: minion_hostname
        """
        # Generate 5 digit random number
        characters = string.ascii_letters + string.digits
        return f"minion-server-{''.join(random.choice(characters) for _ in range(6))}"
