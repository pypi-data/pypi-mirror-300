"""Python Package named ToolAgent (A Highly-Modularized Tool Learning Framework for LLM Based Agent)"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

from fastmindapi.utils.config import get_config
from fastmindapi.utils.logging import get_logger

__all__ = [
    "__version__",
    "config",
    "logger"
]

# Official PEP 396
try:
    __version__ = version("fastmindapi")
except PackageNotFoundError:
    __version__ = "unknown version"

config = get_config()
logger = get_logger()


logger.info("FastMindAPI (FM) initialization is completed.")

from .server.core import Server  # noqa: F401, E402
from .client.core import Client  # noqa: F401, E402