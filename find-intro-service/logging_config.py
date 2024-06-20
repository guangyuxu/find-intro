import sys
import logging
from src.env.env import LOGGING_LEVEL

log_format = '[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s'
date_format = '%Y-%m-%d-%H%M%S.%z'
formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(LOGGING_LEVEL)
stream_handler.setFormatter(formatter)

logging.basicConfig(level=LOGGING_LEVEL, handlers=[stream_handler])
