import requests

from password_cracker_minion import minion_context


def minion_startup_tasks():
    """
    minion_startup_tasks is the function that runs on startup
    :return:
    """
    requests.post(
        f"http://{minion_context.main_settings.master_hostname}:{minion_context.main_settings.master_port}/api/minion/signup/")
