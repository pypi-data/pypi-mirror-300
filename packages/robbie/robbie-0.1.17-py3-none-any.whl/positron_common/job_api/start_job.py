import requests
from positron_common.utils import debug
from positron_common.exceptions import RemoteCallException
from ..env_config import env

def start_job(job_id, data):
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN, "PositronJobId": job_id}
    url = f'{env.API_BASE}/start-job'
    
    debug(f'Calling: {url}')
    response = requests.post(url, headers=Headers, json=data)
    
    debug(response)
    if response.status_code != 200:
        raise RemoteCallException(
            f'Failed to start job with http code: {response.status_code} \n {response.text}')
    else:
        debug(response.json())
        return response.json()