import asyncio
import hashlib
from typing import Optional

import requests
from requests.models import Response
from uvicorn.main import logger

from password_cracker_minion import minion_context
from password_cracker_minion.src.models.minion_tasks import MinionFinishTaskModel


def hash_str(plain_text: str) -> str:
    """
    Hash a string to md5 format
    :param plain_text:
    :return:
    """
    return hashlib.md5(plain_text.encode()).hexdigest()


def brute_force_hashed_password() -> Optional[str]:
    """
    Brute force the password and send response to master server
    """
    try:
        logger.debug(
            f"Starting brute force task, task_id: {minion_context.current_task_id}, start_range: {minion_context.current_password_lst[0]}, end_range: {minion_context.current_password_lst[-1]}")
        for password in minion_context.current_password_lst:
            # Check if task is cancelled
            if minion_context.stop_current_task:
                logger.info(f"Brute force task cancelled, task_id: {minion_context.current_task_id}")
                return None
            # Check if password is cracked
            if hash_str(password) == minion_context.current_password_hash:
                logger.info(
                    f"PASSWORD CRACKED SUCCESSFULLY, {minion_context.current_password_hash}:::{password}")
                # Reset current task id
                logger.info(f"Brute force completed, task_id: {minion_context.current_task_id}")
                return password
    except asyncio.CancelledError:
        logger.info("Brute force task cancelled by master server")
    except Exception as e:
        logger.error(f"Failed to brute force password, task_id: {minion_context.current_task_id}, error: {e}")


def send_task_result(payload: MinionFinishTaskModel):
    """
    Send task result to master server
    """
    # Send task completion to master server
    logger.debug(f"Sending task result to master server, task_id: {minion_context.current_task_id}")
    r: Response = requests.post(
        f"http://{minion_context.main_settings.master_hostname}:{minion_context.main_settings.master_port}/"
        f"api/minion/finished",
        json=payload.dict())
    match r.status_code:
        case 200:
            logger.info(f"Task result sent successfully, task_id: {minion_context.current_task_id}")
        case _:
            logger.error(
                f"Failed to send task result, task_id: {minion_context.current_task_id}, message: {r.status_code}")
