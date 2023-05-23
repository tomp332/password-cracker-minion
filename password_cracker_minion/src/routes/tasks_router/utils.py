import asyncio
import hashlib

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


async def brute_force_hashed_password():
    """
    Brute force the password and send response to master server
    """
    try:
        logger.debug(f"Starting brute force task, task_id: {minion_context.current_task_id}")
        for password in minion_context.current_password_lst:
            if hash_str(password) == minion_context.current_password_hash:
                logger.info(
                    f"PASSWORD CRACKED SUCCESSFULLY, {minion_context.current_password_hash}:::{password}")
                send_task_result(plaintext_password=password)
                # Reset current task id
                minion_context.current_task_id = None
                logger.info(f"Task completed, task_id: {minion_context.current_task_id}")
    except asyncio.CancelledError:
        logger.info("Brute force task cancelled by master server")


def send_task_result(plaintext_password: str):
    """
    Send task result to master server
    """
    # Send task completion to master server
    r: Response = requests.post(
        f"http://{minion_context.main_settings.master_hostname}:{minion_context.main_settings.master_port}/"
        f"api/minion/cracked",
        json=MinionFinishTaskModel(hashed_password=minion_context.current_password_hash,
                                   task_id=minion_context.current_task_id,
                                   password_plaintext=plaintext_password))
    match r.status_code:
        case 200:
            logger.info(f"Task result sent successfully, task_id: {minion_context.current_task_id}")
        case _:
            logger.error(
                f"Failed to send task result, task_id: {minion_context.current_task_id}, message: {r.status_code}")


async def launch_brute_force():
    """
    Launch brute force task
    :return:
    """
    if not minion_context.current_task_id:
        logger.error("No task id found, unable to start brute force task")
    else:
        # Append the task to all tasks
        minion_context.brute_force_tasks.append(asyncio.create_task(brute_force_hashed_password()))
