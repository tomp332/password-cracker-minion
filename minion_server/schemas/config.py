from pydantic import BaseSettings, Field


class MinionBaseSettings(BaseSettings):
    """
    Minion server base settings
    """
    # Framework Settings
    minion_hostname: str = Field(default='0.0.0.0', env='MINION_HOSTNAME')
    minion_port: int = Field(default=8001, env='MINION_PORT')
