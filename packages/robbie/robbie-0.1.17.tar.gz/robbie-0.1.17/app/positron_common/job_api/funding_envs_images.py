import requests
from ..exceptions import RobbieException
from ..env_config import env
from ..cli.logging_config import logger


# API call
def list_funding_sources():
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN  }
    url = f'{env.API_BASE}/list-funding-sources'
    logger.debug(f'list_funding_sources Calling: {url}')
    response = requests.get(url, headers=Headers)
    logger.debug(response)
    if response.status_code != 200:
        raise RobbieException(
            f'list_funding_sources failed with http code: {response.status_code} \n {response.text}')
    else:
        logger.debug(response.json())
        return response.json()
    
# API call
def list_environments(fs_id: str):
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN, "fundingGroupId": fs_id  }
    url = f'{env.API_BASE}/list-environments'
    logger.debug(f'Calling: {url}')
    response = requests.get(url, headers=Headers)
    logger.debug(response)
    if response.status_code != 200:
        raise RobbieException(
            f'list_environments failed with http code: {response.status_code} \n {response.text}')
    else:
        logger.debug(response.json())
        return response.json()
    

# API call
def list_images(fs_id: str, env_id: str):
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN, "fundingGroupId": fs_id, "environmentId": env_id  }
    url = f'{env.API_BASE}/list-images'
    logger.debug(f'Calling: {url}')
    response = requests.get(url, headers=Headers)
    logger.debug(response)
    if response.status_code != 200:
        raise RobbieException(
            f'list_images failed with http code: {response.status_code} \n {response.text}')
    else:
        logger.debug(response.json())
        return response.json()
    



