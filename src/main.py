import os
import yaml

with open('../config/dev/parameters.yaml', 'r') as file:
    parameters = yaml.safe_load(file)['parameters']

from logger.logger import Logger
from configuration import Configuration

if __name__ == '__main__':
    logger = Logger(parameters['logger'])

    configuration = Configuration(os.getenv('GOOGLE_CREDENTIALS'))


    logger.debug('This is a debug')
    logger.error(f"Configuration projectid: {configuration.projectId()}")
    logger.error(f"Configuration credentials: {configuration.googleCredentialsFilePath()}")