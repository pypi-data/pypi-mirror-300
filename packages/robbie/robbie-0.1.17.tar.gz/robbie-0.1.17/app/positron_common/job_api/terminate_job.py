import requests
from positron_common.utils import debug
from positron_common.exceptions import RobbieException
from ..env_config import env
from ..cli.logging_config import logger

def terminate_job(job_id, reason: str):
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN, "PositronJobId": job_id}
    url = f'{env.API_BASE}/terminate-job-user'
    logger.debug(f'Calling: {url}')
    data = { "reason": reason }
    response = requests.post(url, headers=Headers, json=data)
    logger.debug(response)
    if response.status_code != 200:
        raise RobbieException(
            f'Failed to terminate job with http code: {response.status_code} \n {response.text}')
    else:
        logger.debug(response.json())
        return response.json()