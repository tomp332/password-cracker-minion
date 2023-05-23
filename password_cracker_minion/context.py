"""
Singleton class to store global variables
"""

from password_cracker_minion.schemas.config import MinionBaseSettings


class MainContext:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """

        """
        self.main_settings: MinionBaseSettings = MinionBaseSettings()
