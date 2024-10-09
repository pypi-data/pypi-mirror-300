from pydantic import BaseModel
from .env_defaults import current
from .user_config import user_config

class EnvConfig(BaseModel):
    """
    The environment configuration for the Positron CLI.
    Loaded like so: defaults <- config file <- env vars.
    """
    API_BASE: str = current.api_base
    SOCKET_IO_DOMAIN: str = current.ws_base
    AUTH0_DOMAIN: str = current.auth0_domain
    AUTH0_CLIENT_ID: str = current.auth0_client_id
    AUTH0_AUDIENCE: str =  current.auth0_audience
    COMPRESSED_WS_NAME: str = 'workspace.tar.gz'
    SOCKET_IO_PATH: str = '/api/ws/socket.io'
    USER_AUTH_TOKEN: str | None = None 

    def __init__(self):
        super().__init__()

        # Override app dev defaults
        if user_config.user_auth_token:
            self.USER_AUTH_TOKEN = user_config.user_auth_token
        if user_config.backend_api_base_url:
            self.API_BASE = user_config.backend_api_base_url
        if user_config.backend_ws_base_url:
            self.SOCKET_IO_DOMAIN = user_config.backend_ws_base_url

env = EnvConfig()
"""
The environment configuration for the Positron CLI.
"""
