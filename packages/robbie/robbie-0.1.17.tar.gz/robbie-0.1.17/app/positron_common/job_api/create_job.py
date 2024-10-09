import requests
import json
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from ..utils import undefined
from ..config import PositronJob
from ..cli_args import args as cli_args
from ..env_config import env
from ..exceptions import RemoteCallException, RobbieKnownException
from ..cli.logging_config import logger
from ..env_defaults import current

class CreateJobBody(BaseModel):
    """
    Maps to the request body of the Create Job API
    """
    fundingGroupId: Optional[str] = Field(default=undefined)
    imageName: Optional[str] = Field(default=undefined)
    environmentId: Optional[str] = Field(default=undefined)
    jobArguments: Optional[List[str]] = Field(default=undefined)
    entryPoint: Optional[str] = Field(default=undefined)
    commands: Optional[str] = Field(default=undefined)
    maxTokens: Optional[int] = Field(default=undefined)
    maxMinutes: Optional[int] = Field(default=undefined)

    def http_dict(self) -> Dict[str, Any]:
        """
        Enables dropping fields that were never set and should be treated as undefined
        """
        return {k: v for k, v in self.__dict__.items() if v is not undefined}

    @staticmethod
    def from_config(job_config: PositronJob):
        instance = CreateJobBody(
            maxTokens=job_config.max_tokens,
            maxMinutes=job_config.max_time,
        )
        # determine if this is a generic or python job.
        if job_config.commands:
            instance.commands = ";\n".join(job_config.commands)
        elif job_config.entry_point:
            instance.entryPoint = job_config.entry_point
            instance.jobArguments = cli_args.job_args
        if job_config.funding_group_id:
            instance.fundingGroupId = job_config.funding_group_id
        if job_config.image:
            instance.imageName = job_config.image
        if job_config.environment_id:
            instance.environmentId = job_config.environment_id
        return instance



def create_job(job_config: PositronJob):
    logger.debug(job_config)
    data = CreateJobBody.from_config(job_config)
    logger.debug(data.http_dict())
    url = f'{env.API_BASE}/create-job'
    logger.debug(f'Calling: {url}')
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN}
    response = requests.post(url, headers=Headers, json=data.http_dict())
    logger.debug(response)
    if response.status_code != 200:
        body = response.json()
        # TODO: need standard error codes in errors
        if (body.get('message').lower() == 'concurrent job limit exceeded'):
            additional_help = [
                "You can free up capacity by terminating running jobs or reaching out to your group's",
                "administrator to increase your concurrent job limit.",
                f"{current.portal_base}/portal/app/dashboard/jobs"
            ]
            raise RobbieKnownException(
                reason=body.get('message').lower(),
                user_friendly_message=body.get('userFriendlyErrorMessage'),
                additional_help="\n".join(additional_help)
            )
        if body.get('userFriendlyErrorMessage'):
            print(body.get('userFriendlyErrorMessage'))
            logger.debug(json.dumps(body, indent=2))
            raise RemoteCallException('Cannot create job. Please resolve the issue and try again.')
        raise RemoteCallException(
            f'Job creation failed with http code: {response.status_code} \n {response.text}')
    else:
        logger.debug(response.json())
        return response.json()

