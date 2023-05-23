"""
Singleton class to store global variables
"""
from asyncio import Task
from typing import Optional, List

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
        self.minion_id: Optional[str] = None
        self.stop_current_task: bool = False
        self.current_crack_task_id: Optional[str] = None
        self.current_task_id: Optional[str] = None
        self.current_password_hash: str = ""
        self.current_password_lst: List[str] = []
        self.brute_force_tasks: List[Task] = []
