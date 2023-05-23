import asyncio

import pydantic
import requests
from requests.models import Response
from uvicorn.main import logger

from password_cracker_minion import minion_context
from password_cracker_minion.src.models.responses import StartCrackTaskResponse, MinionSignUpResponse
from password_cracker_minion.src.routes.tasks_router.utils import launch_brute_force


def fetch_task():
    """
    Fetch task from master server
    """
    r: Response = requests.get(
        f"http://{minion_context.main_settings.master_hostname}:{minion_context.main_settings.master_port}/"
        f"api/minion/task?limit={minion_context.main_settings.minion_password_limit}&minion_id={minion_context.minion_id}")
    match r.status_code:
        case 204:
            pass
        case 200:
            new_task_response: StartCrackTaskResponse = StartCrackTaskResponse(**r.json())
            # Assign metadata of task to current context
            minion_context.current_task_id = new_task_response.task_id
            minion_context.current_password_hash = new_task_response.password
            minion_context.current_password_lst = new_task_response.crack_hash_range
            logger.info(f"New task received, task_id: {minion_context.current_task_id}")
        case _:
            raise Exception(f"Failed to register minion, bad status code received, message: {r}")


def register_minion():
    """
    register_minion is the function that registers the minion to the master server
    """
    r: Response = requests.get(
        f"http://{minion_context.main_settings.master_hostname}:{minion_context.main_settings.master_port}/"
        f"api/minion/signup?minion_hostname={minion_context.main_settings.minion_hostname}")
    if r.status_code != 200:
        raise Exception(f"Failed to register minion, bad status code received, message: {r.text}")
    signup_response: MinionSignUpResponse = MinionSignUpResponse(**r.json())
    # Assign current minion id
    minion_context.minion_id = signup_response.minion_id
    logger.info(f"Minion registered successfully, minion_id: {minion_context.minion_id}")


async def minion_startup_tasks():
    """
    minion_startup_tasks is the function that runs on startup
    :return:
    """
    try:
        register_minion()
        fetch_task()
        while minion_context.current_task_id is None:
            logger.info("No tasks available, waiting for tasks...")
            await asyncio.sleep(5)
            fetch_task()
        await launch_brute_force()
    except requests.exceptions.ConnectionError as connection_err:
        raise Exception(f"Failed to register minion, {connection_err}")
    except pydantic.error_wrappers.ValidationError as validation_err:
        raise Exception(f"Failed to register minion, received unknown response from master server, {validation_err}")
