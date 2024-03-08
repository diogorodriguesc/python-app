import os

from logger import Logger
from configuration import Configuration

logger = Logger()

configuration = Configuration('project-id', os.getenv('GOOGLE_CREDENTIALS'))

credentials = configuration.googleCredentialsFilePath()

logger.info(f"Configuration credentials: {credentials}")
logger.warning(f"This is a warning")
logger.error(f"This is a error")