import pydantic
import requests
from requests.models import Response
from uvicorn.main import logger

from password_cracker_minion import minion_context
from password_cracker_minion.src.models.master_communication import MinionSignUpResponse


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


def minion_startup_tasks():
    """
    minion_startup_tasks is the function that runs on startup
    :return:
    """
    try:
        register_minion()
    except requests.exceptions.ConnectionError as connection_err:
        raise Exception(f"Failed to register minion, {connection_err}")
    except pydantic.PydanticValueError as validation_err:
        raise Exception(f"Failed to register minion, received unknown response from master server, {validation_err}")
