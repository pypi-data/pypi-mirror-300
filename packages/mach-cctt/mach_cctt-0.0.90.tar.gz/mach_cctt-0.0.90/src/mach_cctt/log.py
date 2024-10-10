import logging

from mach_client.log import *

from . import config


# Default logger for this project
logger: Logger = make_logger("cctt", logging.DEBUG, config.log_file)
