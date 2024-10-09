import sys
import os
import traceback
from typing import Any

def debug(log: Any, default: str | None = None) -> None:
    """
        This debug utility will check for '--debug' command line flag to only print logs if it is set
        For exceptions this utility will print the stack trace as well
        The default parameter is usable as an alternate log in case the '--debug' flag is not set
    """
    if sys.argv.__contains__('--debug'):
        if isinstance(log, Exception):
            print('DEBUG ERROR: An exception occurred')
            traceback.print_exception(type(log), log, log.__traceback__)
        else:
            print(f'DEBUG: {log}')
    elif default is not None:
        print(default)

def get_python_version():
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

def get_default_workspace_dir():
    cwd = os.getcwd()
    return cwd

# Sentinel object for undefined
undefined = object()
