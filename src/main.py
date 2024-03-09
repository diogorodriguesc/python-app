import os
import yaml

GOOGLE_CREDENTIALS_ENV_VAR = 'GOOGLE_CREDENTIALS'

with open('../config/dev/parameters.yaml', 'r') as file:
    parameters = yaml.safe_load(file)['parameters']

from logger.logger import Logger
from configuration import Configuration

if __name__ == '__main__':
    try: 
        logger = Logger(parameters.get('logger'))
        google_credentials = os.getenv(GOOGLE_CREDENTIALS_ENV_VAR)
        if google_credentials is None:
            raise Exception(f'{GOOGLE_CREDENTIALS_ENV_VAR} environment variable missing!')
    
        configuration = Configuration(google_credentials)
    except Exception as exception:
        logger.critical(exception)