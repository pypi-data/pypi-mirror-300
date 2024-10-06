import sys

from loguru import logger  # noqa

from ambient_edge_server.config import settings  # noqa

logger.remove()
logger.add(
    sys.stderr,
    level=settings.ambient_log_level,
    enqueue=True,
    backtrace=True,
    diagnose=True,
)
