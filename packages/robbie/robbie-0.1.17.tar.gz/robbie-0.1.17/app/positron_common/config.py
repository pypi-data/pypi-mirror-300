from pydantic import BaseModel, field_validator
from typing import Dict, Optional, ClassVar, List
import os
import sys
import yaml
import re
from pydantic_yaml import parse_yaml_raw_as, to_yaml_str
from .utils import debug
from .exceptions import RobbieException
from positron_common.user_config import user_config, REMOTE_FUNCTION_SECRET_KEY_NAME

class PositronJob(BaseModel):
    """
    The Job details as defined in the `python_job` from the `job_config.yaml` file.
    """
    funding_group_id: Optional[str] = None
    environment_id: Optional[str] = None
    image: Optional[str] = None
    commands: Optional[List[str]] = None
    entry_point: Optional[str] = None
    workspace_dir: Optional[str] = None
    max_tokens: Optional[int] = None
    max_time: Optional[int] = None
    env: Optional[Dict[str, str]] = None
    python_version: Optional[str] = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    ENV_PREFIX: ClassVar[str] = '__RUNTIME_'

    @field_validator('commands', mode='after')
    def ensure_non_empty(cls, commands):
        return commands if len(commands) else None

    @field_validator('env', mode='after')
    def ensure_env_is_dict(cls, v):
        if isinstance(v, dict):
            return v
        raise ValueError('env must be a dictionary')

    @field_validator('max_time', mode='before')
    def ensure_max_time_is_int(cls, max_time: int | str | None) -> int | None:
        return cls._max_time_to_minutes(max_time)

    @field_validator('max_tokens', mode='before')
    def ensure_max_tokens_is_int(cls, max_tokens: int | str | None) -> int | None:
        return cls._max_tokens_to_int(max_tokens)

    def create_runtime_env(self) -> Dict[str, str]:
        """
        Used on the client side to create the prefixed runtime environment variables
        to avoid conflicts with the local environment variables.
        """
        env: Dict[str, str] = {}
        # without env_prefix?? yes, but maybe not in this file, but part of the deploy.py file.
        env[REMOTE_FUNCTION_SECRET_KEY_NAME] = user_config.user_auth_token
        if not self.env:
            return env
        for key, value in self.env.items():
            if (value == ""):
                env_var = os.environ.get(key)
                if env_var is None:
                    raise ValueError(f"The env prop {key} is unset inside job_config.yaml and also unset in local env vars. Please set this value.")
                env[f'{self.ENV_PREFIX}{key}'] = env_var
            else:
                env[f'{self.ENV_PREFIX}{key}'] = value
        return env

    def parse_runtime_env(self) -> Dict[str, str]:
        """
        Used on the server side to parse the prefixed runtime environment variables
        and inject them into the client job environment.
        """
        env: Dict[str, str] = {}
        if not self.env:
            return env
        print(self.env)
        for key, value in self.env.items():
            if value == "":
                env_value = os.environ.get(f'{self.ENV_PREFIX}{key}')
                if env_value is None:
                    raise ValueError(f"The env prop {key} is unset inside job_config.yaml and also unset in local env vars. Please set this value.")
                env[key] = env_value
            else:
                env[key] = value
        return env

    @staticmethod
    def _max_time_to_minutes(max_time: int | str | None) -> int | None:
        if not max_time:
            return None
        if isinstance(max_time, int):
            return max_time
        matches = re.search(r'^(\d+):(\d{2})$', max_time)
        if matches is None:
            raise ValueError(f'Invalid Job Config: Field "max_time" ({max_time}) must have the format "HH:MM" or be a positive integer')
        try:
            hours = int(matches.group(1))
            minutes = int(matches.group(2))
        except:
            raise ValueError(f'Invalid Job Config: Field "max_time" ({max_time}) must have the format "HH:MM" or be a positive integer')
        if minutes >= 60:
            raise ValueError('Invalid Job Config: Field "max_time" ({max_time}) has invalid minutes! Must be 0 <= minutes < 60!')
        return hours * 60 + minutes

    @staticmethod
    def _max_tokens_to_int(max_tokens: int | str | None) -> int | None:
        if not max_tokens:
            return None
        if isinstance(max_tokens, int):
            return max_tokens
        try:
            max_tokens = int(max_tokens)
        except:
            raise ValueError(f'Invalid Job Config: "max_tokens" ({max_tokens}) needs to be a positive integer.')
        if max_tokens <= 0:
            raise ValueError(f'Invalid Job Config: "max_tokens" ({max_tokens}) needs to be a positive integer.')
        return max_tokens

    def validate_values(self) -> None:
        errors = []
        # Per our plan to enable defaults, we do not require a funding group. 
        # If no funding group is specified, the free trial or personal funding group is used.
        # if not self.funding_group_id:
            # errors.append('funding_group is required')
        if not self.commands and not self.entry_point:
            errors.append('At least one of commands or entry_point must be provided')
        if self.env and not validate_env_vars(self.env):
            errors.append('At least one of the environment variables provided is invalid')
        if errors:
            raise RobbieException(f'Invalid configuration. Errors: {errors}')
        return None

class PositronJobConfig(BaseModel):
    """
    The `job_config.yaml` schema class.
    """
    version: float
    python_job: PositronJob

    def write_to_file(this, filename: str = "./job_config.yaml"):
        with open(filename, 'w') as file:
            file.write(to_yaml_str(this, exclude_unset=True))


def is_valid_key_value(keyvalue):
    """
    Validate that the key-value contains only alphanumeric characters, dashes, and underscores, and has no spaces.
    """
    return bool(re.match(r'^[\w-]+$', keyvalue))

def validate_env_vars(env_dict):
    """
    Validate the environment variables from the given dictionary.
    """
    valid = True
    for key, value in env_dict.items():
        if not is_valid_key_value(key):
            print(f"Invalid key (contains invalid characters or spaces): {key}")
            valid = False
        if value != "" and not is_valid_key_value(value):
            print(f"Invalid value (contains invalid characters or spaces): {value}")
            valid = False
    return valid

def merge_config(base_config: PositronJob, override_config: PositronJob) -> PositronJob:
    """
    Makes it easy to merge decorator configs on top of the YAML config.
    """
    update_data = override_config.dict(exclude_unset=True)
    updated_config = base_config.copy(update=update_data)
    return updated_config

def parse_job_config(config_path: str = 'job_config.yaml') -> Optional[PositronJob]:
    """
    Load the job configuration from the `job_config.yaml` file if it exists
    """
    
    if not os.path.exists(config_path):
        debug('job_config.yaml file not found')
        return None

    try:
        with open(config_path, 'r') as job_config_file:
            job_config_dict = yaml.safe_load(job_config_file)
            job_config = PositronJobConfig(**job_config_dict)
            return job_config.python_job
    except Exception as e:
        print(f'Error loading job configuration! {str(e)}')
        return None
