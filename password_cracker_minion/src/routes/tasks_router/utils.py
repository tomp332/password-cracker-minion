import asyncio
import hashlib
from typing import Optional

from uvicorn.main import logger

from password_cracker_minion import minion_context


def hash_str(plain_text: str) -> str:
    """
    Hash a string to md5 format
    :param plain_text:
    :return:
    """
    return hashlib.md5(plain_text.encode()).hexdigest()


async def brute_force_hashed_password():
    """
    Brute force the password

    :return:
    """
    plain_text_password: Optional[str] = None
    try:
        for password in minion_context.current_password_lst:
            if hash_str(password) == minion_context.current_password_hash:
                plain_text_password = password
    except asyncio.CancelledError:
        logger.info("Brute force task cancelled by master server")
    return plain_text_password


async def launch_brute_force():
    """
    Launch brute force task
    :return:
    """
    logger.info("Starting brute force task")
    if not minion_context.current_task_id:
        logger.error("No task id found, unable to start brute force task")
    else:
        # Append the task to all tasks
        minion_context.brute_force_tasks.append(asyncio.create_task(launch_brute_force()))
