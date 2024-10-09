import platform
from rich.console import Console

# Website colors
ROBBIE_GREEN="#1e3138"
ROBBIE_ORANGE="#41A7FF"
ROBBIE_GREY="#4d5f69"
SPINNER = "line" if platform.system() == "Windows" else "dots"

# Used to print nice message to the end user, this is not a logger. See `logging_config.py` for logging.
console = Console()
