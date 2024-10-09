import os
from dataclasses import dataclass
from dotenv import load_dotenv
from positron_common.user_config import REMOTE_FUNCTION_SECRET_KEY_NAME
from positron_common.constants import temp_path

load_dotenv()

# Disable stdout buffering
os.environ['PYTHONUNBUFFERED'] = '1'
os.environ['POSITRON_CLOUD_ENVIRONMENT'] = '1'

@dataclass
class RunnerEnv():
  """
  The environment variables and other global vars required by the Runner.
  """
  SYSTEM_AUTHENTICATION_KEY: str = os.getenv('SYSTEM_AUTHENTICATION_KEY', "")
  REGION: str = os.getenv("REGION", "us-west-2")
  AWS_JOB_LOG_GROUP_NAME: str = os.getenv("AWS_JOB_LOG_GROUP_NAME", "")
  API_ENDPOINT: str = os.getenv("API_ENDPOINT", "")
  POSITRON_CLI_ENV: str = os.getenv("POSITRON_CLI_ENV", "development")
  POSITRON_CHARGE_INTERVAL: int = int(os.getenv('POSITRON_CHARGE_INTERVAL', 60))
  POSITRON_STDOUT_INTERVAL: int = int(os.getenv('POSITRON_STDOUT_INTERVAL', 2))
  POSITRON_CHECK_TERMINATION_INTERVAL: int = int(os.getenv('POSITRON_CHECK_TERMINATION_INTERVAL', 10))
  RUNNER_CWD: str = os.getenv('RUNNER_CWD', os.path.join(os.getcwd(), f'{temp_path}/job-controller'))
  ROBBIE_CLI_PATH: str = os.getenv('ROBBIE_CLI_PATH', '$HOME/python-decorator')
  APP_NAME: str = os.getenv('APP_NAME', 'robbie')
  LOG_LEVEL: str = os.getenv('LOG_LEVEL', "DEBUG") # see logging.getLevelNameMapping()
  JOB_ID: str | None = os.getenv('JOB_ID', None)
  JOB_CWD: str = os.getenv('JOB_CWD', os.path.join(os.getcwd(), f'{temp_path}/job-execution'))
  JOB_USER: str | None = os.getenv('JOB_USER', None)
  JOB_OWNER_EMAIL: str | None = os.getenv('JOB_OWNER_EMAIL', None)
  S3_BUCKET: str = os.getenv('S3_BUCKET', 'positron-dev-workspaces')
  ROBBIE_RUNNER_AWS_ACCESS_KEY_ID: str | None = os.getenv('ROBBIE_RUNNER_AWS_ACCESS_KEY_ID')
  ROBBIE_RUNNER_AWS_SECRET_ACCESS_KEY: str | None = os.getenv('ROBBIE_RUNNER_AWS_SECRET_ACCESS_KEY')
  REMOTE_FUNCTION_SECRET_KEY: str = os.getenv(REMOTE_FUNCTION_SECRET_KEY_NAME, "")
  rerun: bool = False

  def env_without_runner_env(self):
    """
    Will blacklist env vars we're explicitly expecting to be
    set by the infra and used by the Runner.
    """
    env = {}
    for k, v in os.environ.items():
      if k not in self.__dict__:
        env[k] = v
    # Explicitly set as this is just the users API key and will be used to calc integrity hash
    # if this is the remote function.
    env[REMOTE_FUNCTION_SECRET_KEY_NAME] = self.REMOTE_FUNCTION_SECRET_KEY
    return env

runner_env = RunnerEnv()
